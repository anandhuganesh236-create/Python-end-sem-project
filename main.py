"""
main.py  -  the control loop. It only CALLS the other files, in order.
======================================================================

WHAT THIS FILE DOES
    Every cycle (every DT seconds):
        1. get the wanted speeds          (keys.py, or the ROUTE list)
        2. smooth them                    (shaper.py)   only in 'shaped' mode
        3. turn them into wheel speeds    (model.py)
        4. send them to the robot         (sim_link.py)
        5. read where the robot is        (sim_link.py)
        6. record it                      (logger.py)
        7. draw it                        (plots.py)
    There is NO maths, NO plotting code and NO simulator code in this file.

HOW TO BUILD IT IN STAGES (change the settings below as each stage works)
    STAGE 1  Finish: config check, sim_link TODO 1-3, keys TODO 2, model TODO 1.
             Leave the settings as they are and run:  python main.py
             Drive the robot with the arrow keys. Esc stops.
    STAGE 2  Finish logger.py, then set  USE_LOGGER = True
    STAGE 3  Finish plots.py (TODO 1), then set  USE_PLOT = True
    STAGE 4  Finish shaper.py, then set  MODE = 'shaped'  and compare the feel
    STAGE 5  Set  USE_ROUTE = True  so the robot replays the SAME trip with no
             keys. Run once with MODE = 'raw', once with MODE = 'shaped'.
             You now have run_raw.csv and run_shaped.csv.
    STAGE 6  compare.py (see the end of this file) turns the two CSVs into the
             comparison figure.

BEFORE EVERY RUN
    CoppeliaSim open, PLAY pressed, robot's own script disabled.
    Run from this folder:   python main.py

USES: all the other files.          PHASE: 1 to 5
"""

import time
import matplotlib.pyplot as plt

from config import Robot, Motor, DT, ROUTE
from sim_link import connect, get_pose, set_wheels, stop
from keys import setup_keys, read_targets, stop_requested
from model import wheel_speeds
from shaper import Shaper
from logger import Logger
from plots import LivePlot

# ---- Settings: change these as your stages get finished -------------------
MODE = 'raw'          # 'raw' = keys go straight to the wheels, 'shaped' = DriveBot filter
USE_LOGGER = False    # STAGE 2: True once logger.py works
USE_PLOT = False      # STAGE 3: True once plots.py works
USE_ROUTE = False     # STAGE 5: True = replay ROUTE instead of reading keys


def route_targets(elapsed):
    """Return the (v, w) wanted at `elapsed` seconds after the start, taken
    from ROUTE. Returns (None, None) when the route is finished.
    (ALREADY WRITTEN)"""
    start = 0.0
    for v, w, seconds in ROUTE:              # ROUTE is a list of tuples
        if elapsed < start + seconds:
            return v, w
        start += seconds
    return None, None


def main():
    robot, motor = Robot(), Motor()
    connect()

    # A matplotlib window is needed even without the live plot, because the
    # keys are read from it.
    live = LivePlot() if USE_PLOT else None
    if live:
        fig = live.fig
    else:
        plt.ion()
        fig = plt.figure()
    fig.suptitle('Click here. Arrow keys drive, Esc stops. MODE = ' + MODE)
    setup_keys(fig)

    shaper = Shaper(robot, motor)
    log = Logger()
    t_start = time.time()

    try:
        # Keep going until Esc is pressed or the window is closed
        while not stop_requested() and plt.fignum_exists(fig.number):
            elapsed = time.time() - t_start

            # 1. what does the operator (or the route) want?
            if USE_ROUTE:
                v_target, w_target = route_targets(elapsed)
                if v_target is None:         # route finished
                    break
            else:
                v_target, w_target = read_targets()

            # 2. raw mode skips the filter, shaped mode uses it
            if MODE == 'shaped':
                v, w = shaper.step(v_target, w_target, DT)
            else:
                v, w = v_target, w_target

            # 3 + 4. wheel speeds, then send them to the robot
            wl, wr = wheel_speeds(v, w, robot)
            set_wheels(wl, wr)

            # 5. where is the robot now, and how fast is it REALLY going?
            x, y, yaw, t_sim, v_real, w_real = get_pose()

            # 6 + 7. record and draw (only if switched on above).
            # We log the MEASURED speed (v_real), not the commanded one, so the
            # energy is worked out from what the robot actually did.
            if USE_LOGGER:
                log.add(t_sim, x, y, v_real, w_real)
            if live:
                live.update(x, y)

            fig.canvas.flush_events()        # lets matplotlib deliver key presses
            time.sleep(DT)
    finally:
        # Runs even if something crashes, so the robot always stops
        stop()
        if USE_LOGGER:
            log.save('run_' + MODE + '.csv')
        print('Done.')


if __name__ == '__main__':
    main()


# ===========================================================================
# STAGE 6: put this in a NEW file called compare.py (it needs no simulator)
# ===========================================================================
#
#   from config import Robot, Motor
#   from logger import load
#   from model import energy_for_profile
#   from plots import comparison_figure
#
#   raw = load('run_raw.csv')
#   shaped = load('run_shaped.csv')
#   robot, motor = Robot(), Motor()
#
#   E_raw = energy_for_profile(raw['t'], raw['v'], robot, motor)[0]
#   E_shaped = energy_for_profile(shaped['t'], shaped['v'], robot, motor)[0]
#   # If the energies look wildly large, the measured speed is probably noisy.
#   # Smooth it first (ask for help the first time you do this):
#   #   v_smooth = np.convolve(v, np.ones(5) / 5, mode='same')
#   # The two runs may cover slightly different distances, so ALSO compare
#   # energy per metre (this is the fair number for the report):
#   #   import numpy as np
#   #   def distance(d):
#   #       return float(np.sum(np.hypot(np.diff(d['x']), np.diff(d['y']))))
#   #   print('J per metre raw / shaped:', E_raw / distance(raw), E_shaped / distance(shaped))
#   print('energy raw   :', E_raw, 'J')
#   print('energy shaped:', E_shaped, 'J')
#   print('saved', round(100 * (E_raw - E_shaped) / E_raw, 1), '% energy')
#   print('travel time raw / shaped:', raw['t'][-1] - raw['t'][0],
#         shaped['t'][-1] - shaped['t'][0], 's')
#   comparison_figure(raw, shaped, E_raw, E_shaped)
