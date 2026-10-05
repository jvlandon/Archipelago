from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from . import locations
from .addressdata import ALL_SONGS, ALL_VENUES

has_stonehenge: Rule = Has("Stonehenge")

if TYPE_CHECKING:
    from .world import GH2World
    from .addressdata import SongData, VenueData

def set_all_rules(world: GH2World) -> None:

    set_entrance_rules(world)
    set_location_rules(world)
    set_completion_condition(world)

def set_entrance_rules(world: GH2World) -> None:
    venue_by_tier = {venue.tier: venue for venue in ALL_VENUES}
    tier_8_songs = [song for song in ALL_SONGS if song.tier == 8 and song.name != "Free Bird"]
    for song in ALL_SONGS:
        song_entrance = world.get_entrance(song.name)
        if world.options.venue_requirement:
            world.set_rule(song_entrance, HasAll(venue_by_tier[song.tier].name, song.name))
        else:
            world.set_rule(song_entrance, Has(song.name))
        if song.name == "Free Bird":
            world.set_rule(song_entrance, has_stonehenge)



def set_location_rules(world: GH2World) -> None:
    suffixes = ["3 Stars"]
    if world.options.four_star_checks:
        suffixes.append("4 Stars")
    if world.options.five_star_checks:
        suffixes.append("5 Stars")
    if world.options.all_notes:
        suffixes.append("100%")
    for song in ALL_SONGS:
        song_locations = [world.get_location(location) for location in locations.location_name_to_id.keys()
                          if location.startswith(song.name)
                          and location.endswith(tuple(suffixes))]
        for song_location in song_locations:
            world.set_rule(song_location, Has(song.name))
    for venue in ALL_VENUES:
        songs_by_tier = {venue.name: [song.name for song in ALL_SONGS if song.tier == venue.tier]}
        venue_songs = songs_by_tier.get(venue.name)
        venue_location = world.get_location(f"{venue.name} - All Songs Cleared")
        world.set_rule(venue_location, HasAll(
            venue_songs[0],
            venue_songs[1],
            venue_songs[2],
            venue_songs[3],
            venue_songs[4]))

def set_completion_condition(world: GH2World) -> None:
    tier_8_songs = [song for song in ALL_SONGS if song.tier == 8]
    has_t8 = HasAll(tier_8_songs[0].name,
            tier_8_songs[1].name,
            tier_8_songs[2].name,
            tier_8_songs[3].name)
    world.set_completion_rule(has_stonehenge & has_t8)