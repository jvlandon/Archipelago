# Guitar Hero II (PS2) AP World

Archipelago implementation for Guitar Hero II for the PS2. This AP world uses PCSX2's PINE interface to facilitate communication between the client and the emulator.

## Goal

Complete Free Bird at Stonehenge in Career mode on the difficulty chosen in the player's settings.

## What's Randomized

All songs and venues are shuffled into the item pools. Checks are awarded based on song performance (3, 4, and 5 Stars, plus 100% of notes). All of these apart from
three stars can be toggled in the player's settings.

Filler items consist solely of cash at this time. Bonus songs may be purchased in the shop but they are also in the item pool, so purchasing them is considered
out of logic, and may not persist over game reloads. Do so at your own risk. This is admittedly an odd quirk, but should not exist long term.

## Setup and Warnings

A full setup guide can be found in this repo, but two things require emphasis:

1. **Start each seed with a fresh save.** Not creating a new save file may cause issues, including checks being sent out before they are meant to.

2. **Calibrate your lag.** Guitar Hero II was designed for CRTs, and modern screens create significant lag for the games (to say nothing of emulator lag).
Always calibrate your lag after initializing a new file.

## Known issues

- There have been a few locking issues with the client. I think this is fixed, but generally disconnecting/reconnecting is enough to get it to behave
- Encores sometimes occur for tiers if the criteria are met. This could give access to songs out of logic, though I believe it would just be limited to the
encore song itself. I have to do more testing/research to fully stymie this. For now, I recommend not playing an encore if it comes up.
- Of note to the above issue: Free Bird *will* trigger an encore (by design), but playing it as an encore at a venue other than Stonehenge will crash the game, and you will neither
complete the seed, Free Bird, or the song you played prior.
- The Blackout Bar venue is always available. This doesn't affect the item pool or randomization, it's just the default venue in case you play 
Quick Play and don't have anything unlocked.
- Unlocking later tier songs will push the song list lower than the screen, meaning some of the bonus tracks may not be viewable. 

## To-Do list

- Shop shuffle
- alternate goal(s)
- Rocks the 80s
