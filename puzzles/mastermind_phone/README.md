# Blue Bedroom: Mastermind Phone

[← Previous: Dressing Room - Polybius](../polybius) | [Next: Boudoir - Sliding Puzzle →](../boudoir_slides)

![Screenshot](ss.jpg)

## Solution

The phone's 4-digit code is randomized each playthrough, so there is no fixed answer -- instead, use `solve.py` as a Mastermind solver. Known constraints learned from play: the last digit is always `9`, and all 4 digits are distinct.

1. Run `python solve.py -i`.
2. Enter the opening guess `1234` on the phone and read back its feedback per digit (wrong / present-but-wrong-position / correct-position).
3. Feed that feedback into the script as a `w`/`p`/`c` string; it narrows the remaining candidates and proposes the next best guess (minimizing the worst-case remaining candidates).
4. Repeat until only one candidate remains -- that's the code.
