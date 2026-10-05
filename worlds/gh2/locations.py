from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from .addressdata import ALL_SONGS, star_bytes, ALL_VENUES
from . import items


if TYPE_CHECKING:
    from .world import GH2World
    from .addressdata import SongData

class GH2Location(Location):
    game = "Guitar Hero II"

def get_location_names_with_ids()-> dict[str,int | None]:
    location_names: dict[str,int | None] = {}
    for song in ALL_SONGS:
        for score, byte in star_bytes.items():
            location_names[f"{song.name} - {score}"] = (byte << 24) | song.pointer
    for venue in ALL_VENUES:
        location_names[f"{venue.name} - All Songs Cleared"] = (0x05 << 24) |venue.pointer
    return location_names

location_name_to_id = get_location_names_with_ids()

def create_all_locations(world: GH2World) -> None:
    create_regular_locations(world)
    create_event_locations(world)


def create_regular_locations(world: GH2World) -> None:
    for song in ALL_SONGS:
        song_region = world.get_region(f"{song.name} Region")
        for location_name, value in location_name_to_id.items():
            if location_name.startswith(song.name):
                if location_name.endswith("100%") and world.options.all_notes == 0:
                    continue
                if location_name.endswith("5 Stars") and world.options.five_star_checks == 0:
                    continue
                if location_name.endswith("4 Stars") and world.options.four_star_checks == 0:
                    continue
                location = GH2Location(world.player, location_name, value, song_region)
                song_region.locations.append(location)
    for venue in ALL_VENUES:
        venue_region = world.get_region(f"{venue.name} Region")
        for location_name, value in location_name_to_id.items():
            if location_name.startswith(venue.name):
                location = GH2Location(world.player, location_name, value, venue_region)
                venue_region.locations.append(location)

def create_event_locations(world: GH2World) -> None:
    pass