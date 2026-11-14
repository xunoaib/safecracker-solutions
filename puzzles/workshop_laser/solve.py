def make(*r):
    return tuple(range(*r))


RANGES = [
    VIOLET := make(401, 447),
    BLUE := make(447, 501),
    GREEN := make(501, 579),
    YELLOW := make(579, 593),
    ORANGE := make(593, 621),
    RED := make(621, 701),
]

print(YELLOW[-1] - 8)
