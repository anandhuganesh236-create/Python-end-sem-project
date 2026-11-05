"""
sim_link.py  -  the ONLY file that talks to CoppeliaSim
=======================================================

WHAT THIS FILE DOES
    Four small jobs:
        connect()          open the link and find the robot + its two motors
        get_pose()         read where the robot is
        set_wheels(wl,wr)  tell the two wheels how fast to spin
        stop()             both wheels to zero
    No other file imports the CoppeliaSim client. If the simulator changes,
    only this file changes.

WHAT YOU HAVE TO DO
    TODO 1  write get_pose()
    TODO 2  write set_wheels()
    TODO 3  write stop()
    (connect() is already written, it is your working connection test.)
    Also check the three PATH names below against the scene hierarchy in
    CoppeliaSim. If connect() says "object does not exist", call
    list_objects() and copy the exact path it prints.

BEFORE YOU RUN
    CoppeliaSim open, scene loaded, PLAY pressed, and the robot's own
    built-in script disabled (otherwise it fights your commands).

HOW TO TEST
    python sim_link.py   ->  prints (x, y, yaw, t, v, w) 5 times, spins both
                             wheels for 2 seconds, then stops them.

USES: config.py is not needed here.      PHASE: 1
"""

import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# These are filled in by connect() and used by the other functions below.
sim = None
robot_handle = None
left_handle = None
right_handle = None

# CHECK these names in the scene hierarchy (left panel in CoppeliaSim).
ROBOT_PATH = '/PioneerP3DX'
LEFT_PATH = '/PioneerP3DX/leftMotor'
RIGHT_PATH = '/PioneerP3DX/rightMotor'


def connect():
    """Open the link and find the handles. (ALREADY WRITTEN)

    A 'handle' is just a number CoppeliaSim gives each object so we can talk
    about it. 'global' lets this function fill in the variables at the top.
    """
    global sim, robot_handle, left_handle, right_handle
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    robot_handle = sim.getObject(ROBOT_PATH)
    left_handle = sim.getObject(LEFT_PATH)
    right_handle = sim.getObject(RIGHT_PATH)
    print('Connected to CoppeliaSim')


def list_objects():
    """Print every object path in the scene. (ALREADY WRITTEN)
    Use it when connect() cannot find a name."""
    for handle in sim.getObjectsInTree(sim.handle_scene):
        print(sim.getObjectAlias(handle, 1))


def get_pose():
    """Return (x, y, yaw, t, v, w).
        x, y : position in metres
        yaw  : heading in radians
        t    : simulator time in seconds
        v    : MEASURED forward speed in m/s     (what the robot really does,
        w    : MEASURED turning speed in rad/s     not what we asked for)
    """
    # TODO 1: fill this in. The calls you need:
    #     x, y, z = sim.getObjectPosition(robot_handle, sim.handle_world)
    #     yaw = sim.getObjectOrientation(robot_handle, sim.handle_world)[2]
    #     t = sim.getSimulationTime()
    #     lin, ang = sim.getObjectVelocity(robot_handle)        # velocities in the world frame
    #     v = lin[0] * math.cos(yaw) + lin[1] * math.sin(yaw)   # the part along the heading
    #     w = ang[2]                                            # turning around the vertical axis
    #     return x, y, yaw, t, v, w
    # (If getObjectVelocity gives an error in your CoppeliaSim version, tell us.)
    raise NotImplementedError('TODO 1 in sim_link.py: write get_pose()')


def set_wheels(wl, wr):
    """Spin the left wheel at wl and the right wheel at wr (rad/s)."""
    # TODO 2: one call per motor:
    #     sim.setJointTargetVelocity(left_handle, wl)
    #     sim.setJointTargetVelocity(right_handle, wr)
    raise NotImplementedError('TODO 2 in sim_link.py: write set_wheels()')


def stop():
    """Both wheels to zero. main.py calls this in 'finally', so the robot
    always stops, even if the program crashes."""
    # TODO 3: one line, reuse your own function:  set_wheels(0.0, 0.0)
    raise NotImplementedError('TODO 3 in sim_link.py: write stop()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python sim_link.py   (not when imported)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import time

    connect()
    try:
        for _ in range(5):
            print(get_pose())
            time.sleep(0.5)
        print('Spinning wheels for 2 seconds...')
        set_wheels(2.0, 2.0)
        time.sleep(2)
    finally:
        stop()
        print('Stopped.')
