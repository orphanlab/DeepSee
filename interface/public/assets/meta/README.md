# meta/

This folder contains a single `.JSON` for each cruise listed in `config.json`.

REMEMBER, exactly spelling and case matters for the file names!! They have to exactly
match what is written in `config.json`

Each `.JSON` will have this structure, with the exactly spelling and case:

```(json)
{
    "backgrounds": [ "bg1", ... ],
    "variables": {
        "Meta": [ "colA", ... ],
        "Geochemistry": [ "colB", ... ],
        "Taxa": [ "colC", ... ]
    }
}
```

- `backgrounds` will contain the names of the `.PNG` and `.JSON` files in the
  `backgrounds/<cruise>/` sub-folder; e.g., `Auka_MAP_slope3710-3630`.
  Only include the background name ONCE. The program will know to look for both
  `<background>.PNG` and `<background>.JSON`.

- `Meta` will contain the names of the metadata columns in the `.CSV`. See the
  README in `data/` for more info about what columns are required here.

- `Geochemistry` will contain the names of the columns you want to treat as
  geochemicals for the purposes of interpolation and viewing core data.
  Currently, this does not change how the data is visualized.

- `Taxa` will contain the names of the columns you want to treat as taxa
  for the purposes of interpolation and viewing core data. Currently, this
  divides the column value by another column, `sum_abundance`, on-the-fly
  to create a new value for that taxa: relative abundance.
