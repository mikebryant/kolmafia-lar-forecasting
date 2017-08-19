import "lar-forecasting.ash";

void main() {
  foreach key in $locations[] {
    if (lar_known_encounter(key)) {
      print(key + " -> " + lar_encounter_to_string(lar_get_encounter(key)));
    }
  }
}
