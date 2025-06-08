from itertools import product

CAPACITIES = (3, 5, 8)


def solved(state):
    return state[1] == 4


def neighbors(state):
    for (src, src_vol), (tar, tar_vol) in product(enumerate(state), repeat=2):
        if src != tar and src_vol > 0:
            new = list(state)
            tar_left = CAPACITIES[tar] - tar_vol
            xfer = min(tar_left, src_vol)
            new[tar] += xfer
            new[src] -= xfer
            yield tuple(new), (src, tar)


def reconstruct_path(parent, state):
    path = []
    while entry := parent[state]:
        state, move = entry
        path.append(move)
    return tuple(path[::-1])


def solve(start):
    parent = {start: None}
    q = [start]
    while q:
        state = q.pop(0)
        if solved(state):
            return reconstruct_path(parent, state)

        for n, move in neighbors(state):
            if n not in parent:
                parent[n] = state, move
                q.append(n)


start = (0, 0, 8)

solution = solve(start)
for src, tar in solution:
    print(f'{src} to {tar}')
