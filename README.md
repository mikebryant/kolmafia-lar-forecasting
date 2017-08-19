# kolmafia-lar-forecasting
Live. Ascend. Repeat. - See what's next for you

## How do I use it?
First, install it by running this command in KoLmafia's graphical CLI:

```
svn checkout https://github.com/mikebryant/kolmafia-lar-forecasting/branches/master/src/
```

Then, run `lar-showall` to show the next encounter in each zone, if known.

To update the script, run this command in the graphical CLI:

```
svn update
```


## Using in scripts

`<import lar-forecasting.ash>;`

### `lar_known_encounter`

Do we know what this encounter is?

### `lar_get_encounter`

Get an object describing the encounter for that location/turn etc.
