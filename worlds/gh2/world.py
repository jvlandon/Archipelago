from typing import Any, Mapping

from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from .addressdata import ALL_SONGS, ALL_VENUES, songs_by_venue, VenueData, SongData
from _collections_abc import Mapping
from . import options as gh2_options
from . import items, locations, regions, rules




class GH2World(World):
    """

    """

    game = "Guitar Hero II"

    options_dataclass = gh2_options.GH2Options
    options: gh2_options.GH2Options

    location_name_to_id = locations.location_name_to_id
    item_name_to_id = items.ITEM_NAME_TO_ID


    origin_region_name = "Menu"

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        itempool: list[items.GH2Item] = []
        starting_venue, starting_songs = self.choose_starting_items()
        self.multiworld.push_precollected(self.create_item(starting_venue.name))
        for song in starting_songs:
            self.multiworld.push_precollected(self.create_item(song))
        for song in ALL_SONGS:
            if song.name in starting_songs:
                continue
            if song.name == "Free Bird":
                continue
            itempool.append(self.create_item(song.name))
        for venue in ALL_VENUES:
            if venue.name == starting_venue.name:
                continue
            itempool.append(self.create_item(venue.name))
        number_of_items = len(itempool)
        unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        needed_filler = unfilled_locations - number_of_items
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(needed_filler)]
        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(items.filler.keys()))

    def create_item(self, name: str) -> items.GH2Item:
        return items.GH2Item(name=name,
                       classification=items.item_classification[name],
                       code=self.item_name_to_id[name],
                       player=self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "difficulty", "venue_requirement", "four_star_checks", "five_star_checks", "all_notes"
        )
    def choose_starting_items(self) -> tuple[VenueData, list[str]]:
        starting_venue = self.random.choice(ALL_VENUES[:7])
        venue_list = songs_by_venue[starting_venue.name]
        if self.options.starting_mode == 0:
            starting_songs: list[str] = []
            for song in ALL_SONGS:
                if song.name in venue_list:
                    starting_songs.append(song.name)
                    if len(starting_songs) == 4:
                        break
        elif self.options.starting_mode == 1:
            guaranteed_song = self.random.choice(venue_list[:4])

            starting_songs: list[str] = [guaranteed_song]
            while len(starting_songs) < 4:
                song = self.random.choice(ALL_SONGS)
                if song.name in starting_songs:
                    continue
                if song.tier == 8:
                    continue
                starting_songs.append(song.name)
        return starting_venue, starting_songs