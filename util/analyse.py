#!/usr/bin/env python

from collections import defaultdict

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

    def __repr__(self):
        return "Roll(%s, %s)" % (self.minimum, self.maximum)

cncrolls = {}
for i in range(1, 2000):
    cncrolls[i] = Roll(0, 100)

mobrolls = {}
for i in range(1, 2000):
    mobrolls[i] = Roll(0, 100)

byturn = defaultdict(list)
byloc = defaultdict(list)
bylocturn = defaultdict(dict)

combat_percentages = {
    "spooky forest": 85,
    "the dark heart of the woods": 90,
    "the dark elbow of the woods": 90,
    "the dark neck of the woods": 90,
    "the defiled niche": 85,
    "the defiled cranny": 85,
    "the defiled alcove": 85,
    "the defiled nook": 85,
    "the penultimate fantasy airship": 80,
    "the obligatory pirate's cove": 58.8,
    "the sleazy back alley": 80,
    "haunted pantry": 82,
    "outskirts of cobb's knob": 80,
}

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

#def guess_roll(loc, enc):


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
        if monster_name == "none":
            monster_name = ''
        enc = Encounter(loc, turn, combat, monster_name or encounter_name)
        byturn[turn].append(enc)
        byloc[loc].append(enc)
        bylocturn[loc][turn] = enc

        if loc in combat_percentages:
            cpc = combat_percentages[loc]
            if combat:
                cncrolls[turn].maximum = min(cncrolls[turn].maximum, cpc)
            else:
                cncrolls[turn].minimum = max(cncrolls[turn].minimum, cpc)

        if loc in source_encounter_lists:
            if combat:
                el = source_encounter_lists[loc]
                if enc.name not in el:
                    print("%s not in encounter list for %s!" % (enc.name, loc))
                else:
                    i = el.index(enc.name)
                    mobrolls[turn].minimum = max(mobrolls[turn].minimum, (i * 100)//len(el))
                    mobrolls[turn].maximum = min(mobrolls[turn].maximum, ((i+1) * 100)//len(el))



# For determining encounter correspondences
for turn in range(1, 1500):
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

# Debugging
for turn in range(1, 10):
    print "CNC", turn, cncrolls[turn]
    if cncrolls[turn].minimum >= cncrolls[turn].maximum:

        for enc in byturn[turn]:
            print "\t", enc.location, enc.combat, combat_percentages.get(enc.location, '')
    print "M", turn, mobrolls[turn]
    if mobrolls[turn].minimum >= mobrolls[turn].maximum:


        for enc in byturn[turn]:
            if enc.combat:
                print "\t", enc.location, enc.name
