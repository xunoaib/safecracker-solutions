EMPTY, TALL, SHORT, LONG, SQUARE = range(5)

START = (SQUARE, SHORT, TALL, LONG, EMPTY)
GOAL = (TALL, LONG, EMPTY, SHORT, SQUARE)


def swap(state, src, tar):
    assert state[tar] == EMPTY
    items = list(state)
    items[src], items[tar] = items[tar], items[src]
    return tuple(items)


def solve(start):
    q = [(start, tuple())]
    visited = {start}
    while q:
        state, path = q.pop(0)
        if state == GOAL:
            return path
        tar = state.index(EMPTY)
        for src in state:
            if src != tar:
                nstate = swap(state, src, tar)
                if nstate not in visited:
                    visited.add(nstate)
                    q.append((nstate, path + ((src, tar), )))


path = solve(START)
print(path)
