notify "LeaChim";

record lar_roll {
  int minimum;
  int maximum;
};

static {
  // lar_cnc_rolls[turn]
  lar_roll [int] lar_cnc_rolls;

  // lar_monster_rolls[turn][retry]
  lar_roll [int, int] lar_monster_rolls;

  // lar_monster_orders[location][0]
  monster [location][int] lar_monster_orders;

  // lar_combat_percentags[location]
  int [location] lar_combat_percentages;
}

void lar_load_data() {
  file_to_map("lar_cnc_rolls.txt", lar_cnc_rolls);
  file_to_map("lar_monster_rolls.txt", lar_monster_rolls);
  file_to_map("lar_monster_orders.txt", lar_monster_orders);
  file_to_map("lar_combat_percentages.txt", lar_combat_percentages);
}

// Auto load data
static {
  lar_load_data();
}
lar_load_data();

boolean lar_encounter_is_combat_with_roll(int roll, location loc) {
  int cpc = lar_combat_percentages[loc];
  return (roll <= cpc);
}

boolean lar_encounter_is_combat(location loc, int turn) {
  lar_roll roll = lar_cnc_rolls[turn];
  return lar_encounter_is_combat_with_roll((roll.minimum + roll.maximum) / 2, loc);
}

boolean lar_encounter_is_combat(location loc) {
  return lar_encounter_is_combat(loc, my_turncount() + 1);
}

boolean lar_encounter_known_is_combat(boolean guess, location loc, int turn) {
  if (!(lar_combat_percentages contains loc)) {
    return false;
  }
  if (!(lar_cnc_rolls contains turn)) {
    return false;
  }
  if (guess) {
    return true;
  }
  lar_roll roll = lar_cnc_rolls[turn];
  if (lar_encounter_is_combat_with_roll(roll.minimum, loc) == lar_encounter_is_combat_with_roll(roll.maximum, loc)) {
    // The whole range agrees, so we're not guessing
    return true;
  }
  return false;
}

boolean lar_encounter_known_is_combat(boolean guess, location loc) {
  return lar_encounter_known_is_combat(guess, loc, my_turncount() + 1);
}

boolean lar_encounter_known_is_combat(location loc) {
  return lar_encounter_known_is_combat(false, loc, my_turncount() + 1);
}

boolean lar_encounter_known_is_combat(location loc, int turn) {
  return lar_encounter_known_is_combat(false, loc, turn);
}





// monsters
monster lar_encounter_monster_with_roll(int roll, location loc) {
  //int cpc = lar_combat_percentages[loc];
  //return (roll > cpc);
  monster [int] monsters = lar_monster_orders[loc];
  return monsters[(roll-1)/(100/count(monsters))];
}

monster lar_encounter_monster(location loc, int turn) {
  lar_roll roll = lar_monster_rolls[turn][0];
  return lar_encounter_monster_with_roll((roll.minimum + roll.maximum) / 2, loc);
}

monster lar_encounter_monster(location loc) {
  return lar_encounter_monster(loc, my_turncount() + 1);
}

boolean lar_encounter_known_monster(boolean guess, location loc, int turn) {
  if(!(lar_monster_orders contains loc)) {
    return false;
  }
  if (!lar_encounter_known_is_combat(guess, loc, turn)) {
    return false;
  }
  if(!(lar_monster_rolls contains turn)) {
    return false;
  }
  if (guess) {
    return true;
  }
  lar_roll roll = lar_monster_rolls[turn][0];
  if (lar_encounter_monster_with_roll(roll.minimum, loc) == lar_encounter_monster_with_roll(roll.maximum, loc)) {
    return true;
  }
  return false;
}

boolean lar_encounter_known_monster(boolean guess, location loc) {
  return lar_encounter_known_monster(guess, loc, my_turncount() + 1);
}

boolean lar_encounter_known_monster(location loc) {
  return lar_encounter_known_monster(false, loc);
}

boolean lar_encounter_known_monster(location loc, int turn) {
  return lar_encounter_known_monster(false, loc, turn);
}


string lar_get_known_info(location loc, int turn) {
  string cnc = "unknown";
  if (lar_encounter_known_is_combat(loc, turn)) {
    if (lar_encounter_is_combat(loc, turn)) {
      cnc = "combat";
    } else {
      cnc = "noncombat";
    }
  }

  if (cnc != "unknown") {
    return(loc + " -> " + cnc);
  }

  return "";
}

string lar_get_known_info(location loc) {
  return lar_get_known_info(loc, my_turncount() + 1);
}
