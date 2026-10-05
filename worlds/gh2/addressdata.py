from dataclasses import dataclass
from enum import Enum
from typing import Any


# Offsets where score for respective song data is stored
expert_song_addresses = {
    "Shout at the Devil": 0x00AAB610,
    "Mother": 0x00AAB620,
    "Surrender": 0x00AAB630,
    "Woman": 0x00AAB640,
    "Tonight I'm Gonna Rock You Tonight": 0x00AAB650,
    "Strutter": 0x00AAB660,
    "Heart-Shaped Box": 0x00AAB670,
    "Message in a Bottle": 0x00AAB680,
    "You Really Got Me": 0x00AAB690,
    "Carry On Wayward Son": 0x00AAB6A0,
    "Monkey Wrench": 0x00AAB6B0,
    "Them Bones": 0x00AAB6C0,
    "Search and Destroy": 0x00AAB6D0,
    "Tattooed Love Boys": 0x00AAB6E0,
    "War Pigs": 0x00AAB6F0,
    "Cherry Pie": 0x00AAB700,
    "Who Was In My Room Last Night?": 0x00AAB710,
    "Girlfriend": 0x00AAB720,
    "Can't You Hear Me Knockin'": 0x00AAB730,
    "Sweet Child O' Mine": 0x00AAB740,
    "Killing in the Name": 0x00AAB750,
    "John the Fisherman": 0x00AAB760,
    "Freya": 0x00AAB770,
    "Bad Reputation": 0x00AAB780,
    "Last Child": 0x00AAB790,
    "Crazy on You": 0x00AAB7A0,
    "Trippin' on a Hole in a Paper Heart": 0x00AAB7B0,
    "Rock This Town": 0x00AAB7C0,
    "Jessica": 0x00AAB7D0,
    "Stop": 0x00AAB7E0,
    "Madhouse": 0x00AAB7F0,
    "Carry Me Home": 0x00AAB800,
    "Laid to Rest": 0x00AAB810,
    "Psychobilly Freakout": 0x00AAB820,
    "YYZ": 0x00AAB830,
    "Beast and the Harlot": 0x00AAB840,
    "Institutionalized": 0x00AAB850,
    "Misirlou": 0x00AAB860,
    "Hangar 18": 0x00AAB870,
    "Free Bird": 0x00AAB880,
    "Raw Dog": 0x00AAB890,
    "Arterial Black": 0x00AAB8A0,
    "Collide": 0x00AAB8B0,
    "Elephant Bones": 0x00AAB8C0,
    "Fall of Pangaea": 0x00AAB8D0,
    "FTK": 0x00AAB8E0,
    "Gemini": 0x00AAB8F0,
    "Push Push (Lady Lightning)": 0x00AAB900,
    "Laughtrack": 0x00AAB910,
    "Less Talk More Rokk": 0x00AAB920,
    "Jordan": 0x00AAB930,
    "Mr Fix It": 0x00AAB940,
    "The New Black": 0x00AAB960,
    "One for the Road": 0x00AAB970,
    "Parasite": 0x00AAB980,
    "Radium Eyes": 0x00AAB990,
    "Red Lottery": 0x00AAB9A0,
    "Six": 0x00AAB9B0,
    "Soy Bomb": 0x00AAB9C0,
    "The Light That Blinds": 0x00AAB9D0,
    "Thunderhorse": 0x00AAB9E0,
    "Trogdor": 0x00AAB9F0 ,
    "X-Stream": 0x00AABA00,
    "Yes We Can": 0x00AABA10,
}

