notify "LeaChim";

import "lar-forecasting.ash";

void main() {
  foreach loc in $locations[] {
    print(lar_get_known_info(loc));
  }
}
