# Diablo 2 Hero Editing Hacks for 1.14

A script to hex-edit your single player save file in Diablo II for patches 1.13 and 1.14.
The script just requires python (2.7 or 3.x) and numpy, and it should work on Mac OSX or Windows.

Note: I've only tested it on 1.14d on Mac OSX with a character in Normal difficulty.

This code could also be a good starting point if you want to learn how to programmatically edit your D2 save file.

## Installation

    # Install requirements into a virtualenv
    mkvirtualenv diablo2
    pip install numpy

## Reset your stat points

The script re-enables your ability to reset stat and skill points through Akara in normal Act 1.
Make sure you've completed the Den of Evil first.

    # Activate the virtualenv
    workon diablo2
    # Run the script. It first creates a backup of your save file
    python d2hax.py --reset-stats --file "/Applications/Diablo II/Save/sohax.d2s"

## Unlock all waypoints

The script unlocks all waypoints in all difficulties. Currently untested for Nightmare and Hell.

    # Activate the virtualenv
    workon diablo2
    # Run the script. It first creates a backup of your save file
    python d2hax.py --unlock-waypoints --file "/Applications/Diablo II/Save/sohax.d2s"

## Reset the Hell's Forge quest

The script can reset your hell forge quest, so you can re-kill Hephasto and reap the rewards on the forge again.

    # Activate the virtualenv
    workon diablo2
    # Run the script. It first creates a backup of your save file
    python d2hax.py --reset-forge --difficulty 2 --file "/Applications/Diablo II/Save/sohax.d2s"

## How it works

The D2 single player save file is a mostly deterministic, binary serialization of some data structure that persists the state of your character and progress into the game.

So without knowing the individual fields of the struct, we can use trial and error to figure out what each part of the save file represents, byte by byte.
We modify some state in the game, look at the binary dump, and examine which bits changed, and what their offset was into the file.

We then can modify those bits and apply a checksum over the new binary data.
As a result, we've edited the data persisted in your character's save file.

