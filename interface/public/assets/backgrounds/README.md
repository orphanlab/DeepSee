# backgrounds/

This folder contains a single `<cruise>/` directory for each cruise listed in
`config.json`.

REMEMBER, exactly spelling and case matters for the folder names!! They have to exactly
match what is written in `config.json`

Each `<cruise>/` folder will contain two files for each background listed in the
`.JSON` for the given cruise. The name of each background, `<background>`, will
prefix both files.

One file will be a `<background>.PNG` image that is going to be plotted in the
Map View.

The other file will be a `<background>.JSON` with a single key-value pair =>
`{ bbox: [lon_start, lat_start, lon_end, lat_end] }`. See the diagram below
for how the coordinates correspond to the image.

```(bash)
                   lon_end
           +----------o lat_end
           |          |
           |          |
 lat_start o----------+
       lon_start
```
