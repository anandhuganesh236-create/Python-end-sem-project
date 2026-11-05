"""
keys.py  -  turns the keys you hold down into the speeds you WANT
=================================================================

WHAT THIS FILE DOES
    The matplotlib window tells us when a key goes down and up. We keep a
    set called `pressed` with the keys that are down right now.
    read_targets() looks at that set and answers:
        "how fast does the operator want to go (v) and turn (w)?"
    These are only the WANTED speeds. The robot does not get them directly,
    shaper.py smooths them first.

WHAT YOU HAVE TO DO
    TODO 1  (optional) learn first: search "matplotlib event handling" and
            make a tiny script that prints event.key for every key you press.
    TODO 2  write read_targets()
    (everything else is already written)

HOW TO TEST
    python keys.py   -> a plot window opens. CLICK ON IT, then hold the arrow
                        keys. The numbers printed in the terminal must change.
                        Press Esc to see the stop message.

USES: config.py          PHASE: 1
"""

import time
import matplotlib.pyplot as plt
from config import KEYMAP, MAX_V, MAX_W, STOP_KEY

# The keys that are held down right now. A 'set' holds each item only once.
pressed = set()


def on_press(event):
    """matplotlib calls this when a key goes DOWN. (ALREADY WRITTEN)"""
    pressed.add(event.key)


def on_release(event):
    """matplotlib calls this when a key comes UP. (ALREADY WRITTEN)"""
    pressed.discard(event.key)


def setup_keys(fig):
    """Hook the two functions above to a matplotlib figure. (ALREADY WRITTEN)

    matplotlib has its own shortcuts (left/right = history, s = save, q = quit).
    We switch them off so they do not interfere with driving.
    """
    for name in ('keymap.back', 'keymap.forward', 'keymap.save', 'keymap.quit'):
        plt.rcParams[name] = []
    fig.canvas.mpl_connect('key_press_event', on_press)
    fig.canvas.mpl_connect('key_release_event', on_release)


def stop_requested():
    """True when the stop key is held. (ALREADY WRITTEN)"""
    return STOP_KEY in pressed


def read_targets():
    """Return (v_target, w_target) from the keys held down right now.

    v_target : wanted forward speed in m/s   (negative = reverse)
    w_target : wanted turning speed in rad/s (positive = turn left)
    """
    # TODO 2: write this. A way to do it:
    #     v = 0.0
    #     w = 0.0
    #     for key in pressed:
    #         if key in KEYMAP:            # ignore keys that are not arrows
    #             dv, dw = KEYMAP[key]     # e.g. 'up' gives (1, 0)
    #             v += dv
    #             w += dw
    #     return v * MAX_V, w * MAX_W
    # Think: what happens if 'up' and 'down' are both held? (they cancel, ok)
    raise NotImplementedError('TODO 2 in keys.py: write read_targets()')


# ---------------------------------------------------------------------------
# Test: only runs when you type  python keys.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title('Click here, then hold the arrow keys. Esc = stop')
    setup_keys(fig)

    while plt.fignum_exists(fig.number):
        fig.canvas.flush_events()      # lets matplotlib deliver key events
        if stop_requested():
            print('Stop key pressed')
            break
        print(read_targets())
        time.sleep(0.2)
