# DriveBot starter files

Robot driven by the keyboard in CoppeliaSim, with a filter that makes the
driving smooth so it uses less energy. Python, no ROS.

## What each file does (one line each)

| File | What it does |
| --- | --- |
| `config.py` | All shared numbers in one place (robot size, motor constants, limits, keys, test route) |
| `sim_link.py` | The only file that talks to CoppeliaSim: connect, read position, set wheel speeds, stop |
| `keys.py` | Turns the arrow keys you hold into the speeds you WANT |
| `model.py` | The physics: wheel speeds and the ENERGY a speed curve costs |
| `profiles.py` | Builds speed curves for the same trip: raw key press vs smooth |
| `shaper.py` | The DriveBot filter: smooths the wanted speeds before the wheels get them |
| `logger.py` | Records every cycle and saves it as a CSV |
| `plots.py` | Live path while driving, and the raw vs shaped figure for the report |
| `main.py` | The loop that calls all the others, in order |

## How to work

1. Every file starts with a comment block: **what it does**, **what you have to do**, **how to test**.
2. Search each file for `TODO`. Each one is a small job with a hint right under it.
3. Until a TODO is done, its function stops with a message saying which TODO is missing.
4. Test each file ALONE with `python filename.py` before using it from `main.py`.
   The test code is at the bottom of each file, with the expected result in a comment.
5. The guess numbers in `config.py` (marked `# CHECK`) must be replaced with real ones.

## Order to build

1. `config.py` -> `sim_link.py` -> `keys.py` -> `model.py` (TODO 1 only) -> `main.py` stage 1: robot drives from the keyboard
2. `logger.py` and `plots.py` (live part)
3. `model.py` (the rest) and `profiles.py`: energy of raw vs smooth curve
4. `shaper.py` and `main.py` shaped mode
5. `main.py` route replay, then `compare.py` (code is at the end of `main.py`)

## Good to know

- The logger saves the speed the robot REALLY had (measured by the simulator), not the speed you asked for. Energy is worked out from that.
- The raw profile needs an assumption: how fast the motors get up to speed when a key is pressed (`RAW_RAMP` in `config.py`). Write the value you chose in the report.
- The shaped run lags behind the keys on purpose, so in the same route time it may cover a slightly different distance. Compare energy per metre as well as total energy.
- The numbers in `config.py` are guesses. The "expected" values in the test comments (for example 154 J for the smooth profile) only hold for those guesses.

## Rules

- All files in ONE folder. Run commands from that folder.
- Never name a file like a library (`time.py`, `math.py`, `csv.py`, `numpy.py`).
- A file may only import from files lower in this list: `config`, then
  `model` / `sim_link`, then `profiles`, then `keys` / `shaper` / `logger` / `plots`, then `main`.
- Stuck for more than about half an hour? Ask, and paste the code and the full error message.

## Set up once

```
conda create -n coppelia python=3.10
conda activate coppelia
pip install coppeliasim-zmqremoteapi-client numpy matplotlib scipy
```
