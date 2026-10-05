import struct
import asyncio
import logging

import os
import sys
from enum import IntEnum

from .addressdata import SongData, VenueData


logger = logging.getLogger("PINE")

class OpCode(IntEnum):
    MsgRead8 = 0
    MsgRead16 = 1
    MsgRead32 = 2
    MsgRead64 = 3
    MsgWrite8 = 4
    MsgWrite16 = 5
    MsgWrite32 = 6
    MsgWrite64 = 7
    MsgID = 11

PINE_UNIX_SOCKET = "XDG_RUNTIME_DIR/pcsx2.sock"



async def open_connection(host="127.0.0.1", port=28011, delay = 2.0):
    while True:
        try:
            if sys.platform != "win32" and os.path.exists(PINE_UNIX_SOCKET):
                reader, writer = await asyncio.open_unix_connection(
                    path=PINE_UNIX_SOCKET
                )
            else:
                reader, writer = await asyncio.open_connection(host, port)
            return reader, writer
        except (OSError, ConnectionRefusedError):

            await asyncio.sleep(delay)

class PineClient:

    def __init__(self):
        self.reader = None
        self.writer = None
        self._lock = asyncio.Lock()

    @property
    def is_connected(self):
        return self.reader is not None and self.writer is not None

    async def connect(self):
        self.reader, self.writer = await open_connection()

    async def disconnect(self):
       if self.is_connected:
           self.writer.close()
       self.reader, self.writer = None, None

    async def read_uint32(self, address: int) -> int:
        async with self._lock:
            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IBI", 9, OpCode.MsgRead32, address))
                await self.writer.drain()
                data = await self.reader.readexactly(9)
                header, status, value = struct.unpack("<IBI", data)
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}")
                return value
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def read_uint16(self, address: int) -> int:
        async with self._lock:
            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IBI", 9, OpCode.MsgRead16, address))
                await self.writer.drain()
                data = await self.reader.readexactly(7)
                header, status, value = struct.unpack("<IBH", data)
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}")
                return value
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def read_uint8(self, address: int) -> int:
        async with self._lock:

            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IBI", 9, OpCode.MsgRead8, address))
                await self.writer.drain()
                data = await self.reader.readexactly(6)
                response, status, value = struct.unpack("<IBB", data)
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}")

                return value
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def write_uint32(self, address: int, value: int) -> None:
        async with self._lock:
            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IBII", 13, OpCode.MsgWrite32, address, value))
                await self.writer.drain()
                response = await self.reader.readexactly(5)
                status = response[4]
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}")
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def write_uint16(self, address: int, value: int) -> None:
        async with self._lock:
            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IBIH", 11, OpCode.MsgWrite16, address, value))
                await self.writer.drain()
                response = await self.reader.readexactly(5)
                status = response[4]
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}")
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def write_uint8(self, address: int, value: int) -> None:
        async with self._lock:

            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                logger.info(f"PINE WRITE8: {address} <- {value}")
                self.writer.write(struct.pack("<IBIB", 10, OpCode.MsgWrite8, address, value))
                await self.writer.drain()
                response = await self.reader.readexactly(5)
                status = response[4]
                if status != 0:
                    raise RuntimeError(f"read failed with status {status}"
                                       f"{address}, {value}")

            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def read_id(self) -> str:
        async with self._lock:
            if not self.is_connected:
                raise ConnectionError("PINE not connected")
            try:
                self.writer.write(struct.pack("<IB", 5, OpCode.MsgID))
                await self.writer.drain()
                size = await self.reader.readexactly(4)
                total_size = struct.unpack("<I", size)[0]
                response = await self.reader.readexactly(total_size - 4)
                status = response[0]
                if status != 0:
                    return ""
                game_id = response[5:]
                return game_id.rstrip(b"\x00").decode("ascii", errors="ignore")
            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                await self.disconnect()
                raise

    async def write_initial_state(self, all_locations, ctx, songs_by_tier, venues_by_tier):
        for item in all_locations.values():
            if isinstance(item, VenueData):
                if item.name == "Bonus Tracks":
                    continue
                await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x04)
            elif item.tier == 9:
                await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x05)
            else:
                await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x00)
        item_ids = [network_item.item for network_item in ctx.items_received]
        for item in item_ids:
            if item > 0xFF000000:
                continue
            item = all_locations[item]
            if isinstance(item, VenueData):
                if ctx.venue_requirement:
                    for song in songs_by_tier[item.tier]:
                        if song.pointer in item_ids:
                            await self.write_uint8(song.difficulty[ctx.difficulty] + 0x0E, 0x02)
                if item.name == "Bonus Tracks":
                    continue
                elif item.name == "Stonehenge":
                    free_bird = all_locations[0x00549e2c]
                    await self.write_uint8(free_bird.difficulty[ctx.difficulty] + 0x0E, 0x0A)
                    await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x06)
                else:
                    await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x16)
            elif ctx.venue_requirement and venues_by_tier[item.tier] not in ctx.items_received:
                continue
            elif item.tier == 9:
                await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x07)
            else:
                await self.write_uint8(item.difficulty[ctx.difficulty] + 0x0E, 0x02)

    async def verify_locations(self, all_songs, ctx) -> list[int]:
        new_checks = []
        for song in all_songs:
            read = await self.read_uint8(song.difficulty[ctx.difficulty]+0x0C)
            if read == 0x00:
                continue
            if read >= 0x03:
                new_checks.append(0x03 << 24 | song.pointer)
            if read >= 0x04:
                new_checks.append(0x04 << 24 | song.pointer)
            if read >= 0x05:
                new_checks.append(0x05 << 24 | song.pointer)
            if read == 0x85:
                new_checks.append(0x85 << 24 | song.pointer)
        return new_checks