# Museum: Currency

[← Previous: Museum - Dollar Safe](../rotating_symbol_tiles) | [Next: Museum - Square Numbers →](../museum_square_numbers)

## Solution

A 4x4 grid where each cell cycles through 5 states (blank, then four currency symbols) when clicked. Four cells are pre-filled as givens. Solve it like a Sudoku square so each row and column contains all four currency symbols exactly once:

```
E Y L S
L S E Y
S L Y E
Y E S L
```

Equivalently, the number of times to click each blank cell to cycle to the right symbol:

```
2 4 3 .
3 1 . 4
1 . 4 2
. 2 1 3
```

![Screenshot](ss.jpg)
