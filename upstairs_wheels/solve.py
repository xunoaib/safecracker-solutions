# Upstairs 5-wheel puzzle.
# 5 wheels, 6 bars

# Each wheel alternates between moving two sets of bars.
# Each bar SEEMS to be in either a "retracting" or "extending" state,
# until it reaches a maximum position (left or right), where it will
# then reverse direction.

# Wheels are numbered from 0-4 from top to bottom
# Bars are numberes from 0-5 from top to bottom

NUM_WHEELS = 5
NUM_BARS = 6

MIN_BAR_VAL = 0
MAX_BAR_VAL = 2

# Sequence of bar positions. Position 1 technically has two states, as it can
# be retracting or extending.
# 2 = fully closed
# 1 = retracting
# 0 = fully open
# 1 = extending
BAR_POS_SEQUENCE = (2, 1, 0, 1)

# bars moved by each wheel on each wheel turn
# wheel => (bars1, bars2)
WHEEL_BARS = {
    0: ((0, 3), (4, 5)),
    1: ((3, 4), (0, 4)),
    2: ((1, 2), (0, 3)),
    3: ((1, 5), (0, 1)),
    4: ((2, 4), (0, 3))
}

NUM_WHEEL_STATES = len(WHEEL_BARS[0])  # 2

START_BAR_IDXS = (0, ) * NUM_BARS  # BAR_SEQUENCE[0] = 2 (closed)
GOAL_BAR_IDXS = (2, ) * NUM_BARS  # BAR_SEQUENCE[2] = 0 (open)
START_WHEELS = (0, ) * NUM_WHEELS
START_STATE = (START_BAR_IDXS, START_WHEELS)


def rotate_wheel(state, wheel: int):
    bar_seq_idxs, wheels = map(list, state)

    wheel_seq_idx = wheels[wheel]
    # advance wheel state
    wheels[wheel] = (wheels[wheel] + 1) % NUM_WHEEL_STATES

    for bar_id in WHEEL_BARS[wheel][wheel_seq_idx]:
        # advance bar state
        bar_seq_idxs[bar_id] = (bar_seq_idxs[bar_id]
                                + 1) % len(BAR_POS_SEQUENCE)

    return tuple(bar_seq_idxs), tuple(wheels)


def neighbors(state):
    for wheel in range(NUM_WHEELS):
        yield rotate_wheel(state, wheel), wheel


def solve(state: tuple[tuple, tuple]):
    visited = {state}
    q = [(state, tuple())]

    while q:
        state, path = q.pop(0)
        bars, wheels = state
        if bars == GOAL_BAR_IDXS:
            return path

        for n, move in neighbors(state):
            if n not in visited:
                visited.add(n)
                q.append((n, path + (move, )))


def main():
    # assert_wheel_cycles()
    # display_bars(START_STATE)
    solution = solve(START_STATE)
    print('Wheels:', solution)


def display_bars(state):
    bars, wheels = state
    print('Bars:', *(BAR_POS_SEQUENCE[b] for b in bars))


def assert_wheel_cycles():
    # Ensure 8 turns of any wheel returns it to its starting position
    state = START_STATE
    print('i', state)
    for wheel in range(NUM_WHEELS):
        for i in range(8):
            state = rotate_wheel(state, wheel)
            print(i, state)
        assert state == START_STATE


if __name__ == '__main__':
    main()
