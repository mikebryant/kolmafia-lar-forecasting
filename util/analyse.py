#!/usr/bin/env python

from collections import defaultdict

MAX_TURN = 1

class Encounter(object):
    def __init__(self, location, turn, combat, name):
        self.location = location
        self.turn = turn
        self.combat = combat
        self.name = name

    def __str__(self):
        return "%s / %s" % (self.location, self.name)

    def __repr__(self):
        return str(self)

class Roll(object):
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __and__(self, other):
        return Roll(max(self.minimum, other.minimum), min(self.maximum, other.maximum))

    def __repr__(self):
        return "Roll(%s, %s)" % (self.minimum, self.maximum)

cncrolls = defaultdict(lambda: Roll(1, 100))

mobrolls = defaultdict(lambda: Roll(1, 100))

byturn = defaultdict(list)
byloc = defaultdict(list)
bylocturn = defaultdict(dict)

combat_percentages = {}

with open("../src/data/lar_combat_percentages.txt") as fobj:
    for line in fobj.readlines():
        line = line.strip()
        if not line:
            continue
        loc, cpc = line.split("\t")
        combat_percentages[loc] = int(cpc)

source_encounter_lists_tmp = defaultdict(dict)

with open("../src/data/lar_monster_orders.txt") as fobj:
    for line in fobj.readlines():
        line = line.strip()
        if not line:
            continue
        loc, i, name = line.split("\t")
        i = int(i)
        source_encounter_lists_tmp[loc][i] = name

source_encounter_lists = {}
for loc in source_encounter_lists_tmp:
    source_encounter_lists[loc] = [None] * (max(source_encounter_lists_tmp[loc].keys()) + 1)
    for k, v in source_encounter_lists_tmp[loc].items():
        source_encounter_lists[loc][k] = v
    if not all(source_encounter_lists[loc]):
        print "Datafile lar_monster_orders.txt issue:", source_encounter_lists[loc]

analysis_skip_locations = [
    "8-bit realm",
    "haunted pantry",
    "spooky forest",
]

def guess_combat_roll(enc):
    loc = enc.location
    if not combat:
        return Roll(1, 100)
    if loc not in source_encounter_lists:
        return Roll(1, 100)
    el = source_encounter_lists[loc]
    if enc.name not in el:
        print("%s/%s not in encounter list for %s!" % (enc.turn, enc.name, loc))
        return Roll(1, 100)
    i = el.index(enc.name)
    return Roll((i * 100)//len(el) + 1, ((i+1) * 100)//len(el))


with open("lar_encounter_data_v1.txt") as fobj:
    for line in fobj.readlines():
        params = line.split("\t")
        if not params:
            continue
        #print params
        #print params
        loc, subtype, turn, _, combat, monster_name, encounter_name = params[:7]
        if subtype:
            loc = loc + " / " + subtype
        combat = combat == "true"
        turn = int(turn)
        MAX_TURN = max(MAX_TURN, turn)
        if monster_name == "none":
            monster_name = ''
        enc = Encounter(loc, turn, combat, monster_name or encounter_name)
        byturn[turn].append(enc)
        byloc[loc].append(enc)
        bylocturn[loc][turn] = enc

        # Skip analysis of zones with delay, for now
        if loc in analysis_skip_locations:
            continue

        if loc in combat_percentages:
            cpc = combat_percentages[loc]
            if combat:
                cncrolls[turn] &= Roll(1, cpc)
                #cncrolls[turn].maximum = min(cncrolls[turn].maximum, cpc)
            else:
                cncrolls[turn] &= Roll(cpc + 1, 100)
                #cncrolls[turn].minimum = max(cncrolls[turn].minimum, cpc)

        mobrolls[turn] &= guess_combat_roll(enc)


# For determining encounter correspondences
for turn in range(1, MAX_TURN):
    try:
        #s = bylocturn["spooky forest"][turn]
        locs = [

            #"haunted billiards room",
            #"haunted pantry",
            #"hidden bowling alley",

            #"the dark heart of the woods",
            #"the dark neck of the woods",
            #"the dark elbow of the woods",
            "outskirts of cobb's knob",
            #"haunted laundry room",
            #"haunted kitchen",
            "black forest",
            #"spooky forest",
            #"8-bit realm / odd",
            #"8-bit realm / even",
        ]
        encs = [bylocturn[loc][turn] for loc in locs]
        if not all([enc.combat for enc in encs]):
            continue
        print(turn, [enc.name for enc in encs])
    except KeyError:
        pass

print "Errors:"
for turn in range(1, MAX_TURN):

    if cncrolls[turn].minimum >= cncrolls[turn].maximum:
        print "CNC", turn, cncrolls[turn]
        for enc in byturn[turn]:
            if enc.location in combat_percentages:
                print "\t", enc.location, enc.combat, combat_percentages[enc.location]

    if mobrolls[turn].minimum >= mobrolls[turn].maximum:
        print "M", turn, mobrolls[turn]
        for enc in byturn[turn]:
            if enc.combat:
                print "\t", enc.location, enc.name, guess_combat_roll(enc)
print "End of Errors"

with open("../src/data/lar_cnc_rolls.txt", "w") as fobj:
    for turn in range(1, MAX_TURN):
        roll = cncrolls[turn]
        if roll.minimum >= roll.maximum:
            # Don't record the data if it's broken
            roll = Roll(1, 100)
        fobj.write("%s\t%s\t%s\n" % (turn, roll.minimum, roll.maximum))

with open("../src/data/lar_monster_rolls.txt", "w") as fobj:
    for turn in range(1, MAX_TURN):
        roll = mobrolls[turn]
        if roll.minimum >= roll.maximum:
            # Don't record the data if it's broken
            roll = Roll(1, 100)
        # Turn, roll_number (so we can add the rerolls on rejections in future), min, max
        fobj.write("%s\t%s\t%s\t%s\n" % (turn, 0, roll.minimum, roll.maximum))
