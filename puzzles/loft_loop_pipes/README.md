# Loft: Metal Loop Safe

[← Previous: East Corridor - Metal Wheel Door](../upstairs_wheels) | [Next: Loft - Six Queens →](../loft_queens)

![Screenshot](ss.jpg)

## Solution

The safe is a 5x5 grid of rotatable pipe tiles; each tile must be turned so its loop connects to its neighbors all the way around. Rotate each tile clockwise by the number of quarter-turns shown below (row-major, top-left to bottom-right):

```
3 . 2 2 1
1 2 2 3 1
1 . 1 2 1
. 1 . . 1
. . . 1 2
```
