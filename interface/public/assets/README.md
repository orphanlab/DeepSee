# How to structure your assets

The entry point for the program is `config.json`, which should be in the same
folder as this file, spelled exactly as written.

It will look like this:

```(json)
{
    cruise: ["cruise", ... ]
}
```

- Edit that file to include the names of all cruises in each of three
  sub-directories in this same folder: `meta/`, `data/`, and `backgrounds/`

- e.g., including "Pescadero" in `config.json` means that the program will
  expect to find `meta/Pescadero.json`, `data/Pescadero.csv`, and
  `backgrounds/Pescadero/` all created in the same directory as `config.json`.

- This is explained in more detail below:

## meta/

This folder should have 1 file for each cruise => a `<cruise>.json` with
background filenames and lists of variable names organized by their category.

See the README in `meta/` for more info.

## data/

This folder should have 1 file for each cruise => a `<cruise>.csv` with all
of the geochemical and taxonmic data.

See the README in `data/` for more info.

## backgrounds/

This folder should have 1 folder for each cruise => `<cruise>/` which contains
any background files (`.png`) and associated meta files (`.json`) to plot on
the map in the tool.

See the README in `backgrounds/` for more info.
