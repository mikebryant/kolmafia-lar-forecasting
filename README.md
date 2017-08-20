# kolmafia-lar-forecasting
Live. Ascend. Repeat. - See what's next for you

## How do I use it?
First, install it by running this command in KoLmafia's graphical CLI:

```
svn checkout https://github.com/mikebryant/kolmafia-lar-forecasting/branches/master/src/
```

Then, run `lar-show-next` to show the next encounter in each zone, if known.

Or `lar-show-upcoming spooky forest` to see the next 10 upcoming encounters, if known.

To update the script, run this command in the graphical CLI:

```
svn update
```


## Using in scripts

`<import lar-forecasting.ash>;`

### `lar_encounter_known_is_combat`

Do we know what this type of encounter is?

### `lar_encounter_is_combat`

Is this encounter combat?

### `lar_encounter_known_monster`

Do we know what monster it is for this encounter?

### `lar_encounter_monster`

What monster is this encounter?

### Example

```
> ash import lar-forecasting.ash; lar_encounter_monster($location[the dark elbow of the woods], 14).to_string();

Returned: Demoninja

> ash import lar-forecasting.ash; lar_encounter_known_monster($location[the dark elbow of the woods], 14);

Returned: true

> ash import lar-forecasting.ash; lar_encounter_known_is_combat($location[the dark elbow of the woods], 14);

Returned: true

> ash import lar-forecasting.ash; lar_encounter_is_combat($location[the dark elbow of the woods], 14);

Returned: false
```

## Data files

If you're interested in the data I've generated / computed:

`src/data/lar_cnc_rolls.txt` - Combat/Noncombat rolls per turn
`src/data/lar_monster_rolls.txt` - Monster rolls per turn
`src/data/lar_monster_orders.txt` - What order the monsters appear in each zone

All rolls are presented as max/min pairs, as it still needs to be narrowed down, but this data is still useful for some zones.

## Updating

```
cd utils
./update
```
