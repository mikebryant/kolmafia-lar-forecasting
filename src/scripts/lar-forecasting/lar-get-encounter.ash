import "lar-forecasting.ash";

void main(string loc, int turn) {
  print(lar_encounter_to_string(lar_get_encounter(loc.to_location(), turn)));
}
