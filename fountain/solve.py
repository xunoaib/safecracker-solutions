# Each jet can be in one of four states
LEFT, MID_RIGHT, RIGHT, MID_LEFT = range(4)

# A middle jet can be in one of two states (in the process of moving left or
# right), though this detail technically doesn't actually matter.
JET_STATES = [0, 1, 2, 1]

# Initial states starting from the main entrance tile (0) moving clockwise
INIT_STATE = ((LEFT, LEFT, MID_RIGHT, LEFT), 0)


def move(state, direction: int):
    '''Move in a given direction (1 = left, -1 = right)'''
    assert direction in (-1, 1)
    jets, pos = state
    pos = (pos + direction) % 4
    return (jets[:pos] + ((jets[pos] + 1) % 4, ) + jets[pos + 1:], pos)


def solved(state):
    return tuple(JET_STATES[s] for s in state[0]) == (2, 1, 0, 2)


def solve(state):
    q = [(state, tuple())]
    visited = {state}
    while q:
        state, path = q.pop(0)
        if solved(state):
            return path
        for dir in (-1, 1):
            nstate = move(state, dir)
            if nstate not in visited:
                visited.add(nstate)
                q.append((nstate, path + (dir, )))


def solve_all(state):
    solutions = []
    q = [(state, tuple())]
    visited = {state}
    while q:
        state, path = q.pop(0)
        if solutions and len(path) > len(solutions[0][0]):
            continue
        if solved(state):
            solutions.append((path, state))
        for dir in (-1, 1):
            nstate = move(state, dir)
            if nstate not in visited:
                visited.add(nstate)
                q.append((nstate, path + (dir, )))
    return solutions


solutions = solve_all(INIT_STATE)
print(f'Found {len(solutions)} solutions:')
for solution, state in solutions:
    solution_str = ''.join('L' if v == 1 else 'R' for v in solution)
    print(state, solution_str)
