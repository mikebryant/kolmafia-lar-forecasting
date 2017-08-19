script "lar-forecasting.ash";
notify "LeaChim";

import <zlib.ash>

boolean use_map_manager = true;

record lar_encounter {
  boolean combat; // True for combat, False for noncombat
  monster combat_monster; // If .combat, the monster we expect
  string noncombat_name; // If !.combat, the name of the NC encounter
  string encounter_subtype; // Optionally the encounter subtype, e.g. gremlins good/bad
};

//record lar_encounter_delay {
//  int required_delay; // Required turns spent in the zone to see this encounter
//  lar_encounter encounter; // The actual encounter
//};

static {
  // Index by:
  // location - where the encounter is
  // zone_special - Some special subparameter, e.g. battlefield as hippy or frat
  // current turn
  // required delay - Required turns spent in the zone to see this encounter
  lar_encounter [location, string, int, int] lar_encounter_data;
  lar_encounter lar_unknown_encounter;
  lar_unknown_encounter.combat = false;
  lar_unknown_encounter.noncombat_name = "unknown";
}

void lar_load_data() {
  clear(lar_encounter_data);
  if (use_map_manager) {
    load_current_map("lar_encounter_data_v1", lar_encounter_data);
  } else {
    file_to_map("lar_encounter_data_v1.txt", lar_encounter_data);
  }
}

// Auto load data
lar_load_data();

lar_encounter lar_get_encounter(location loc, string zone_special, int turn, int turns_spent) {
  lar_encounter ret = lar_unknown_encounter;
  int checked_delay = -1;

  foreach required_delay in lar_encounter_data[loc, zone_special, turn] {
    if (turns_spent >= required_delay && required_delay > checked_delay) {
      ret = lar_encounter_data[loc, zone_special, turn, required_delay];
      checked_delay = required_delay;
    }
  }
  // ret = lar_encounter_data[loc, turn][turns_spent];
  return ret;
}

boolean lar_known_encounter(location loc, string zone_special, int turn, int turns_spent) {
  return (lar_get_encounter(loc, zone_special, turn, turns_spent).noncombat_name != lar_unknown_encounter.noncombat_name);
}

lar_encounter lar_get_encounter(location loc, int turn) {
  return lar_get_encounter(loc, "", turn, loc.turns_spent);
}

lar_encounter lar_get_encounter(location loc) {
  return lar_get_encounter(loc, "", my_turncount(), loc.turns_spent);
}

boolean lar_known_encounter(location loc) {
  return (lar_get_encounter(loc).noncombat_name != lar_unknown_encounter.noncombat_name);
}

string lar_encounter_to_string(lar_encounter enc) {
  string out = "";
  if (enc.combat) {
    out = enc.combat_monster.to_string();
  } else {
    out = enc.noncombat_name;
  }
  if (length(enc.encounter_subtype) > 0) {
    out += " / " + enc.encounter_subtype;
  }
  return out;
}
