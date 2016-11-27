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
