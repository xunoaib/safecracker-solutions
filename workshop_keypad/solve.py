#!/usr/bin/env python3
from itertools import batched

# The keypad buttons are malfunctioning, so they don't send the expected
# numbers when pressed. Multiple presses of the same button will produce
# different numbers, however, each button has its own sequence of numbers that
# it cycles through when pressed.

# Correct combination: 5841


def press(number, times=1):
    for _ in range(times):
        sequences[number] = sequences[number][1:] + sequences[number][:1]


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

combination = [5, 8, 4, 1]
avail = set(sequences)
solution = []
final_seq = []

# advance final combination buttons to the correct positions
for c in combination:
    num = min(
        avail,
        key=lambda v: sequences[v].index(c)
        if c in sequences[v] else float('inf')
    )
    solution += [num] * sequences[num].index(c)
    final_seq.append(num)
    press(num, sequences[num].index(c))
    avail.remove(num)

# press other buttons for filler parity
while rem := len(solution) % 4:
    solution = [min(avail)] * rem + solution

solution += final_seq

for b in batched(solution, 4):
    print(''.join(map(str, b)), end=' ')
print()
