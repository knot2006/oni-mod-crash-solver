# Oxygen Not Included Mod Crash Solver

A simple Python script to do a binary test to pin-point what mod is causing Oxygen Not Included to crash.

## How to use

Run `./oni-crash-solver.py -h` to get help information, but the only argument is `-m` to select the `mods.json`.

Once a `mods.json` file is given, follow the instructions at prompt.

Print will list out the mods by name that are confirmed OK followed by the list of mods currently being tested by if enabled and name. Refresh will rewrite the JSON file, useful if ONI rewrote the file. Commit will exit the script and save the mods as is. Abort returns the file to it's original state.

## `mods.json`

`mods.json` is ONI's way to keep track of the state of mods.

On Linux, this location is `~/.config/unity3d/Klei/Oxygen Not Included/mods/mods.json`
