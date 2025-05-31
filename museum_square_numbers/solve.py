START = ((1, 2, 3), (4, 5, 6), (7, 8, 9))


def solved(state):
    return all(
        [
            *(sum(row) == 15 for row in state),
            *(sum(col) == 15 for col in rotate(state)),
            state[0][0] + state[1][1] + state[2][2] == 15,
            state[2][0] + state[1][1] + state[0][2] == 15,
        ]
    )


def rotate(state, times=1):
    for _ in range(times):
        state = tuple(zip(*state[::-1]))
    return state


def neighbors(state):
    for r in range(3):
        # rotate columns left
        left = list(state)
        left[r] = left[r][1:] + left[r][:1]
        yield tuple(left), (r, 'left')

        # rotate columns right
        right = list(state)
        right[r] = right[r][-1:] + right[r][:-1]
        yield tuple(right), (r, 'right')

    for c in range(3):
        # rotate rows left
        down = list(rotate(state))
        down[c] = down[c][1:] + down[c][:1]
        yield rotate(tuple(down), 3), (c, 'down')

        # rotate rows right
        up = list(rotate(state))
        up[c] = up[c][-1:] + up[c][:-1]
        yield rotate(tuple(up), 3), (c, 'up')


def solve(start):
    visited = {start}
    q = [(start, tuple())]
    while q:
        state, path = q.pop(0)
        if solved(state):
            return path

        for n, move in neighbors(state):
            if n not in visited:
                visited.add(n)
                q.append((n, path + (move, )))


if __name__ == '__main__':
    for idx, dir in solve(START):
        print('Row' if dir in ('left', 'right') else 'Col', idx, dir)
