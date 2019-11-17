#!/usr/bin/python3
import json, argparse, sys, shutil
from pathlib import Path

def prompt(valid_responses, prompt_text):
    while True:
        print(prompt_text)
        response = sys.stdin.readline()[0]
        response = response.lower()
        for p in valid_responses:
            if p == response:
                return response
        
        print("Bad response")


desc = "Oxygen Not Included Mod Crash Resolver"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-m", "--mod-json", dest="json", help="ONI mod json to read from")
parser.add_argument("-n", "--enable-mods", dest="enable_mods", action='store_true', help="enable all mods")
# parser.add_argument("-e", "--executable", dest='exe', help="ONI executable for automatic testing")
# Defunct.
args = parser.parse_args()

if args.json == None:
    if sys.platform == "linux" or platform == "linux2":
        # linux
        print("Detected Linux.")
        args.json = "~/.config/unity3d/Klei/Oxygen Not Included/mods/mods.json"
    elif sys.platform == "darwin":
        # OS X
        print("Detected OSX")
        args.json = "~/Library/Application Support/Klei/Oxygen Not Included/mods/mods.json"
    elif sys.platform == "win32":
        # Windows
        print("Detected Windows")
        args.json = "~\\Documents\\Klei\\OxygenNotIncluded\\mods\\mods.json"
    else:
        print("Unknown OS, " + sys.platform)
        print("mod json required to operate. See help.")
        sys.exit(1)

mod_json_path = Path(args.json).expanduser()

if not mod_json_path.is_file():
    print("`" + str(mod_json_path) + "` not a valid file.")
    sys.exit(1)

mods_perm_off: int = 0
mods_test: list = []
mods_okay: list = []
data = dict()
mod_id: str = str()
mod_enabled: bool = bool()
prompted: bool = False
enable_all: bool = args.enable_mods

with open(str(mod_json_path), "r") as json_file:
    data = json.load(json_file)

for mod in data["mods"]:
    mod_id = mod["label"]["id"]
    mod_name = mod["label"]["title"]
    mod_enabled = mod["enabled"]
    if not mod_enabled and not enable_all and not prompted:
        response = prompt(["y", "n"],"Some mods are disabled either by you or from a crash.\n\tEnable them? [Y]es/[N]o")
        if response == "y":
            enable_all = True
        
        prompted = True
        
    if not enable_all and not mod_enabled:
        mods_perm_off += 1
        continue
    
    mods_test.append([mod_id, mod_enabled, mod_name])
    
print("Mods Disabled: " + str(mods_perm_off))
print("Mods Enabled: " + str(len(mods_test)))
print("This tool works by disabling half of your mods and asking if it crashed.\n\nPress Enter to continue.")
sys.stdin.readline()
backup_loc = str(mod_json_path.parent) +  "/mods.json.bak"
print("Saving backup at " + backup_loc)
shutil.copyfile(str(mod_json_path), backup_loc, follow_symlinks=False)

def refresh_mod_json():
    with open(str(mod_json_path), "w", encoding="utf8") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)

def update_mod_json(soft=False):
    mod_prt: int = 0
    for i, mod in enumerate(data["mods"]):
        mod_id = mod["label"]["id"]
        if mod_prt == len(mods_test):
            break
        if mod_id == mods_test[mod_prt][0]:
            data["mods"][i]["enabled"] = mods_test[mod_prt][1]
            data["mods"][i]["crash_count"] = 0
            mod_prt += 1
    if not soft: refresh_mod_json()
    return

while True:
    print("Disabling half of mods.")
    mods_to_disable: int = round(len(mods_test)/2)
    print(str(mods_to_disable) + " mods to disable.")
    for i, c in enumerate(mods_test):
        if mods_to_disable == 0:
            break
        mods_test[i][1] = not mods_test[i][1]
        mods_to_disable -= 1
    
    update_mod_json()
    response: str = str()
    while True:
        if len(mods_test) == 1:
            print("Trouble mod located.")
            print("\t" + mods_test[0][2])
            sys.exit(0)
        
        response = prompt(["y", "n", "a", "p", "c", "r"], "Wrote new mod list. Open and check if game crashes.\n\tCrashed? [Y]es/[N]o/[P]rint/[C]ommit/[R]efresh/[A]bort")

        if response == "a":
            print("Aborting. Copying from backup file at `" + backup_loc + "`")
            shutil.copyfile(backup_loc, str(mod_json_path), follow_symlinks=False)
            sys.exit(0)
        elif response == "y" or response == "n":
            if response == "y":
                print("Flipping mods.")
                for i, c in enumerate(mods_test):
                    mods_test[i][1] = not mods_test[i][1]
                update_mod_json(soft=True)

            print("Recording current safe mods")
            mods_okay.extend(list(filter(lambda x: x[1] == True, mods_test)))
            mods_test = list(filter(lambda x: x[1] == False, mods_test))
            break
        elif response == "p":
            print("Printing current status...\n")
            print("--OKAY--")
            for mod in mods_okay:
                print("\t" + mod[2])
            print("--TESTING--")
            for mod in mods_test:
                print("\t" + ("DISABLED", "Enabled ")[mod[1]] + ": " + mod[2])
        elif response == "c":
            print("Changes committed.")
            sys.exit(0)
        elif response == "r":
            print("Refreshing file.")
            refresh_mod_json()
            
            
