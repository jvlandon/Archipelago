from CommonClient import (CommonContext, ClientCommandProcessor,
                          get_base_parser, server_loop, gui_enabled)
import asyncio
import sys
import Utils
from NetUtils import NetworkItem, ClientStatus
from typing import TYPE_CHECKING, Any
from enum import Enum


from . import pine
from .addressdata import ALL_SONGS, ALL_VENUES, Difficulty, VenueData, SongData
from .items import ITEM_NAME_TO_ID
import logging

from Utils import async_start

if TYPE_CHECKING:
    from .world import GH2World

logger = logging.getLogger("Client")

songs_by_tier = {}
for song in ALL_SONGS:
    songs_by_tier.setdefault(song.tier, []).append(song)

songs_and_venues_by_pointer = {item.pointer: item for item in ALL_SONGS + ALL_VENUES}
songs_and_venues_by_name = {item.name: item for item in ALL_SONGS + ALL_VENUES}
venues_by_tier = {venue.tier: venue for venue in ALL_VENUES}
pine_client = pine.PineClient()

class ConnectionStatus(Enum):
    NOT_CONNECTED = 0
    SCOUTS_NOT_SENT = 1
    SCOUTS_SENT = 2
    GAME_RUNNING = 3

class GH2CommandProcessor(ClientCommandProcessor):

    def __init__(self, ctx: "GH2Context"):
        super().__init__(ctx)

    def _status(self):
        self.output(f"Connected: {self.ctx.server is not None}")

class GH2Context(CommonContext):
    game = "Guitar Hero II"

    items_handling = 0b111

    client_loop: asyncio.Task[None]
    slot_data: dict[str, Any]

    difficulty: Difficulty
    venue_requirement: bool
    four_star_checks: bool
    five_star_checks: bool
    all_notes: bool

    last_connected_slot: int | None = None
    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED
    highest_processed_item_index: int = 0
    queued_locations: list[int]


    scene_pointer = 0x00473860
    score_screen = 0x00AC2450
    encore_screen = 0x00AC2610
    winner_screen = 0x00AC2760
    current_song = 0x00ABF164
    cash_address = 0x00AAB4C4




    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.command_processor = GH2CommandProcessor
        self.slot_data = {}
        self.queued_locations = []
        self.game_initialized = False
        self.tags = {"AP"}
        self.lock = asyncio.Lock()
        self.seed_name = None




    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    def handle_connection_loss(self, msg: str) -> None:
        super().handle_connection_loss(msg)

    async def connect(self, address: str | None = None) -> None:
        await super().connect(address)

    async def disconnect(self, *args, **kwargs) -> None:
        self.finished_game = False
        self.locations_checked = set()
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        self.game_initialized = False

        await pine_client.disconnect()
        logger.info("PINE Disconnected")
        await super().disconnect(*args, **kwargs)


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            async_start(process_connected(self, cmd, args))
        elif cmd == "ReceivedItems":
            async_start(process_received(self, cmd, args))
        elif cmd == "RoomInfo":
            async_start(process_room_info(self, cmd, args))



    def run_gui(self):
        from kvui import GameManager

        class GHManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Guitar Hero II Client"

        self.ui = GHManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

async def process_room_info(ctx, cmd, args):
    ctx.seed_name = args["seed_name"]
    state_data = Utils.persistent_load()
    gh2_data = state_data.get(f"GH2 {ctx.seed_name}", {})
    ctx.highest_processed_item_index = gh2_data.get("highest index", 0)
    ctx.items_received = gh2_data.get("items received", [])
    ctx.difficulty = gh2_data.get("difficulty")
    if ctx.difficulty is not None:
        ctx.queued_locations = await pine_client.verify_locations(ALL_SONGS, ctx)
        await send_location_check(ctx, ctx.queued_locations)
    ctx.queued_locations = []

async def process_connected(ctx: GH2Context, cmd: str, args: dict):
    async with ctx.lock:
        if cmd == "Connected":
            if not pine_client.is_connected:
                await pine_client.connect()
            ctx.connection_status = ConnectionStatus.GAME_RUNNING
            ctx.last_connected_slot = ctx.slot
            ctx.slot_data = args["slot_data"]
            raw_difficulty = ctx.slot_data.get("difficulty", 0)
            ctx.difficulty = Difficulty(raw_difficulty)
            Utils.persistent_store(f"GH2 {ctx.seed_name}", "difficulty", ctx.difficulty)
            ctx.four_star_checks = ctx.slot_data["four_star_checks"]
            ctx.five_star_checks = ctx.slot_data["five_star_checks"]
            ctx.all_notes = ctx.slot_data["all_notes"]
            ctx.venue_requirement = ctx.slot_data["venue_requirement"]
            while not ctx.game_initialized:
                try:

                    await pine_client.write_initial_state(songs_and_venues_by_pointer, ctx, songs_by_tier, venues_by_tier)


                    ctx.game_initialized = True
                except (OSError, asyncio.IncompleteReadError, ConnectionResetError):
                    await asyncio.sleep(1)
                    continue