hard_song_addresses = {
    "Shout at the Devil": 0x00AAE5C0,
    "Mother": 0x00AAE5D0,
    "Surrender": 0x00AAE5E0,
    "Woman": 0x00AAE5F0,
    "Tonight I'm Gonna Rock You Tonight": 0x00AAE600,
    "Strutter": 0x00AAE610,
    "Heart-Shaped Box": 0x00AAE620,
    "Message in a Bottle": 0x00AAE630,
    "You Really Got Me": 0x00AAE640,
    "Carry On Wayward Son": 0x00AAE650,
    "Monkey Wrench": 0x00AAE660,
    "Them Bones": 0x00AAE670,
    "Search and Destroy": 0x00AAE680,
    "Tattooed Love Boys": 0x00AAE690,
    "War Pigs": 0x00AAE6A0,
    "Cherry Pie": 0x00AAE6B0,
    "Who Was In My Room Last Night?": 0x00AAE6C0,
    "Girlfriend": 0x00AAE6D0,
    "Can't You Hear Me Knockin'": 0x00AAE6E0,
    "Sweet Child O' Mine": 0x00AAE6F0,
    "Killing in the Name": 0x00AAE700,
    "John the Fisherman": 0x00AAE710,
    "Freya": 0x00AAE720,
    "Bad Reputation": 0x00AAE730,
    "Last Child": 0x00AAE740,
    "Crazy on You": 0x00AAE750,
    "Trippin' on a Hole in a Paper Heart": 0x00AAE760,
    "Rock This Town": 0x00AAE770,
    "Jessica": 0x00AAE780,
    "Stop": 0x00AAE790,
    "Madhouse": 0x00AAE7A0,
    "Carry Me Home": 0x00AAE7B0,
    "Laid to Rest": 0x00AAE7C0,
    "Psychobilly Freakout": 0x00AAE7D0,
    "YYZ": 0x00AAE7E0,
    "Beast and the Harlot": 0x00AAE7F0,
    "Institutionalized": 0x00AAE800,
    "Misirlou": 0x00AAE810,
    "Hangar 18": 0x00AAE820,
    "Free Bird": 0x00AAE830,
    "Raw Dog": 0x00AAE840,
    "Arterial Black": 0x00AAE850,
    "Collide": 0x00AAE860,
    "Elephant Bones": 0x00AAE870,
    "Fall of Pangaea": 0x00AAE880,
    "FTK": 0x00AAE890,
    "Gemini": 0x00AAE8A0,
    "Push Push (Lady Lightning)": 0x00AAE8B0,
    "Laughtrack": 0x00AAE8C0,
    "Less Talk More Rokk": 0x00AAE8D0,
    "Jordan": 0x00AAE8E0,
    "Mr Fix It": 0x00AAE8F0,
    "The New Black": 0x00AAE900,
    "One for the Road": 0x00AAE910,
    "Parasite": 0x00AAE920,
    "Radium Eyes": 0x00AAE930,
    "Red Lottery": 0x00AAE940,
    "Six": 0x00AAE950,
    "Soy Bomb": 0x00AAE960,
    "The Light That Blinds": 0x00AAE970,
    "Thunderhorse": 0x00AAE980,
    "Trogdor": 0x00AAE990 ,
    "X-Stream": 0x00AAE9A0,
    "Yes We Can": 0x00AAE9B0,
}

