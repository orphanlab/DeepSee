# DeepSee interpolations server

A Python 3.9 Flask web app running on a Waitress WSGI server. Cross-platform!

**NOTE FOR macOS/Linux USERS**

- You may need to prefix your terminal commands with `sudo` to grant the system write access to restricted folders.
  - e.g., `sudo python -m pip install`

## Packages

Two different packages were used for interpolation:

1. Discrete Sibson (Natural Neighbor) Interpolation in 3D.
   - See: <https://github.com/innolitics/natural-neighbor-interpolation>
   - **NOTE**: This package only works on a `Windows OS`. The current (08/24/2021) implementation of the frontend
     checks if the user is on a Windows machine before requesting `app.py` for an interpolation; if the user is not
     on a Windows machine, the frontend does not even attempt the request.
   - Because of this limitation, there are two versions of `requirements.txt` for installing the required python
     packages. The only difference between the files is that the `-mac` version does not have the `naturalneighbors`
     package.

2. Nearest and Linear Interpolation over unstructured D-D data.
   - See: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html>

## Getting Started

1. Install Python 3.9.x by visiting <https://www.python.org/>.
2. Open a command window or terminal rooted in this folder.

The commands for Python used are slightly different between Windows, MacOS, and Linux.
But the order of the operations is the same.

### Windows

1. Check that python was install correctly with the command `py --version`.
2. Create a python virtual environment (e.g. `py -3.9 -m venv venv`)
3. Activate the environment (e.g. `venv\Scripts\activate.bat`)
4. To check that the correct `python` command is invoked, run `WHERE python`. You may see multiple results.
   At the top of the results, you should see `C:\<path>\<to>\<folder>\venv\Scripts\python.exe`.
5. Install the required packages (e.g. `python -m pip install -r requirements-win.txt`)

### MacOS/Linux

1. Check that python was install correctly with the command `python3 --version`.
2. Create a python virtual environment (e.g. `python3 -m venv venv`)
3. Activate the environment (e.g. `source venv/bin/activate`)
4. To check that the correct `python` command is invoked, run `which python`. You may see multiple results.
   At the top of the results, you should see `<path>/<to>/<folder>/venv/bin/python`.
5. Install the required packages (e.g. `python -m pip install -r requirements-mac.txt`)

### Known Installation Issues

- The python package `naturalneighbors` may require a bunch of extra packages installed on your computer. Try your best to follow the instructions that the compiler gives you. If you get stuck, please reach out.

## Testing

At the start of every session, remember to activate your virtual environment!!

To test the server, run `python app.py` (from inside the activated virtual
environment)

## Bundling

At the start of every session, remember to activate your virtual environment!!

To bundle the server into a single executable, run `pyinstaller --onefile app.py`

The generated executable will be found at `dist\app.exe` on Windows and `dist/app` on MacOS/Linux.
