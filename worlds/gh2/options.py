from Options import Toggle, Range, Choice, DeathLink, OptionSet, PerGameCommonOptions, OptionGroup, Removed
from dataclasses import dataclass

class Difficulty(Choice):
    """
    Select the difficulty level for checks.
    Only songs played at this difficulty will send checks.
    """
    display_name = "Difficulty"
    option_Medium = 0
    option_Hard = 1
    option_Expert = 2
    #Easy is excluded due to Free Bird not being available by default
    #I need to research this more to see if it can be used

class StartingMode(Choice):
    """
    Determines initial available checks.
    tier_songs: one random tier is unlocked and all songs in that tier are available.
    random_songs: one random tier is unlocked, with at least 1 song from that tier available.
    """
    display_name = "Starting Mode"
    option_tier_songs = 0
    option_random_songs = 1
    default = 0

class VenueRequirement(Toggle):
    """
    Determines how songs are unlocked.
    If selected, the venue item and the song item ar both required to play a song.
    Otherwise, just the song item is required.
    """
    display_name = "Song Unlock Mode"

class FourStarChecks(Toggle):
    """
    Set whether earning 4-stars on a song gives rewards.
    If selected, 3-star rewards are granted if 4-stars are earned and that setting is enabled.
    """
    display_name = "4-Star Rewards"

class FiveStarChecks(Toggle):
    """
    Set whether earning 5-stars on a song gives rewards.
    If selected, lower star rewards are granted if 5-stars are earned and those setting(s) are enabled.
    """
    display_name = "5-Star Rewards"

class AllNotes(Toggle):
    """
    Set whether hitting all notes on a song gives rewards.
    If selected, lower star rewards are granted if 100% of notes are hit and those setting(s) are enabled.
    """
    display_name = "100% Rewards"

@dataclass
class GH2Options(PerGameCommonOptions):
    difficulty: Difficulty
    starting_mode: StartingMode
    venue_requirement: VenueRequirement
    four_star_checks: FourStarChecks
    five_star_checks: FiveStarChecks
    all_notes: AllNotes