async def process_received(ctx: GH2Context, cmd: str, args: dict):
    async with ctx.lock:
        if cmd == "ReceivedItems":
            if args["index"] == 0:
                ctx.items_received = []
            if args["index"] != ctx.highest_processed_item_index:
                await ctx.check_locations(ctx.locations_checked)
                await ctx.send_msgs([{"cmd": "Sync"}])
            for i in range(len(args["items"])):

                if args["index"] + i >= ctx.highest_processed_item_index:
                    item = args["items"][i].item
                    if item > 0xFF000000:
                        cash = await pine_client.read_uint32(ctx.cash_address)
                        cash += 550
                        await pine_client.write_uint32(ctx.cash_address, cash)
                    else:
                        song_or_venue = songs_and_venues_by_pointer[item]
                        if isinstance(song_or_venue, VenueData):
                            if ctx.venue_requirement:
                                for song in songs_by_tier[song_or_venue.tier]:
                                    if song in ctx.items_received:
                                        await pine_client.write_uint8(song.difficulty[ctx.difficulty] + 0x0E, 0x02)
                            if song_or_venue.name == "Bonus Tracks":
                                ctx.items_received.append(args["items"][i].item)
                                continue
                            if song_or_venue.name == "Stonehenge":
                                free_bird = songs_and_venues_by_pointer[0x00549e2c]
                                await pine_client.write_uint8(free_bird.difficulty[ctx.difficulty] + 0x0E, 0x0A)
                                await pine_client.write_uint8(song_or_venue.difficulty[ctx.difficulty]+0x0E, 0x06)
                                ctx.items_received.append(args["items"][i].item)
                                continue

                            await pine_client.write_uint8(song_or_venue.difficulty[ctx.difficulty] + 0x0E, 0x16)
                        elif ctx.venue_requirement and venues_by_tier[song_or_venue.tier] not in ctx.items_received:
                            continue
                        elif song_or_venue.tier == 9:
                            await pine_client.write_uint8(song_or_venue.difficulty[ctx.difficulty] + 0x0E, 0x07)
                        else:
                            await pine_client.write_uint8(song_or_venue.difficulty[ctx.difficulty]+0x0E, 0x02)

                    ctx.items_received.append(args["items"][i].item)
                elif args["index"] + i < ctx.highest_processed_item_index:
                    continue
            ctx.highest_processed_item_index = args["index"] + len(args["items"])
            if ctx.seed_name is not None:
                Utils.persistent_store(f"GH2 {ctx.seed_name}", "highest index", ctx.highest_processed_item_index)
                Utils.persistent_store(f"GH2 {ctx.seed_name}", "items received", ctx.items_received)





async def send_location_check(ctx: GH2Context, locations: list[int]):
    for location in locations:
        if location not in ctx.locations_checked:
            ctx.locations_checked.add(location)
    if ctx.server and not ctx.server.socket.closed:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations}])

async def memory_watcher(ctx: "GH2Context") -> None:
    while not ctx.exit_event.is_set():
        if ctx.server is None or not ctx.server.socket.open:
            await asyncio.sleep(1)
            continue
        if not pine_client.is_connected:
            logger.info("Attempting to connect to PCSX2...")
            await pine_client.connect()
            logger.info("PINE Connected!")
        if not ctx.server or ctx.server.socket.closed or not ctx.slot_data:
            await asyncio.sleep(1)
            continue
        if not ctx.game_initialized:
            game_id = await pine_client.read_id()

            if game_id != "Guitar Hero II":
                await asyncio.sleep(1)
                continue



        while ctx.game_initialized:
            try:
                read = await pine_client.read_uint32(ctx.scene_pointer)
                if read == ctx.winner_screen:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                if read == ctx.score_screen or read == ctx.encore_screen:
                    now_playing = await pine_client.read_uint32(ctx.current_song)
                    song = songs_and_venues_by_pointer[now_playing]
                    star_score = await pine_client.read_uint8(song.difficulty[ctx.difficulty]+0x0C)
                    star_checks = []
                    if star_score >= 0x03:
                        star_checks.append(0x03 << 24 | now_playing)
                    if star_score >= 0x04:
                        star_checks.append(0x04 << 24 | now_playing)
                    if star_score >= 0x05:
                        star_checks.append(0x05 << 24 | now_playing)
                    if star_score == 0x85:
                        star_checks.append(0x85 << 24 | now_playing)
                    await send_location_check(ctx, star_checks)


                    all_completed = True
                    for other_song in songs_by_tier[song.tier]:
                        value = await pine_client.read_uint8(other_song.difficulty[ctx.difficulty]+0x0E)
                        if value == 0:
                            all_completed = False
                            break
                    if all_completed:
                        await send_location_check(ctx, [0x05 << 24 | venues_by_tier[song.tier].pointer])

                await asyncio.sleep(1)
            except (OSError, asyncio.IncompleteReadError, ConnectionResetError):
                logger.warning("connection to PCSX2 lost")
                await pine_client.disconnect()
                await asyncio.sleep(1)

def main():
    Utils.init_logging("GH2Client", exception_logger="Client")

    async def _main():
        ctx = GH2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        asyncio.create_task(
            memory_watcher(ctx), name="GH2MemoryWatcher")

        if gui_enabled:
            ctx.run_gui()
        else:
            ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Guitar Hero II Client")
    args = parser.parse_args()
    main()