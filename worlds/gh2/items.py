from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .addressdata import ALL_SONGS, ALL_VENUES

if TYPE_CHECKING:
    from world import GH2World

class GH2Item(Item):
    game = "Guitar Hero II"

ITEM_NAME_TO_ID = {}
item_classification: dict[str, ItemClassification] = {}

filler: dict[str, int] = {
    "$550": 0xFF000226
}


for song in ALL_SONGS:
    ITEM_NAME_TO_ID[song.name] = song.pointer
    item_classification[song.name] = ItemClassification.progression

for venue in ALL_VENUES:
    ITEM_NAME_TO_ID[venue.name] = venue.pointer
    item_classification[venue.name] = ItemClassification.progression

for name, item_id in filler.items():
    ITEM_NAME_TO_ID[name] = item_id
    item_classification[name] = ItemClassification.filler