medium_song_addresses = {
    "Shout at the Devil": 0x00AAE120,
    "Mother": 0x00AAE130,
    "Surrender": 0x00AAE140,
    "Woman": 0x00AAE150,
    "Tonight I'm Gonna Rock You Tonight": 0x00AAE160,
    "Strutter": 0x00AAE170,
    "Heart-Shaped Box": 0x00AAE180,
    "Message in a Bottle": 0x00AAE190,
    "You Really Got Me": 0x00AAE1A0,
    "Carry On Wayward Son": 0x00AAE1B0,
    "Monkey Wrench": 0x00AAE1C0,
    "Them Bones": 0x00AAE1D0,
    "Search and Destroy": 0x00AAE1E0,
    "Tattooed Love Boys": 0x00AAE1F0,
    "War Pigs": 0x00AAE200,
    "Cherry Pie": 0x00AAE210,
    "Who Was In My Room Last Night?": 0x00AAE220,
    "Girlfriend": 0x00AAE230,
    "Can't You Hear Me Knockin'": 0x00AAE240,
    "Sweet Child O' Mine": 0x00AAE250,
    "Killing in the Name": 0x00AAE260,
    "John the Fisherman": 0x00AAE270,
    "Freya": 0x00AAE280,
    "Bad Reputation": 0x00AAE290,
    "Last Child": 0x00AAE2A0,
    "Crazy on You": 0x00AAE2B0,
    "Trippin' on a Hole in a Paper Heart":0x00AAE2C0 ,
    "Rock This Town": 0x00AAE2D0,
    "Jessica": 0x00AAE2E0,
    "Stop": 0x00AAE2F0,
    "Madhouse": 0x00AAE300,
    "Carry Me Home": 0x00AAE310,
    "Laid to Rest": 0x00AAE320,
    "Psychobilly Freakout": 0x00AAE330,
    "YYZ": 0x00AAE340,
    "Beast and the Harlot":0x00AAE350,
    "Institutionalized": 0x00AAE360,
    "Misirlou": 0x00AAE370,
    "Hangar 18": 0x00AAE380,
    "Free Bird": 0x00AAE390,
    "Raw Dog": 0x00AAE3A0,
    "Arterial Black": 0x00AAE3B0,
    "Collide": 0x00AAE3C0,
    "Elephant Bones": 0x00AAE3D0,
    "Fall of Pangaea": 0x00AAE3E0,
    "FTK": 0x00AAE3F0,
    "Gemini": 0x00AAE400,
    "Push Push (Lady Lightning)": 0x00AAE410,
    "Laughtrack": 0x00AAE420,
    "Less Talk More Rokk": 0x00AAE430,
    "Jordan": 0x00AAE440,
    "Mr Fix It": 0x00AAE450,
    "The New Black": 0x00AAE460,
    "One for the Road": 0x00AAE470,
    "Parasite": 0x00AAE480,
    "Radium Eyes": 0x00AAE490,
    "Red Lottery": 0x00AAE4A0,
    "Six": 0x00AAE4B0,
    "Soy Bomb": 0x00AAE4C0,
    "The Light That Blinds": 0x00AAE4D0,
    "Thunderhorse": 0x00AAE4E0,
    "Trogdor": 0x00AAE4F0 ,
    "X-Stream": 0x00AAE500,
    "Yes We Can": 0x00AAE510,
}

# Likewise, offsets for venue unlocks for each difficulty
# Bonus Tracks gets a fake address, since it's not actually a venue
expert_venue_addresses = {
    "Battle of the Bands": 0x00AAB590,
    "The Rat Cellar": 0x00AAB5A0,
    "Blackout Bar": 0x00AAB5B0,
    "Red Octane Club": 0x00AAB5C0,
    "Rock City Theater": 0x00AAB5D0,
    "Vans Warped Tour": 0x00AAB5E0,
    "The Arena": 0x00AAB5F0,
    "Stonehenge": 0x00AAB600,
    "Bonus Tracks": 0x00FF0005
}

hard_venue_addresses = {
    "Battle of the Bands": 0x00AAE540,
    "The Rat Cellar": 0x00AAE550,
    "Blackout Bar": 0x00AAE560,
    "Red Octane Club": 0x00AAE570,
    "Rock City Theater": 0x00AAE580,
    "Vans Warped Tour": 0x00AAE590,
    "The Arena": 0x00AAE5A0,
    "Stonehenge": 0x00AAE5B0,
    "Bonus Tracks": 0x00FF0008,
}

medium_venue_addresses = {
    "Battle of the Bands":0x00AAE0A0,
    "The Rat Cellar": 0x00AAE0B0,
    "Blackout Bar": 0x00AAE0C0,
    "Red Octane Club": 0x00AAE0D0,
    "Rock City Theater": 0x00AAE0E0,
    "Vans Warped Tour": 0x00AAE0F0,
    "The Arena": 0x00AAE100,
    "Stonehenge": 0x00AAE110,
    "Bonus Tracks": 0x00FF000C,
}

