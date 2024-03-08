# data/

This folder contains a single `.CSV` for each cruise listed in `config.json`.

REMEMBER, exactly spelling and case matters for the file names!! They have to exactly
match what is written in `config.json`

Each `.CSV` will have 10 required columns. These columns **MUST** have values for
every row!! No blank cells in any of these 10 columns.

1. `Location` - a concatenation of `Region` + `Site` columns

2. `Cylinder` - a concatenation of `Dive` + `Core` columns

3. `Date` - when the sample was collected. Must be written as `yyyy-mm-dd`.
   e.g., `2012-12-12` is December 12th, 2012.

4. `Core Fate` - what type of sample/core the row refers to

5. `Latitude` - in decimal degrees

6. `Longitude` - in decimal degrees

7. `Horizon` - written as `startDepth_finalDepth`; e.g., `0_3` is between 0cm and 3cm.
   This is used to help label data in the tool.

8. `start_depth` - the starting depth in cm for the given row. does NOT have to match
   what is listed for the `Horizon` measurement! This is for plotting the data
   when the `Horizon` is larger than 1cm.

9. `final_depth` - the final depth in cm for the given row. does NOT have to match
   what is listed for the `Horizon` measurement! This is for plotting the data
   when the `Horizon` is larger than 1cm.

10. `sum_abundance` - the sum of the abundance values for all taxa in a given
    row of the `.CSV`. Will be used by the program when calculating the
    relative abundance for any taxa.

Make sure these 10 columns are also listed in the `Meta` variables list in the
corresponding `.JSON` meta file for the cruise the `.CSV` refers to.

After this, you can include any columns you want, and they can be as full or
as empty as you please.

For any additional columns you want to interpolate or see in the core view,
they must go in the `Geochemistry` or `Taxa` variables lists in the `.JSON` for
the given cruise.
