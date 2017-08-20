notify "LeaChim";

import "lar-forecasting.ash";

void main(location loc) {
  int start = my_turncount() + 1;
  for turn from start to (start + 10) {
    print(turn.to_string() + " -> " + lar_get_known_info(loc, turn));
  }
}
