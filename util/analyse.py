#!/usr/bin/env python

from collections import defaultdict
import sys

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
ncrolls = defaultdict(lambda: Roll(1, 100))

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

source_monster_lists_tmp = defaultdict(dict)

with open("../src/data/lar_monster_orders.txt") as fobj:
    for line in fobj.readlines():
        line = line.strip()
        if not line:
            continue
        loc, i, name = line.split("\t")
        i = int(i)
        source_monster_lists_tmp[loc][i] = name

source_monster_lists = {}
for loc in source_monster_lists_tmp:
    source_monster_lists[loc] = [None] * (max(source_monster_lists_tmp[loc].keys()) + 1)
    for k, v in source_monster_lists_tmp[loc].items():
        source_monster_lists[loc][k] = v
    if not all(source_monster_lists[loc]):
        print "Datafile lar_monster_orders.txt issue:", source_monster_lists[loc]

source_noncombat_lists_tmp = defaultdict(dict)

with open("../src/data/lar_noncombat_orders.txt") as fobj:
    for line in fobj.readlines():
        line = line.strip()
        if not line:
            continue
        loc, i, name = line.split("\t")
        i = int(i)
        source_noncombat_lists_tmp[loc][i] = name

source_noncombat_lists = {}
for loc in source_noncombat_lists_tmp:
    source_noncombat_lists[loc] = [None] * (max(source_noncombat_lists_tmp[loc].keys()) + 1)
    for k, v in source_noncombat_lists_tmp[loc].items():
        source_noncombat_lists[loc][k] = v
    if not all(source_noncombat_lists[loc]):
        print "Datafile lar_noncombat_orders.txt issue:", source_noncombat_lists[loc]

cnc_analysis_skip_locations = [
    "black forest", # Has all of the map superlikelies.
    "infernal rackets backstage", # Forced NCs
    "spooky forest", # aboreal superlikely
    "the spooky forest",
]

monster_analysis_skip_locations = [
    "8-bit realm", # Odd/even rejection
    "the haunted pantry", # Odd/even rejection
    "the sleazy back alley", #Odd/even rejection
    "the haunted billiards room", #Several odd entries on the spreadsheet
    # All kinds of stuff with the various monsters being shoved in here
    "the hidden park",
    "the hidden apartment building",
    "the hidden office building",
    "the hidden bowling alley",
    "the hidden hospital",
    "the batrat and ratbat burrow",
]

noncombat_analysis_skip_locations = [
]

def guess_combat_roll(enc):
    loc = enc.location
    if not enc.combat:
        return Roll(1, 100)
    if loc not in source_monster_lists:
        return Roll(1, 100)
    el = source_monster_lists[loc]
    if enc.name not in el:
        print("%s/%s not in encounter list for %s!" % (enc.turn, enc.name, loc))
        return Roll(1, 100)
    i = el.index(enc.name)
    return Roll((i * 100)//len(el) + 1, ((i+1) * 100)//len(el))

def guess_noncombat_roll(enc):
    loc = enc.location
    if enc.combat:
        return Roll(1, 100)
    if loc not in source_noncombat_lists:
        return Roll(1, 100)
    el = source_noncombat_lists[loc]
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

        if enc.name not in source_monster_lists.get(loc, []) + source_noncombat_lists.get(loc, []):
            if loc not in ["8-bit realm / odd", "8-bit realm / even"]:
                print("%s/%s not in encounter list for %s!" % (enc.turn, enc.name, loc))

        # Skip analysis of zones with delay, for now
        if loc not in cnc_analysis_skip_locations:
            if loc in combat_percentages:
                cpc = combat_percentages[loc]
                if cpc != 100:
                    if combat:
                        cncrolls[turn] &= Roll(1, cpc)
                        #cncrolls[turn].maximum = min(cncrolls[turn].maximum, cpc)
                    else:
                        cncrolls[turn] &= Roll(cpc + 1, 100)
                        #cncrolls[turn].minimum = max(cncrolls[turn].minimum, cpc)

        if loc not in monster_analysis_skip_locations:
            mobrolls[turn] &= guess_combat_roll(enc)

        if loc not in noncombat_analysis_skip_locations:
            ncrolls[turn] &= guess_noncombat_roll(enc)

# Special processing - black forest / spooky forest
for turn in range(1, MAX_TURN):
    for loc in ["black forest"]:
        enc = bylocturn[loc].get(turn, None)
        if enc is None:
            continue
        if not enc.combat:
            continue
        cncrolls[turn] &= Roll(1, combat_percentages[loc])

# Special processing - 8-bit
for turn in range(1, MAX_TURN):
    odd_enc = bylocturn["8-bit realm / odd"].get(turn, None)
    even_enc = bylocturn["8-bit realm / even"].get(turn, None)
    if not odd_enc or not even_enc:
        # Can't say with certainty if it's right, as it could be from a
        # rejection of Goomba or Buzzy Beetle
        continue
    if odd_enc.name == "goomba" and even_enc.name == "buzzy beetle":
        # How to tell which is real and which is the rejection reroll?
        continue
    if odd_enc.name == even_enc.name:
        enc = Encounter("8-bit realm", odd_enc.turn, odd_enc.combat, odd_enc.name)
    elif odd_enc.name == "goomba":
        enc = Encounter("8-bit realm", odd_enc.turn, odd_enc.combat, odd_enc.name)
    elif even_enc.name == "buzzy beetle":
        enc = Encounter("8-bit realm", even_enc.turn, even_enc.combat, even_enc.name)
    byturn[turn].append(enc)
    mobrolls[turn] &= guess_combat_roll(enc)

# For determining encounter correspondences
correspondences = []
for turn in range(1, MAX_TURN):
    locs = sys.argv[1:]
    if not locs:
        continue
    try:
        #s = bylocturn["spooky forest"][turn]

        encs = [bylocturn[loc][turn] for loc in locs]
        if all([enc.combat for enc in encs]):
            correspondences.append((turn, mobrolls[turn], [enc.name for enc in encs]))
        if all([not enc.combat for enc in encs]):
            correspondences.append((turn, ncrolls[turn], [enc.name for enc in encs]))
    except KeyError:
        pass
correspondences.sort(key=lambda x: (x[1].minimum + x[1].maximum)/2)
for c in correspondences:
    print c

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

    if ncrolls[turn].minimum >= ncrolls[turn].maximum:
        print "NC", turn, ncrolls[turn]
        for enc in byturn[turn]:
            if not enc.combat:
                print "\t", enc.location, enc.name, guess_noncombat_roll(enc)
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

with open("../src/data/lar_noncombat_rolls.txt", "w") as fobj:
    for turn in range(1, MAX_TURN):
        roll = ncrolls[turn]
        if roll.minimum >= roll.maximum:
            # Don't record the data if it's broken
            roll = Roll(1, 100)
        # Turn, roll_number (so we can add the rerolls on rejections in future), min, max
        fobj.write("%s\t%s\t%s\t%s\n" % (turn, 0, roll.minimum, roll.maximum))
