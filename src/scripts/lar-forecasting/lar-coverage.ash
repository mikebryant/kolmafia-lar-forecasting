notify "LeaChim";

import "lar-forecasting.ash";

boolean [location] quest_relevant_locations = $locations[
  the spooky forest,
  the dark neck of the woods,
  the dark heart of the woods,
  the dark elbow of the woods,
  the black forest,
  whitey's grove,
  the hidden temple,
  8-bit realm,
  the old landfill,
  the hidden park,
  the hidden apartment building,
  the hidden office building,
  the hidden bowling alley,
  the hidden hospital,
  the sleazy back alley,
  the haunted pantry,
  the haunted kitchen,
  the haunted billiards room,
  the haunted library,
  the haunted conservatory,
  the haunted gallery,
  the haunted bathroom,
  the haunted bedroom,
  the haunted ballroom,
  the haunted laboratory,
  the haunted storage room,
  the haunted nursery,
  the haunted wine cellar,
  the haunted laundry room,
  the haunted boiler room,
  the outskirts of cobb's knob,
  the bat hole entrance,
  guano junction,
  the batrat and ratbat burrow,
  the beanbat chamber,
  cobb's knob barracks,
  cobb's knob kitchens,
  cobb's knob harem,
  cobb's knob treasury,
  the "fun" house,
  inside the palindome,
  the degrassi knoll restroom,
  the degrassi knoll gym,
  the degrassi knoll bakery,
  the degrassi knoll garage,
  the unquiet garves,
  the defiled nook,
  the defiled niche,
  the defiled cranny,
  the defiled alcove,
  the penultimate fantasy airship,
  the castle in the clouds in the sky (basement),
  the castle in the clouds in the sky (ground floor),
  the castle in the clouds in the sky (top floor),
  the hole in the sky,
  infernal rackets backstage,
  the laugh floor,
  pandamonium slums,
  the goatlet,
  Itznotyerzitz Mine,
  lair of the ninja snowmen,
  the extreme slope,
  the icy peak,
  the smut orc logging camp,
  a-boo peak,
  twin peak,
  the obligatory pirate's cove,
  barrrney's barrr,
  the f'c'le,
  the poop deck,
  belowdecks,
  frat house,
  frat house in disguise,
  wartime frat house,
  wartime frat house (hippy disguise),
  hippy camp,
  hippy camp in disguise,
  wartime hippy camp,
  wartime hippy camp (frat disguise),
  sonofa beach,
  next to that barrel with something burning in it,
  near an abandoned refrigerator,
  over where the old tires are,
  out by that rusted-out car,
  the battlefield (frat uniform),
  the battlefield (hippy uniform),
  the arid\, extra-dry desert,
  the oasis,
  the upper chamber,
  the middle chamber,
];

int desired_turns = 500;

void main() {
  print("Coverage for " + desired_turns + " turns:");
  print ("Location, Combat/non-combat, monster name (out of the combat encounters)");
  foreach loc in quest_relevant_locations {
    int cnc_found = 0;
    int combat_found = 0;
    int monster_found = 0;
    for turn from 0 to desired_turns {
      if(lar_encounter_known_is_combat(loc, turn)) {
        cnc_found += 1;

        if(lar_encounter_is_combat(loc, turn)) {
          combat_found +=1;
        }

        if(lar_encounter_known_monster(loc, turn)) {
          monster_found += 1;
        }
      }
    }

    // Report
    print(loc + ": " + (cnc_found * 100 / desired_turns) + "%, " + (monster_found * 100 / (combat_found + 1)) + "%");
  }
}
