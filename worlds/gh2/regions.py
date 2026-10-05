from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from .addressdata import ALL_SONGS, ALL_VENUES

if TYPE_CHECKING:
    from world import GH2World
    from addressdata import SongData, VenueData

def create_and_connect_regions(world: GH2World) -> None:
    create_regions_vanilla(world)
    connect_regions_vanilla(world)

#named based on planned future behavior, which will require iso patching
def create_regions_vanilla(world: GH2World) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    venue_regions = []
    song_regions = []
    for venue in ALL_VENUES:
        venue_regions.append(Region(f"{venue.name} Region", world.player, world.multiworld))


    for song in ALL_SONGS:
        song_regions.append(Region(f"{song.name} Region", world.player, world.multiworld))

    world.multiworld.regions.append(menu)
    world.multiworld.regions += venue_regions
    world.multiworld.regions += song_regions

def connect_regions_vanilla(world: GH2World) -> None:
    menu = world.get_region("Menu")

    for venue in ALL_VENUES:
        venue_region = world.get_region(f"{venue.name} Region")
        menu.connect(venue_region, venue.name)
        for song in ALL_SONGS:
            song_region = world.get_region(f"{song.name} Region")
            if song.tier == venue.tier:
                venue_region.connect(song_region, song.name)