# Pointers for IDs that list the venues out in ASCII for the game's internal use.
# Once again, Bonus Track pointer is invented for the APWorld's benefit
venue_pointer_addresses = {
    "Battle of the Bands": 0x00548760,
    "The Rat Cellar": 0x00549BB7,
    "Blackout Bar": 0x00549BCC,
    "Red Octane Club": 0x00549BDE,
    "Rock City Theater": 0x00549BF1,
    "Vans Warped Tour": 0x00549C05,
    "The Arena": 0x00549C17,
    "Stonehenge": 0x00549C2A,
    "Bonus Tracks": 0x00FF0000
}

# ASCII pointers for songs
song_pointer_addresses = {
    "Shout at the Devil": 0x00552e43 ,
    "Mother": 0x00552e05,
    "Surrender": 0x00552e5c,
    "Woman": 0x00552eb2,
    "Tonight I'm Gonna Rock You Tonight": 0x00548776,
    "Strutter": 0x00552e53,
    "Heart-Shaped Box": 0x00552d80,
    "Message in a Bottle": 0x00552deb,
    "You Really Got Me": 0x00552eb8,
    "Carry On Wayward Son": 0x00552d42,
    "Monkey Wrench": 0x00552e0c,
    "Them Bones": 0x00552e82,
    "Search and Destroy": 0x00552e32,
    "Tattooed Love Boys": 0x00552e71,
    "War Pigs": 0x00552e9b,
    "Cherry Pie": 0x00552d51,
    "Who Was In My Room Last Night?": 0x00552ea3,
    "Girlfriend": 0x00552d6c,
    "Can't You Hear Me Knockin'": 0x00552d28,
    "Sweet Child O' Mine": 0x00552e66,
    "Killing in the Name": 0x00552dba,
    "John the Fisherman": 0x00552dA9,
    "Freya": 0x00552d66,
    "Bad Reputation": 0x00552d08,
    "Last Child": 0x00552dd8,
    "Crazy on You": 0x00552d5B,
    "Trippin' on a Hole in a Paper Heart": 0x00552e8c,
    "Rock This Town": 0x00552e25,
    "Jessica": 0x00552da1,
    "Stop": 0x00546a0e,
    "Madhouse": 0x00552de2,
    "Carry Me Home": 0x00552d36,
    "Laid to Rest": 0x00552dcd,
    "Psychobilly Freakout": 0x00552e19,
    "YYZ": 0x00552ec7,
    "Beast and the Harlot": 0x00552d16,
    "Institutionalized": 0x00552d8f,
    "Misirlou": 0x00552dfc,
    "Hangar 18": 0x00552d77,
    "Free Bird": 0x00549e2c,
    "Raw Dog": 0x00552f76,
    "Arterial Black": 0x00552ecb,
    "Collide": 0x00552ed9,
    "Elephant Bones": 0x00552ee1,
    "Fall of Pangaea": 0x00552eef,
    "FTK": 0x00552efc,
    "Gemini": 0x00552f00,
    "Push Push (Lady Lightning)": 0x00552f0e,
    "Laughtrack": 0x00552f1c,
    "Less Talk More Rokk": 0x00552f27,
    "Jordan": 0x00552f07,
    "Mr Fix It": 0x00552f38,
    "The New Black": 0x00552f40,
    "One for the Road": 0x00552f49,
    "Parasite": 0x00552f57,
    "Radium Eyes": 0x00552f60,
    "Red Lottery": 0x00552f6b,
    "Six": 0x00552f7d,
    "Soy Bomb": 0x00552f81,
    "The Light That Blinds": 0x00552f89,
    "Thunderhorse": 0x00549663,
    "Trogdor": 0x00549670,
    "X-Stream": 0x00552f9c,
    "Yes We Can": 0x00552fa4,
}

# Flags for respective star thresholds
star_bytes = {
    "3 Stars": 0x03,
    "4 Stars": 0x04,
    "5 Stars": 0x05,
    "100%": 0x85,
}

