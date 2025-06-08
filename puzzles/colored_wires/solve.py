# Each colored wire is in the shape of a digit. Digits are ordered from the
# topmost color to the bottommost color (ie: green wires are on top, then
# yellow, blue, and red)

DIGITS = [
    green := 2,
    yellow := 4,
    blue := 9,
    red := 3,
]

# from itertools import permutations
# for p in permutations(DIGITS):
#     print(*p, sep='')

print(*DIGITS, sep='')
