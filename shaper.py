"""
shaper.py  -  the DriveBot filter (the new idea of the project)
===============================================================

WHAT THIS FILE DOES
    Sits between the keys and the wheels. The operator's keys say "go 1 m/s
    NOW". The shaper does not obey instantly. Every control cycle it moves the
    speed TOWARD the wanted value, but by no more than a small amount. So the
    robot ramps up and down smoothly, and the operator still decides where it
    goes.

    Each cycle:   gap = target - current
                  change = gap, but never more than  max_acceleration * dt
                  current = current + change

WHAT YOU HAVE TO DO
    TODO 1  approach()      the 'move toward but not too fast' helper
    TODO 2  Shaper.step()   use approach() for v and for w
    TODO 3  (later, upgrade) follow the parabolic profile instead of a straight
            ramp. Only after the whole project already works.

HOW TO TEST
    python shaper.py  -> asks for speed 1.0 for 60 cycles, then 0.0 for 60
                         cycles, and plots the result: a ramp up, a flat part,
                         a ramp down. NOT a sudden jump.

USES: config.py          PHASE: 4
"""

import numpy as np
from config import MAX_A, MAX_ALPHA


def approach(current, target, max_change):
    """Move `current` toward `target`, by at most `max_change`. Returns the new value."""
    # TODO 1:
    #     delta = np.clip(target - current, -max_change, max_change)
    #     return current + delta
    # np.clip(x, low, high) cuts x down to stay between low and high.
    raise NotImplementedError('TODO 1 in shaper.py: write approach()')


class Shaper:
    """Remembers the current speeds between cycles. (A 'class' is a function
    group that keeps its own variables. self.v is 'the speed right now'.)"""

    def __init__(self, robot, motor):          # ALREADY WRITTEN
        self.robot = robot
        self.motor = motor
        self.v = 0.0    # current forward speed, m/s
        self.w = 0.0    # current turning speed, rad/s

    def step(self, v_target, w_target, dt):
        """One control cycle. Returns the smoothed (v, w) to send to the wheels."""
        # TODO 2:
        #     self.v = approach(self.v, v_target, MAX_A * dt)
        #     self.w = approach(self.w, w_target, MAX_ALPHA * dt)
        #     return self.v, self.w
        raise NotImplementedError('TODO 2 in shaper.py: write Shaper.step()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python shaper.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from config import Robot, Motor

    shaper = Shaper(Robot(), Motor())
    dt = 0.05
    speeds = []
    for _ in range(60):
        v, w = shaper.step(1.0, 0.0, dt)     # operator holds the key
        speeds.append(v)
    for _ in range(60):
        v, w = shaper.step(0.0, 0.0, dt)     # operator lets go
        speeds.append(v)

    plt.plot(np.arange(len(speeds)) * dt, speeds)
    plt.xlabel('time (s)')
    plt.ylabel('speed (m/s)')
    plt.title('Should ramp up, hold, ramp down (no jumps)')
    plt.grid(True)
    plt.show()
