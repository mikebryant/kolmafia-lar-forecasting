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

cncrolls = defaultdict(lambda: Roll(0, 100))

mobrolls = defaultdict(lambda: Roll(0, 100))

byturn = defaultdict(list)
byloc = defaultdict(list)
bylocturn = defaultdict(dict)

combat_percentages = {}

with open("../src/data/lar_combat_percentages.txt") as fobj:
    for line in fobj.readlines():
        line = line.strip()
        print line.split("\t")
        if not line:
            continue
        loc, cpc = line.split("\t")
        combat_percentages[loc] = cpc

source_encounter_lists = {
    "the dark heart of the woods": [
        "fallen archfiend",
        "g imp",
        "p imp",
    ],
    "the dark neck of the woods": [
        "hellion",
        "p imp",
        "w imp",
    ],
    "the dark elbow of the woods": [
        "demoninja",
        "g imp",
        "l imp",
    ],
    "black forest": [
        "black friar",
        "black magic woman",
        "black panther",
        "black widow",
        "black adder",
    ],
    "haunted billiards room": [
        "pooltergeist",
        "chalkdust wraith",
    ],
    "outskirts of cobb's knob": [
        "knob goblin barbecue team",
        "sub-assistant knob mad scientist",
        "knob goblin assistant chef",
        "sleeping knob goblin guard",
    ],
    "haunted kitchen": [
        "zombie chef",
        "skullery maid",
        "paper towelgeist",
        "demonic icebox",
        "possessed silverware drawer",
    ],
}

check_encounter_lists = {
    "spooky forest": [
        "triffid",
        "bar",
        "spooky mummy",
        "wolfman",
        "warwelf",
        "spooky vampire",
    ],
    "8-bit realm": [
        "buzzy beetle",
        "bullet bill",
        "zol",
        "blooper",
        "keese",
        "octorok",
        "koopa troopa",
        "tektite",
        "goomba",
    ],
    "haunted pantry": [
        "overdone flame-broiled meat blob",
        "flame-broiled meat blob",
        "undead elbow macaroni",
        "fiendish can of asparagus",
        "possessed can of tomatoes",
    ],
}

analysis_skip_locations = [
    "8-bit realm",
    "haunted pantry",
    "spooky forest",
]

def guess_combat_roll(enc):
    loc = enc.location
    if not combat:
        return Roll(0, 100)
    if loc not in source_encounter_lists:
        return Roll(0, 100)
    el = source_encounter_lists[loc]
    if enc.name not in el:
        print("%s/%s not in encounter list for %s!" % (enc.turn, enc.name, loc))
        return Roll(0, 100)
    i = el.index(enc.name)
    return Roll((i * 100)//len(el), ((i+1) * 100)//len(el))


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

        if loc in combat_percentages:
            cpc = combat_percentages[loc]
            if combat:
                cncrolls[turn] &= Roll(0, cpc)
                #cncrolls[turn].maximum = min(cncrolls[turn].maximum, cpc)
            else:
                cncrolls[turn] &= Roll(cpc, 100)
                #cncrolls[turn].minimum = max(cncrolls[turn].minimum, cpc)

        mobrolls[turn] &= guess_combat_roll(enc)

        """
        if loc in source_encounter_lists:
            if combat:
                el = source_encounter_lists[loc]
                if enc.name not in el:
                    print("%s not in encounter list for %s!" % (enc.name, loc))
                else:
                    i = el.index(enc.name)
                    mobrolls[turn].minimum = max(mobrolls[turn].minimum, (i * 100)//len(el))
                    mobrolls[turn].maximum = min(mobrolls[turn].maximum, ((i+1) * 100)//len(el))
        """



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
for turn in range(1, 50):

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
            continue
        fobj.write("%s\t%s\t%s\n" % (turn, roll.minimum, roll.maximum))

with open("../src/data/lar_monster_rolls.txt", "w") as fobj:
    for turn in range(1, MAX_TURN):
        roll = mobrolls[turn]
        if roll.minimum >= roll.maximum:
            # Don't record the data if it's broken
            continue
        # Turn, roll_number (so we can add the rerolls on rejections in future), min, max
        fobj.write("%s\t%s\t%s\t%s\n" % (turn, 0, roll.minimum, roll.maximum))
