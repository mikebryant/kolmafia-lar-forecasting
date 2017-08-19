#!/usr/bin/env python

import csv
import re
import sys

def sanitise_location(data, loc):
    loc = loc.lower()
    subtype = ""
    loc = re.sub(" \(delay[\s\w]*\)", "", loc)

    match = re.match("bathole \((.*)\)", loc)
    if match is not None:
        loc = match.groups()[0]

    match = re.match("pyramid \((.*)\)", loc)
    if match is not None:
        loc = match.groups()[0]

    loc = loc.replace("castle in the sky", "castle in the clouds in the sky")
    loc = loc.replace("hey deze arena", "infernal rackets backstage")
    loc = loc.replace("belilafs comedy club", "laugh floor")

    if loc.lower() not in data and "the " + loc.lower() not in data:
        print("Unknown location: " + loc)
        return ("", "")

    return (loc, subtype)


def sanitise_monster(data):
    data = data.lower()
    if data.endswith(" (good)"):
        return (data.replace(" (good)", ""), "good")
    if data.endswith(" (bad)"):
        return (data.replace(" (bad)", ""), "bad")
    return (data, "")

def convert(fobj):
    csvreader = csv.reader(fobj)

    with open("locations.txt") as locations_file:
        locations_data = [line.strip().lower() for line in locations_file.readlines()]
    with open("monsters.txt") as monsters_file:
        monsters = [line.strip().lower() for line in monsters_file.readlines()]

    locations = []
    for row in csvreader:
        if row[0] == 'Turn Count':
            locations = [sanitise_location(locations_data, loc) for loc in row[1:]]
        elif locations and row[0]:
            for loc, enc in zip(locations, row[1:]):
                if not enc or not loc:
                    continue
                monster_name, monster_subtype = sanitise_monster(enc)
                if monster_name in monsters:
                    combat = "true"
                    encounter_name = ""
                    encounter_subtype = monster_subtype
                else:
                    combat = "false"
                    encounter_name = enc
                    monster_name = "none"
                    encounter_subtype = ""
                yield (
                    loc[0], # Location
                    loc[1], # Zone special type
                    row[0], # Turn number
                    "0",# Delay
                    combat,
                    monster_name,
                    encounter_name,
                    encounter_subtype, # Encounter subtype
                )

def main(argv):
    if len(argv) < 3:
        print("""
            Usage: ./convert.py expanded.csv lar_encounter_data_v1.txt

            Download from https://docs.google.com/spreadsheets/d/1HQk1ANU-Uu4VrY5i7KDwPIrDQg37atFGIV1xra1nMfI/
            Use `File` -> `Download as` -> `Comma-separated values`
        """)
        sys.exit(1)
    else:
        with open(argv[1]) as file_in:
            with open(argv[2], "w") as file_out:
                for line in convert(file_in):
                    file_out.write("\t".join(line) + "\n")

if __name__ == "__main__":
    main(sys.argv)
