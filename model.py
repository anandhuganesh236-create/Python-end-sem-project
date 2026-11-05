"""
model.py  -  the physics: how much ENERGY does a speed profile cost?
====================================================================

WHAT THIS FILE DOES
    Pure maths, no simulator needed. It answers two questions:
      1. "If I apply this voltage, how does the robot move?"   (forward model)
      2. "If the robot follows this speed curve, how much energy does it use?"
                                                               (inverse model)
    Also turns (v, w) into the two wheel speeds.

THE IDEAS IN PLAIN WORDS
    motor:   V = i*R + Ke*omega     voltage = resistance part + back-EMF
    torque:  tau = Kt * i           current makes force
    robot:   m * dv/dt = 2*Kt*i/r - b*v     force pushes, friction resists
    energy:  E = integral of power over time, power = V * i

WHAT YOU HAVE TO DO  (do them in this order, test after each)
    TODO 1  wheel_speeds()          two lines
    TODO 2  deriv()                 the forward model
    TODO 3  rk4_step()              like euler_step but more accurate
    TODO 4  energy_for_profile()    the important one
    euler_step() is already written as an example.

HOW TO TEST
    python model.py   -> prints a few numbers. The expected values are in the
                         comments next to each print (they are for the guess
                         values in config.py, so they change if you change those).

USES: config.py          PHASE: 2
"""

import numpy as np
from config import Motor, Robot

# NumPy 2.x calls the integral function np.trapezoid, older NumPy np.trapz.
# (ALREADY WRITTEN) Use  trapezoid(y, t)  below.
trapezoid = getattr(np, 'trapezoid', None) or np.trapz


def wheel_speeds(v, w, robot):
    """Turn robot speeds into wheel speeds.
        v : forward speed, m/s          w : turning speed, rad/s
        returns (wl, wr) : left and right wheel speed in rad/s
    """
    # TODO 1: with r = robot.r and L = robot.L
    #     wl = (v - w * L / 2) / r
    #     wr = (v + w * L / 2) / r
    #     return wl, wr
    raise NotImplementedError('TODO 1 in model.py: write wheel_speeds()')


def deriv(t, y, V, robot, motor):
    """How fast things change right now (the 'slope').
        y = [x, v]   position and speed
        V = voltage on each motor
        returns np.array([dx/dt, dv/dt]) = [v, a]
    """
    # TODO 2:
    #     x, v = y
    #     omega = v / robot.r                          # wheel speed
    #     i = (V - motor.Ke * omega) / motor.R         # motor current
    #     F = 2 * motor.Kt * i / robot.r               # both wheels push
    #     a = (F - robot.b * v) / robot.m              # acceleration
    #     return np.array([v, a])
    raise NotImplementedError('TODO 2 in model.py: write deriv()')


def euler_step(f, t, y, h, *args):
    """One Euler step: go along the slope for a time h. (ALREADY WRITTEN)
    f is a function like deriv, h is the step size in seconds."""
    return y + h * f(t, y, *args)


def rk4_step(f, t, y, h, *args):
    """One RK4 step: look at the slope 4 times and average. Much more accurate."""
    # TODO 3:
    #     k1 = f(t,         y,              *args)
    #     k2 = f(t + h / 2, y + h / 2 * k1, *args)
    #     k3 = f(t + h / 2, y + h / 2 * k2, *args)
    #     k4 = f(t + h,     y + h * k3,     *args)
    #     return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    raise NotImplementedError('TODO 3 in model.py: write rk4_step()')


def energy_for_profile(t, v, robot, motor):
    """Energy needed to follow a speed curve (the inverse model).
        t : array of times (s)       v : array of speeds (m/s)
        returns (E, V, i, feasible)
            E        energy in joules
            V        voltage needed at every time (array)
            i        current needed at every time (array)
            feasible True if the voltage never goes above motor.V_max
    """
    # TODO 4: go step by step, every line works on whole arrays at once
    #     a = np.gradient(v, t)                       # acceleration from speed
    #     F = robot.m * a + robot.b * v               # force needed
    #     i = F * robot.r / (2 * motor.Kt)            # current in each motor
    #     V = i * motor.R + motor.Ke * v / robot.r    # voltage needed
    #     P = 2 * V * i                               # power of both motors, watts
    #     E = trapezoid(np.clip(P, 0, None), t)       # add up power over time
    #                                                 # (clip: braking gives nothing back)
    #     feasible = bool(np.all(np.abs(V) <= motor.V_max))
    #     return E, V, i, feasible
    raise NotImplementedError('TODO 4 in model.py: write energy_for_profile()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python model.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    robot, motor = Robot(), Motor()

    # Test 1 - wheel speeds (needs TODO 1)
    print('straight:', wheel_speeds(1.0, 0.0, robot))   # two EQUAL numbers (about 10.26)
    print('turning :', wheel_speeds(0.0, 1.0, robot))   # left negative, right positive (about -1.95, 1.95)

    # Test 2 - drive with 2 volts for 5 seconds (needs TODO 2, then TODO 3)
    for name, step in (('Euler', euler_step), ('RK4', rk4_step)):
        y = np.array([0.0, 0.0])        # start at rest: [position, speed]
        h = 0.01
        for k in range(500):            # 500 steps * 0.01 s = 5 s
            y = step(deriv, k * h, y, h, 2.0, robot, motor)
        print(name, 'speed after 5 s:', round(y[1], 3))   # about 0.58 m/s for both

    # Test 3 - same drive, but a BIG step of 0.5 s: RK4 should stay near 0.582
    for name, step in (('Euler', euler_step), ('RK4', rk4_step)):
        y = np.array([0.0, 0.0])
        for k in range(10):
            y = step(deriv, k * 0.5, y, 0.5, 2.0, robot, motor)
        print(name, 'with big steps:', round(y[1], 3))    # Euler about 0.60, RK4 about 0.582

    # Test 4 - energy of a smooth (parabolic) trip: 2 m in 4 s (needs TODO 4)
    d, T = 2.0, 4.0
    t = np.linspace(0, T, 401)
    v = 6 * d * t * (T - t) / T**3
    E, V, i, feasible = energy_for_profile(t, v, robot, motor)
    print('parabolic energy:', round(E, 1), 'J, feasible:', feasible)   # about 154 J, True
