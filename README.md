# Oxygen Not Included Mod Crash Solver

A simple Python script to do a binary test to pin-point what mod is causing Oxygen Not Included to crash.

## How to use

Clone this repository to somewhere on your system either by using `git clone $this_repository` or downloading the repository as a zip.

Run `./oni-crash-solver.py -h` or `python3 ./oni-crash-solver.py -h` to get help information, but the only required argument is `-m` to select the `mods.json` to work on.

Once a `mods.json` file is given, follow the instructions at prompt. If an exception occurs, a backup file is present next to the `mods.json` file.

**Print** will list out the mods by name that are confirmed OK followed by the list of mods currently being tested by if enabled/disabled and name.

**Refresh** will rewrite the JSON file, useful if ONI rewrote the file after crashing from unrelated means (system instability).

**Commit** will exit the script and save the mods as is.

**Abort** returns the file to it's original state.

## `mods.json`

`mods.json` is ONI's way to keep track of the state of mods.

On Linux, this location is `~/.config/unity3d/Klei/Oxygen Not Included/mods/mods.json`
