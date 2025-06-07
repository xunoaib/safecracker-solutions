# Collin Simpson @ 2025-05-31
# Solves the rotating tile safe puzzle in the museum (dollar sign image)
# Make sure the mouse is on the upper left dial before starting

# NOTE: the game doesn't register pynput mouse events, so evdev is used.
# permissions may need to be changed on /dev/uinput for this to work

import sys
import time

from evdev import UInput
from evdev import ecodes as e
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller as MouseController
from solve import BEST_KNOWN_SOLUION

PIXEL_DIST = 84  # might require tweaking on other displays
PAUSE_FOR_DIALOGUE = '-p' in sys.argv


def sub(a, b):
    return (b[0] - a[0], b[1] - a[1])


mouse = MouseController()

pressed_keys = set()


def on_press(key):
    pressed_keys.add(key)
    if Key.shift in pressed_keys and hasattr(key, 'char') and key.char == 'E':
        print("Shift + E pressed. Starting click sequence...")
        time.sleep(1)
        steps = (0, ) + BEST_KNOWN_SOLUION
        for i in range(len(steps) - 1):
            m1, m2 = steps[i], steps[i + 1]
            r1, c1 = divmod(m1, 4)
            r2, c2 = divmod(m2, 4)

            yoff = (r2 - r1) * PIXEL_DIST
            xoff = (c2 - c1) * PIXEL_DIST

            print('Moving mouse to', (xoff, yoff))
            mouse.position = (xoff, yoff)
            click()
            time.sleep(0.09)

            if PAUSE_FOR_DIALOGUE and i + 1 == 18:
                print('Pausing for dialogue...')
                time.sleep(4.5)


def on_release(key):
    pressed_keys.discard(key)


def click():
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)  # Press
    ui.syn()
    time.sleep(0.15)
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)  # Release
    ui.syn()


capabilities = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL: [e.REL_X, e.REL_Y]
}

ui = UInput(capabilities)
ui.syn()

if PAUSE_FOR_DIALOGUE:
    print('Script WILL pause after 18 moves for dialogue')
else:
    print('Script will NOT pause after 18 moves for dialogue')

print("Press Shift + E to start clicking...")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

ui.close()
