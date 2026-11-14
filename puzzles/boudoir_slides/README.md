# Boudoir: Sliding Puzzle

[← Previous: Blue Bedroom - Mastermind Phone](../mastermind_phone) | [Next: Violet Bedroom - Final Safe →](../door_digits)

![Screenshot](ss.jpg)

## Solution

**Objective:** Free the key block by sliding it to an opening on the right edge.

**Rules:** A [Rush-Hour-style](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)) sliding block puzzle on a 6x6 grid. Tiles can only be slid back and forth lengthwise.

**Solution:**

Check [solve.py] to see which letters correspond to each tile.

```
i left x1     B down x1     k left x1     G up x2
H up x1       l right x1    E down x3     j right x1
C down x1     i left x2     F up x1       k right x2
C down x3     j left x1     k left x2     E up x4
j right x1    l left x1     H down x1     k right x3
D up x1       C up x3       B up x1       l left x3
D down x1     k left x2     F down x3     j right x2
```
