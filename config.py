"""
config.py  -  ALL shared numbers live here (and ONLY here)
==========================================================

WHAT THIS FILE DOES
    Stores the robot size, the motor constants, the speed limits, the key map
    and the test route. Every other file does  `from config import ...`
    so a number is typed once and never twice.

WHAT YOU HAVE TO DO
    Step 1. Look at every line marked  # CHECK  and replace the guess with a
            real value (measure the robot in your CoppeliaSim scene, or take
            it from a motor datasheet).
    Step 2. Nothing else. Do NOT put calculations in this file.

HOW TO TEST
    python config.py      ->  it prints every value. If it prints, you are done.

USED BY: every other file.        PHASE: 1 and 2
"""

from dataclasses import dataclass


@dataclass
class Motor:
    """Numbers that describe ONE wheel motor."""
    R: float = 1.0        # winding resistance, ohm            # CHECK (guess)
    Ke: float = 0.05      # back-EMF constant, V*s/rad         # CHECK (guess)
    Kt: float = 0.05      # torque constant, N*m/A             # CHECK (guess)
    V_max: float = 12.0   # highest voltage it can get, volts  # CHECK


@dataclass
class Robot:
    """Numbers that describe the robot body."""
    r: float = 0.0975     # wheel radius, metres               # CHECK in scene
    L: float = 0.381      # distance between the wheels, m     # CHECK in scene
    m: float = 10.0       # mass, kg                           # CHECK (guess)
    b: float = 2.0        # viscous friction, N*s/m            # CHECK (guess)


# ---- Limits: the operator can never ask for more than this ----------------
MAX_V = 1.0        # fastest forward speed, m/s
MAX_W = 1.0        # fastest turning speed, rad/s
MAX_A = 0.5        # biggest change of forward speed per second, m/s^2
MAX_ALPHA = 1.0    # biggest change of turning speed per second, rad/s^2

# How long the motors need to get up to speed when a key is just pressed.
# This is an ASSUMPTION for the "raw" profile in profiles.py. Write the value
# you chose in your report, because the raw energy depends on it.
RAW_RAMP = 0.6     # seconds

# ---- Keyboard -------------------------------------------------------------
# key name -> (forward direction, turn direction)
KEYMAP = {
    'up':    (1, 0),
    'down':  (-1, 0),
    'left':  (0, 1),
    'right': (0, -1),
}
STOP_KEY = 'escape'

# ---- Timing ---------------------------------------------------------------
DT = 0.05          # how often the control loop runs, in seconds

# ---- Test route -----------------------------------------------------------
# Replays the SAME trip in raw mode and shaped mode, so the comparison is fair.
# Each item is (forward speed m/s, turn speed rad/s, how long in seconds).
ROUTE = [
    (0.8, 0.0, 3.0),
    (0.0, 0.0, 1.0),
    (0.8, 0.0, 3.0),
    (0.0, 0.0, 1.0),
]


if __name__ == '__main__':
    print(Motor())
    print(Robot())
    print('limits:', MAX_V, MAX_W, MAX_A, MAX_ALPHA, 'raw ramp:', RAW_RAMP)
    print('keys:', KEYMAP)
    print('route:', ROUTE)