songs_by_venue = {
    "Battle of the Bands": [
        "Shout at the Devil",
        "Mother",
        "Surrender",
        "Woman",
        "Tonight I'm Gonna Rock You Tonight",
    ],
    "The Rat Cellar": [
        "Strutter",
        "Heart-Shaped Box",
        "Message in a Bottle",
        "You Really Got Me",
        "Carry On Wayward Son"
    ],
    "Blackout Bar": [
        "Monkey Wrench",
        "Them Bones",
        "Search and Destroy",
        "Tattooed Love Boys",
        "War Pigs"
    ],
    "Red Octane Club": [
        "Cherry Pie",
        "Who Was In My Room Last Night?",
        "Girlfriend",
        "Can't You Hear Me Knockin'",
        "Sweet Child O' Mine"
    ],
    "Rock City Theater": [
        "Killing in the Name",
        "John the Fisherman",
        "Freya",
        "Bad Reputation",
        "Last Child"
    ],
    "Vans Warped Tour": [
        "Crazy on You",
        "Trippin' on a Hole in a Paper Heart",
        "Rock This Town",
        "Jessica",
        "Stop"
    ],
    "The Arena": [
        "Madhouse",
        "Carry Me Home",
        "Laid to Rest",
        "Psychobilly Freakout",
        "YYZ",
    ],
    "Stonehenge": [
        "Beast and the Harlot",
        "Institutionalized",
        "Misirlou",
        "Hangar 18",
        "Free Bird"
    ],
    "Bonus Tracks": [
        "Arterial Black",
        "Collide",
        "Elephant Bones",
        "Fall of Pangaea",
        "FTK",
        "Gemini",
        "Jordan",
        "Laughtrack",
        "Less Talk More Rokk",
        "Mr Fix It",
        "One for the Road",
        "Parasite",
        "Push Push (Lady Lightning)",
        "Radium Eyes",
        "Raw Dog",
        "Red Lottery",
        "Six",
        "Soy Bomb",
        "The Light That Blinds",
        "The New Black",
        "Thunderhorse",
        "Trogdor",
        "X-Stream",
        "Yes We Can",
    ]
}

class Difficulty(Enum):
    MEDIUM = 0
    HARD = 1
    EXPERT = 2

@dataclass(frozen=True)
class SongData:
    name: str
    tier: int
    pointer: int
    difficulty: dict[Difficulty, int]

    def get_location_id(self, star_byte):
        return star_byte << 24 | self.pointer

@dataclass(frozen=True)
class VenueData:
    name: str
    tier: int
    pointer: int
    difficulty: dict[Difficulty, int]

def create_songs_and_venues():
    all_songs: list[SongData] = []
    all_venues:  list[VenueData] = []
    for tier_index, (venue_name, song_names) in enumerate(songs_by_venue.items(), start=1):
        venue_pointer = venue_pointer_addresses[venue_name]
        all_venues.append(VenueData(
            name=venue_name,
            tier=tier_index,
            pointer=venue_pointer,
            difficulty={
                Difficulty.MEDIUM: medium_venue_addresses[venue_name],
                Difficulty.HARD: hard_venue_addresses[venue_name],
                Difficulty.EXPERT: expert_venue_addresses[venue_name],
            }
        ))
        for song_name in song_names:
            pointer = song_pointer_addresses[song_name]
            all_songs.append(SongData(name=song_name,
                                      tier=tier_index, 
                                      pointer=pointer, 
                                      difficulty={
                                          Difficulty.MEDIUM: medium_song_addresses[song_name],
                                          Difficulty.HARD: hard_song_addresses[song_name],
                                          Difficulty.EXPERT: expert_song_addresses[song_name],
                                      },))
    return all_songs, all_venues

ALL_SONGS, ALL_VENUES = create_songs_and_venues()

songs_by_tier = {}
for song in ALL_SONGS:
    songs_by_tier.setdefault(song.tier, []).append(song)

songs_and_venues_by_pointer = {item.pointer: item for item in ALL_SONGS + ALL_VENUES}
songs_and_venues_by_name = {item.name: item for item in ALL_SONGS + ALL_VENUES}
venues_by_tier = {venue.tier: venue for venue in ALL_VENUES}
