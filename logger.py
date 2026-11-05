"""
logger.py  -  remember every control cycle, save it as a CSV file
=================================================================

WHAT THIS FILE DOES
    While the robot drives, add() stores one row per cycle: time, position,
    speed, turn speed. After the run, save() writes them to a .csv file (you
    can open it in Excel). load() reads a saved file back into arrays so you
    can plot it or work out its energy. Raw and shaped runs are saved to
    different files and compared later.

WHAT YOU HAVE TO DO
    TODO 1  Logger.add()
    TODO 2  Logger.save()
    TODO 3  load()
    (Logger.__init__ is already written.)

HOW TO TEST
    python logger.py  -> writes test_log.csv with 5 made-up rows, reads it back
                         and prints the speed column: [0. 0.1 0.2 0.3 0.4]

USES: nothing from our other files.          PHASE: 1 and 5
"""

import csv
import numpy as np

HEADER = ['t', 'x', 'y', 'v', 'w']     # the column names, in order


class Logger:
    def __init__(self):                  # ALREADY WRITTEN
        self.rows = []                   # a list that will hold one row per cycle

    def add(self, t, x, y, v, w):
        """Store one cycle: time, position, MEASURED speed v and MEASURED turn
        speed w (the numbers from sim_link.get_pose()).
        Called inside the control loop, so keep it FAST (just add to the list,
        never write to a file here)."""
        # TODO 1:  self.rows.append([t, x, y, v, w])
        raise NotImplementedError('TODO 1 in logger.py: write Logger.add()')

    def save(self, path):
        """Write everything to a CSV file. Called ONCE, after the run."""
        # TODO 2:
        #     with open(path, 'w', newline='') as f:
        #         writer = csv.writer(f)
        #         writer.writerow(HEADER)        # first line: the column names
        #         writer.writerows(self.rows)    # then all the data rows
        #     print('Saved', len(self.rows), 'rows to', path)
        raise NotImplementedError('TODO 2 in logger.py: write Logger.save()')


def load(path):
    """Read a CSV written by save(). Returns a dictionary of NumPy arrays:
        data = load('run_raw.csv');   data['t'], data['x'], data['v'] ...
    """
    # TODO 3:
    #     data = {name: [] for name in HEADER}       # {'t': [], 'x': [], ...}
    #     with open(path, newline='') as f:
    #         for row in csv.DictReader(f):          # each row is a dictionary
    #             for name in HEADER:
    #                 data[name].append(float(row[name]))
    #     return {name: np.array(values) for name, values in data.items()}
    raise NotImplementedError('TODO 3 in logger.py: write load()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python logger.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    log = Logger()
    for k in range(5):
        log.add(k * 0.1, k, 2 * k, k * 0.1, 0.0)    # made-up numbers
    log.save('test_log.csv')
    data = load('test_log.csv')
    print(data['v'])
