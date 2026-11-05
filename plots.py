"""
plots.py  -  see the robot live, and make the picture for the report
====================================================================

WHAT THIS FILE DOES
    LivePlot       while driving, draws the path of the robot in a window.
    comparison_figure   after two runs (raw and shaped), draws speed against
                   time for both and a bar chart of their energies. This is
                   the picture that goes in the report.

WHAT YOU HAVE TO DO
    TODO 1  LivePlot.update()
    TODO 2  comparison_figure()
    (LivePlot.__init__ is already written; read its comments to learn.)

IMPORTANT
    Redrawing a plot is SLOW. If we redraw every cycle the robot becomes
    jerky. So update() collects points every cycle but redraws only about
    5 times per second.

HOW TO TEST
    python plots.py  -> a window shows a dot moving around a circle, then the
                        comparison figure is saved as test_comparison.png.

USES: nothing from our other files.          PHASE: 1 and 5
"""

import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt


class LivePlot:
    def __init__(self):                          # ALREADY WRITTEN
        plt.ion()                                # interactive mode: do not freeze the program
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')  # an empty line we fill later
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        self.ax.set_aspect('equal')              # same scale on both axes
        self.ax.grid(True)
        # deque(maxlen=2000) = a list that forgets the oldest point when full
        self.xs = deque(maxlen=2000)
        self.ys = deque(maxlen=2000)
        self.last_draw = 0.0                     # time of the last redraw

    def update(self, x, y):
        """Called every control cycle with the robot position."""
        # TODO 1:
        #     self.xs.append(x)
        #     self.ys.append(y)
        #     self.fig.canvas.flush_events()          # keeps the window alive + keys working
        #     if time.time() - self.last_draw > 0.2:  # redraw only every 0.2 s
        #         self.line.set_data(self.xs, self.ys)
        #         self.ax.relim()
        #         self.ax.autoscale_view()
        #         self.fig.canvas.draw_idle()
        #         self.last_draw = time.time()
        raise NotImplementedError('TODO 1 in plots.py: write LivePlot.update()')


def comparison_figure(raw, shaped, E_raw, E_shaped, filename='comparison.png'):
    """Make and save the raw-versus-shaped figure.
        raw, shaped : dictionaries from logger.load()  (keys 't' and 'v')
        E_raw, E_shaped : the two energies in joules (worked out in main/model)
    """
    # TODO 2:
    #     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    #     ax1.plot(raw['t'], raw['v'], label='raw keys')
    #     ax1.plot(shaped['t'], shaped['v'], label='DriveBot')
    #     ax1.set_xlabel('time (s)')
    #     ax1.set_ylabel('speed (m/s)')
    #     ax1.legend()
    #     ax1.grid(True)
    #     ax2.bar(['raw keys', 'DriveBot'], [E_raw, E_shaped])
    #     ax2.set_ylabel('energy (J)')
    #     fig.savefig(filename, dpi=200, bbox_inches='tight')
    #     print('Saved', filename)
    raise NotImplementedError('TODO 2 in plots.py: write comparison_figure()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python plots.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    live = LivePlot()
    for k in range(200):
        angle = k * 0.05
        live.update(np.cos(angle), np.sin(angle))      # a circle
        time.sleep(0.02)

    t = np.linspace(0, 4, 100)
    fake_raw = {'t': t, 'v': np.minimum(t, 1.0)}
    fake_shaped = {'t': t, 'v': np.sin(t / 4 * np.pi)}
    comparison_figure(fake_raw, fake_shaped, 230.0, 154.0, 'test_comparison.png')
