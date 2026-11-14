# Workshop: Malfunctioning Keypad

[← Previous: Office - Arrow Keypad](../directional_keypad) | [Next: Workshop - Laser Safe →](../laser)

## Solution

The keypad is malfunctioning: pressing a button doesn't enter its number — each button instead cycles through its own fixed sequence of digits every time it's pressed. The actual code we need to produce is `5841`. We get there by pressing buttons enough times each to cycle them onto the right digits.

**Solution:** `5841`

One valid button-press sequence (press these buttons in order) that lands on `5841`:
```
3299 3229
```

![Screenshot](ss.jpg)
