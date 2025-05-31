# Collin Simpson @ 2025-05-31
# Solves the rotating tile safe puzzle in the museum (dollar sign image)
# Make sure the mouse is on the upper left dial before starting

import os
import time

from evdev import UInput
from evdev import ecodes as e
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

PIXEL_DIST = 84  # might require tweaking on other displays


def sub(a, b):
    return (b[0] - a[0], b[1] - a[1])


solution = (
    9, 1, 2, 4, 1, 0, 7, 2, 9, 14, 15, 4, 0, 1, 6, 6, 2, 6, 6, 11, 15, 11, 6,
    6, 9, 13, 9, 13, 9, 5, 0, 0, 6, 13, 13, 14, 12, 12, 13, 13, 13, 15, 11, 11,
    14, 13, 12, 15, 15, 15, 12, 13, 14, 14, 14, 15, 10, 2, 1, 6, 2, 2, 2, 3, 3,
    3, 1, 2, 3, 7, 7, 7, 11, 15, 11, 11, 7, 15, 15, 4, 4, 4, 8, 4, 0, 12, 12,
    13, 14, 14, 12, 13, 14, 14, 12, 12, 12, 13, 13, 13, 12, 3, 3, 3, 2, 3, 2,
    3, 3, 3, 2, 2, 2, 3, 3, 0, 1, 3, 2, 0, 0, 0, 13, 13, 14, 15, 13, 13, 15,
    15, 15, 13, 14, 15, 15, 14, 14, 14, 15, 13, 13, 13, 12, 12, 12
)

mouse = MouseController()

pressed_keys = set()

p1 = p2 = None


def on_press(key):
    global p1, p2
    pressed_keys.add(key)
    if Key.shift in pressed_keys and hasattr(key, 'char') and key.char == 'E':
        print("Shift + E pressed. Starting click sequence...")
        time.sleep(1)
        steps = (0, ) + solution
        for i in range(len(steps)):
            m1, m2 = steps[i], steps[i + 1]
            r1, c1 = divmod(m1, 4)
            r2, c2 = divmod(m2, 4)

            yoff = (r2 - r1) * PIXEL_DIST
            xoff = (c2 - c1) * PIXEL_DIST

            tar = (xoff, yoff)
            print('Moving mouse to', tar)
            mouse.position = tar
            click()
            # mouse.click(Button.left, 1)
            # pyautogui.click()
            time.sleep(0.2)
        # return False  # stop the listener

    # try:
    #     if key.char == 's':
    #         p2 = p1 or mouse.position
    #         p1 = mouse.position
    #         print('Saving mouse coordinate', (p1, p2))
    #     if key.char == 'c':
    #         v = sub(p2, p1)
    #         print("Moving mouse to", v)
    #         mouse.position = v
    #         # return False  # stop listener after completion
    # except AttributeError:
    #     pass


def on_release(key):
    pressed_keys.discard(key)


def click():
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)  # Press
    ui.syn()
    time.sleep(0.1)
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)  # Release
    ui.syn()


capabilities = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL: [e.REL_X, e.REL_Y]
}

ui = UInput(capabilities)
ui.syn()

print("Press Shift + E to start clicking...")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

ui.close()
