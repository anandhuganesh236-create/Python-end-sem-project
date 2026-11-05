"""
profiles.py  -  speed-versus-time curves for the same trip
==========================================================

WHAT THIS FILE DOES
    Builds speed curves for a trip of distance d metres in T seconds, so
    model.py can score each one with an energy number:
        raw_profile        what a key press does: speed up fast, cruise, stop fast
        parabolic_profile  the smooth ideal curve (closed-form formula)
        optimal_profile    the numerical best with friction + limits (STRETCH)
    Each function returns two arrays: t (times) and v (speeds).

WHAT YOU HAVE TO DO
    TODO 1  raw_profile()
    TODO 2  parabolic_profile()
    (optimal_profile is a stretch goal. Skip it until everything else works.)

HOW TO TEST
    python profiles.py  -> prints the distance and energy of both curves and
                           shows a plot. Both distances must be about 2.0 m.

USES: config.py, model.py          PHASE: 3
"""

import numpy as np
from config import Motor, Robot, RAW_RAMP
from model import energy_for_profile, trapezoid


def raw_profile(d, T, dt, ramp=RAW_RAMP):
    """Key-press style trip: speed up in `ramp` seconds, cruise, slow down in
    `ramp` seconds. The cruise speed is chosen so the distance comes out as d.
    Returns (t, v).
    """
    # TODO 1:
    #     t = np.linspace(0, T, int(round(T / dt)) + 1)     # time array
    #     v_cruise = d / (T - ramp)                         # speed that gives distance d
    #     # a trapezoid: rises for `ramp` s, flat, falls for `ramp` s
    #     v = np.minimum(np.minimum(t / ramp, (T - t) / ramp), 1.0) * v_cruise
    #     return t, v
    # Why not "jump to d/T instantly"? That needs infinite acceleration, so the
    # energy would depend on dt and the voltage would be impossible.
    raise NotImplementedError('TODO 1 in profiles.py: write raw_profile()')


def parabolic_profile(d, T, dt):
    """The smooth curve v(t) = 6*d*t*(T - t) / T**3 (no friction, no limits).
    Returns (t, v).
    """
    # TODO 2:
    #     t = np.linspace(0, T, int(round(T / dt)) + 1)
    #     v = 6 * d * t * (T - t) / T**3
    #     return t, v
    raise NotImplementedError('TODO 2 in profiles.py: write parabolic_profile()')


def optimal_profile(d, T, robot, motor):
    """STRETCH GOAL: let scipy.optimize.minimize find the cheapest curve that
    still covers d in T seconds and ends at rest, within the motor limits.
    Ask for help (with your working code for TODO 1 and 2) when you get here."""
    raise NotImplementedError('optimal_profile() is a stretch goal')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python profiles.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    robot, motor = Robot(), Motor()
    d, T, dt = 2.0, 4.0, 0.01

    t1, v1 = raw_profile(d, T, dt)
    t2, v2 = parabolic_profile(d, T, dt)

    for name, t, v in (('raw', t1, v1), ('parabolic', t2, v2)):
        E, V, i, feasible = energy_for_profile(t, v, robot, motor)
        print(name, ': distance', round(trapezoid(v, t), 3), 'm,',
              'energy', round(E, 1), 'J, feasible', feasible)
    # about:  raw 229 J,  parabolic 154 J,  both feasible, both 2.0 m

    plt.plot(t1, v1, label='raw key press')
    plt.plot(t2, v2, label='parabolic')
    plt.xlabel('time (s)')
    plt.ylabel('speed (m/s)')
    plt.legend()
    plt.grid(True)
    plt.show()
