#!/usr/bin/env python3

# The keypad buttons are malfunctioning, so they don't send the expected
# numbers when pressed. Multiple presses of the same button will produce
# different numbers, however, each button has its own sequence of numbers that
# it cycles through when pressed.

# Correct combination: 5841

sequences = {
    1: [2, 7, 9, 4, 8],
    2: [6, 8, 4, 3, 1],
    3: [7, 5, 5, 2, 5],
    4: [2, 8, 9, 2, 7],
    5: [6, 7, 4, 3, 2],
    6: [7, 5, 1, 2, 9],
    7: [3, 6, 5, 2, 4],
    8: [9, 7, 6, 5, 4],
    9: [6, 8, 1, 3, 6],
}
