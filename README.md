# DeepSee <a href="https://www.its.caltech.edu/~datavis/deepsee/"><img align="right" src='https://github.com/orphanlab/DeepSee/blob/main/interface/public/icons/android-chrome-512x512.png' height="38"></a>

[![license](https://img.shields.io/badge/License-Apache--2.0-454295)](https://github.com/orphanlab/DeepSee/blob/main/LICENSE)
[![arxiv badge](https://img.shields.io/badge/arXiv-2403.04761-red)](https://arxiv.org/abs/2403.04761)
[![DOI:10.1145/3613904.3642001](https://img.shields.io/badge/DOI-10.1145/3613904.3642001-blue)](https://doi.org/10.1145/3613904.3642001)

Visualize 3D interpolations of deep ocean biogeochemical sediment samples overlaid on 2D seafloor maps!

🌊🛥️🦑🦀🐚

![The DeepSee System](https://github.com/orphanlab/DeepSee/blob/main/images/deepsee.png)

## What is DeepSee?

Deep ocean researchers can now access 2D topographic maps and color photomosaics of the seafloor, allowing for the relation of point-source seafloor sample collections (e.g. sediment cores, rock, animal, and water samples) with their appropriate environmental context at centimeter to kilometer spatial scales.
However, while 2D maps of spatial locations of samples are valuable, the field currently lacks visualization tools which extend into the 3rd dimension, i.e. within the subseafloor.

DeepSee is an interactive workspace for scientists to upload sediment core data and map images and see their sampling history displayed across multiple connected views simultaneously.
Interactive maps of the seafloor between centimeter and kilometer resolution are labeled with information about previous dives as well as collected samples.
Alongside these maps, DeepSee displays 2D visualizations that show parameter gradients as a function of depth and interactive 3D visualizations of data interpolations in the space between samples.
The data interpolations can be run in real time, allowing scientists to "see" below the seafloor and determine the most likely places to collect high-value samples.
To support decision making, DeepSee provides annotation tools on the maps for taking notes, useful for communicating findings and planning future dives.
Finally, DeepSee is portable and requires no internet access, empowering scientists to use DeepSee on field expeditions in remote environments.

This code accompanies the research paper:

**[DeepSee: Multidimensional Visualizations of Seabed Ecosystems][paper]**  
<span style="opacity: 70%">Adam Coscia, Haley M. Sapers, Noah Deutsch, Malika Khurana, John S. Magyar, Sergio A. Parra, Daniel R. Utter, Rebecca L. Wipfler, David W. Caress, Eric J. Martin, Jennifer B. Paduan, Maggie Hendrie, Santiago Lombeyda, Hillary Mushkin, Alex Endert, Scott Davidoff, Victoria J. Orphan</span>  
_ACM Conference on Human Factors in Computing Systems (CHI), 2024_  
| [📖 Paper][paper] | [▶️ Live Demo][demo] | [🎞️ Demo Video][video] | [🧑‍💻 Code][code] |

## Features

<details>
  <summary> 🗺️ Explore maps of the ocean floor overlaid with sampled cores from previous dives:</summary>
  <img src="https://github.com/orphanlab/DeepSee/blob/main/images/map-view.png" width="50%">
</details>

<details>
  <summary> 📊 Compare geochemical, physical, and biological attributes across horizons between cores:</summary>
  <img src="https://github.com/orphanlab/DeepSee/blob/main/images/core-view.png" width="55%">
</details>

<details>
  <summary> 🌐 Analyze interpolated core attributes in 3D between cores:</summary>
  <img src="https://github.com/orphanlab/DeepSee/blob/main/images/interpolation-view.png">
</details>

### Demo Video

🎞️ Watch the demo video for a full tutorial here: <https://youtu.be/HJ4zbueJ9cs>

## Live Demo

🚀 For a live demo, visit: <https://www.its.caltech.edu/~datavis/deepsee/>

## Getting Started

✅ You can try DeepSee locally on your own computer by downloading it as pre-built software!

### Windows

- Download DeepSee for Windows here: <https://sourceforge.net/projects/deepsee/files/v0.1.0/deepsee.win.zip/download>

- Run DeepSee:

  1. Unzip the files to a new folder (e.g., named `DeepSee`)
  2. Inside the folder should be `DeepSee.exe`. Double-click that to run the visualizations interface
  3. Inside the folder should also be `interpolations.exe`. Double-click that to start the interpolations server

- If you want to modify the data that DeepSee uses:

  1. Inside the folder navigate to `resources\assets\`
  2. Read the documentation for each of the sub-directories
  3. After you make changes to the data, simply reload the tool (e.g., in the open tool window, press `CTRL+SHIFT+R`)

### MacOS / Linux

- Download DeepSee for MacOS/Linux here: <https://sourceforge.net/projects/deepsee/files/v0.1.0/deepsee.mac.zip/download>

- Run DeepSee:

  1. Unzip the files to a new folder (e.g., named `DeepSee`)
  2. Inside the folder should be `DeepSee.app`. Double-click that to run the visualizations interface
  3. Inside the folder should also be `interpolations`. Double-click that to start the interpolations server

- If you want to modify the data that DeepSee uses:

  1. Right-click on `DeepSee.app` and select `Show Package Contents`
  2. Navigate to `Contents/Resources/assets/`
  3. Read the documentation for each of the sub-directories
  4. After you make changes to the data, simply reload the tool (e.g., in the open tool window, press `COMMAND+SHIFT+R`)

## Development

🌱 If you want to customize DeepSee for your own project, start here!

- Install Node.js `v16.x` and npm `v7.x` by visiting ([release](https://nodejs.org/en/))
- Install Python `v3.9.x` ([latest release](https://www.python.org/downloads/release/python-3913/))
- Clone this repo to your computer ([instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository))

```bash
git clone git@github.com:orphanlab/DeepSee.git

# use --depth if you don't want to download the whole commit history
git clone --depth 1 git@github.com:orphanlab/DeepSee.git
```

### Interface

- A frontend Vue.js v2 app to visualize data in the browser.
- Additional details can be found in [interface/README.md](https://github.com/orphanlab/DeepSee/blob/main/interface/README.md)
- To upload your own data, see [interface/public/assets/README.md](https://github.com/orphanlab/DeepSee/blob/main/interface/public/assets/README.md)

Navigate to the interface folder:

```bash
cd interface
```

Install dependencies:

```bash
npm install
```

Then run DeepSee:

```bash
npm run serve
```

Navigate to [localhost:8080](http://localhost:8080/). You should see DeepSee running in your browser :)

### Server

- A backend Python 3.9 Flask web app to process interpolations in the background
- Additional details can be found in [deepsee/server/README.md](https://github.com/orphanlab/DeepSee/blob/main/server/README.md)

Navigate to the server folder:

```bash
cd server
```

Install dependencies:

- If you are running Windows:

```bash
# Start a virtual environment
py -3.9 -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements-win.txt
```

- If you are running MacOS / Linux:

```bash
# Start a virtual environment
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
python -m pip install -r requirements-mac.txt
```

Then run the server:

```bash
python app.py
```

## Credits

DeepSee is a result of a collaboration between visualization experts in human-centered computing, interaction design, scientific data visualization and art, as well as scientists and researchers with expertise in environmental microbiology, geochemistry and geology from
<img src="https://adamcoscia.com/assets/icons/other/gt-logo.png" alt="Interlocking GT" height="21" style="vertical-align: bottom;"/>
Georgia Tech,
<img src="https://adamcoscia.com/assets/icons/other/caltech-seal.svg" alt="Caltech seal" height="21" style="vertical-align: bottom;"/>
Caltech,
<img src="https://adamcoscia.com/assets/icons/other/artcenter-logo.png" alt="Artcenter dot" height="21" style="vertical-align: bottom;"/>
ArtCenter,
<img src="https://adamcoscia.com/assets/icons/other/mbari-logo.svg" alt="MBARI logo" height="21" style="vertical-align: bottom;"/>
Monterey Bay Aquarium Research Institute (MBARI), and
<img src="https://adamcoscia.com/assets/icons/other/nasa-logo.png" alt="NASA logo" height="21" style="vertical-align: bottom;"/>
NASA Jet Propulsion Laboratory (JPL).

DeepSee is created by
<a href='https://adamcoscia.com/' target='_blank'>Adam Coscia</a>,
Haley M. Sapers,
Noah Deutsch,
Malika Khurana,
John S. Magyar,
Sergio A. Parra,
Daniel R. Utter,
Rebecca L. Wipfler,
David W. Caress,
Eric J. Martin,
Jennifer B. Paduan,
Maggie Hendrie,
Santiago Lombeyda,
Hillary Mushkin,
Alex Endert,
Scott Davidoff,
and
Victoria J. Orphan.

### Data

- AUV data archived from the Marine Geoscience Data System (MDGS) in the data compilation entitled [PescaderoBasin_MBARI](https://www.marine-geo.org/tools/search/entry.php?id=PescaderoBasin_MBARI)
- GeoTIFF of combined 2015 and 2018 surveys can be found at [doi 10.26022/IEDA/330830](http://get.iedadata.org/doi/330830)
- The included map data were processed and kindly provided by the [Seafloor Mapping Lab](https://www.mbari.org/team/seafloor-mapping/) at MBARI
- Geochemistry and microbial community composition data were selected from the data published in [Speth et al. 2022](https://www.nature.com/articles/s41396-022-01222-x)

## Citation

To learn more about DeepSee, please read our [research paper][paper] (published at [CHI '24](https://chi2024.acm.org/)).

```bibtex
@inproceedings{Coscia:2024:DeepSee,
  author = {Coscia, Adam and Sapers, Haley M. and Deutsch, Noah and Khurana, Malika and Magyar, John S. and Parra, Sergio A. and Utter, Daniel R. and Wipfler, Rebecca L. and Caress, David W. and Martin, Eric J. and Paduan, Jennifer B. and Hendrie, Maggie and Lombeyda, Santiago and Mushkin, Hillary and Endert, Alex and Davidoff, Scott and Orphan, Victoria J.},
  title = {DeepSee: Multidimensional Visualizations of Seabed Ecosystems},
  year = {2024},
  isbn = {979-8-4007-0330-0/24/05},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3613904.3642001},
  doi = {10.1145/3613904.3642001},
  booktitle = {Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems},
  location = {Honolulu, HI, USA},
  series = {CHI '24}
}
```

## Copyright

Copyright (c) 2022-23 California Institute of Technology (“Caltech”). U.S. Government sponsorship acknowledged.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
- Neither the name of Caltech nor its operating division, the Jet Propulsion Laboratory, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## License

The software is available under the [Apache-2.0 License](https://github.com/orphanlab/DeepSee/blob/main/LICENSE).

Open Source License Approved by Caltech/JPL

APACHE LICENSE, VERSION 2.0

- Text version: <https://www.apache.org/licenses/LICENSE-2.0.txt>
- SPDX short identifier: Apache-2.0
- OSI Approved License: <https://opensource.org/licenses/Apache-2.0>

## Contact

If you have any questions, feel free to [open an issue](https://github.com/orphanlab/DeepSee/issues/new) or contact [Adam Coscia](https://adamcoscia.com).

[paper]: https://arxiv.org/abs/2403.04761
[demo]: https://www.its.caltech.edu/~datavis/deepsee/
[video]: https://youtu.be/HJ4zbueJ9cs
[code]: https://github.com/orphanlab/DeepSee
