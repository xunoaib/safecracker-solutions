from itertools import batched, pairwise

# Starting position
START = 4
GOAL = 11

# Range of possible positions
MIN, MAX = 0, 15

# Distance moved by up/down buttons
UP, DOWN = 5, -7


def neighbors(p):
    for v in (UP, DOWN):
        n = p + v
        if MIN <= n <= MAX:
            yield n


def solve(start):
    visited = {start}
    q = [(start, (start, ))]
    while q:
        p, path = q.pop(0)
        if p == GOAL:
            return path

        for n in neighbors(p):
            if n not in visited:
                visited.add(n)
                q.append((n, path + (n, )))


def format_solution(path):
    s = ''
    for a, b in pairwise(path):
        s += 'U' if b - a == UP else 'D'
    return s


solution = solve(START)
solution_str = format_solution(solution)
print(*map(''.join, batched(solution_str, 4)))
