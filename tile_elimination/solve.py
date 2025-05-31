input_grid = '''
..xx.x.
.s..xx.
.xx....
.x..xx.
.x.x...
.x.x.x.
xxx.xxx
x.xx.x.
'''.strip()

grid = {
    (r, c)
    for r, line in enumerate(input_grid.splitlines())
    for c, ch in enumerate(line) if ch == 'x'
}

start = next(
    (r, c) for r, line in enumerate(input_grid.splitlines())
    for c, ch in enumerate(line) if ch == 's'
)

print(grid)
print(start)
