import "lar-forecasting.ash";

void main() {

  print("Combat percentages:");
  foreach key, value in lar_combat_percentages {
    print(key.to_string() + ": " + value);
  }

  if (!(lar_encounter_known_is_combat(false, $location[sonofa beach], 576))) {
    print("Fail: We should know the combat status of sonofa beach at turn 576");
  }

  if((lar_encounter_monster($location[the spooky forest], 1) != $monster[triffid])) {
    print("Fail: Spooky forest turn 1 should be a triffid");
  }

}
