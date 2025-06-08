from itertools import permutations

# Worn keypad reveals likely keys: 3, 4, 8

digits = [3, 4, 8]

for p in permutations(digits):
    print(''.join(map(str, p)))
