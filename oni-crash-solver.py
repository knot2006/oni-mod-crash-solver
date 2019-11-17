#!/usr/bin/python3
import json, argparse, sys, shutil
from pathlib import Path
desc = "Oxygen Not Included Mod Crash Resolver"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-m", "--mod-json", dest='json', help="ONI mod json to read from")
# parser.add_argument("-e", "--executable", dest='exe', help="ONI executable for automatic testing")
# Defunct.
args = parser.parse_args()

if args.json == None:
    print("mod json required to operate. See help.")
    sys.exit(1)
elif not Path(args.json).is_file():
    print("`" + args.json + "` not a valid file.")
    sys.exit(1)


mod_json_path = Path(args.json)
mods_perm_off: int = 0
mods_test: list = []
mods_okay: list = []
data = dict()
mod_id: str = str()
mod_enabled: bool = bool()
with open(args.json, "r") as json_file:
    data = json.load(json_file)

for mod in data["mods"]:
    mod_id = mod["label"]["id"]
    mod_name = mod["label"]["title"]
    mod_enabled = mod["enabled"]
    if not mod_enabled:
        mods_perm_off += 1
    else:
        mods_test.append([mod_id, mod_enabled, mod_name])
    
print("Mods Disabled: " + str(mods_perm_off))
print("Mods Enabled: " + str(len(mods_test)))
print("This tool works by disabling half of your mods and asking if it crashed.\n\nPress Enter to continue.")
sys.stdin.readline()
backup_loc = str(mod_json_path.parent) +  "/mods.json.bak"
print("Saving backup at " + backup_loc)
shutil.copyfile(args.json, backup_loc, follow_symlinks=False)

def update_mod_json():
    mod_prt: int = 0
    for i, mod in enumerate(data["mods"]):
        mod_id = mod["label"]["id"]
        if mod_prt + 1 == len(mods_test):
            break
        if mod_id == mods_test[mod_prt][0]:
            data["mods"][i]["enabled"] = mods_test[mod_prt][1]
            data["mods"][i]["crash_count"] = 0
            mod_prt += 1
    with open(args.json, "w", encoding="utf8") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)
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
        
        while True:
            print("Wrote new mod list. Open and check if game crashes.\n\tCrashed? [Y]es/[N]o/[P]rint/[C]ommit/[A]bort")
            response = sys.stdin.readline()[0]
            response = response.lower()
            if response == "y" or response == "n" or response == "a" or response == "p" or response == "c":
                break
            else:
                print("Bad response.")

        if response == "a":
            print("Aborting. Copying from backup file at `" + backup_loc + "`")
            shutil.copyfile(backup_loc, args.json, follow_symlinks=False)
            sys.exit(0)
        elif response == "y":
            print("Flipping mods.")
            for i, c in enumerate(mods_test):
                mods_test[i][1] = not mods_test[i][1]
            update_mod_json()
        elif response == "n":
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
            
            
