from z3 import Distinct, Int, Solver, sat

# ys[0] is at row 0, ys[1] is at row 1, etc
# ys[i] specifies the column of the y in row i
ys = [Int(f'y{i}') for i in range(4)]
ls = [Int(f'l{i}') for i in range(4)]
es = [Int(f'e{i}') for i in range(4)]
ss = [Int(f's{i}') for i in range(4)]

solver = Solver()

solver.add(ys[3] == 0)
solver.add(ls[2] == 1)
solver.add(es[1] == 2)
solver.add(ss[0] == 3)

for cols in [ys, ls, es, ss]:
    solver.add(Distinct(cols))
    for col in cols:
        solver.add(0 <= col)
        solver.add(col < 4)

for r in range(4):
    solver.add(Distinct([symbols[r] for symbols in [ys, ls, es, ss]]))

if solver.check() == sat:
    m = solver.model()

    grid = [['.'] * 4 for _ in range(4)]

    for cols in [ys, ls, es, ss]:
        for r, col in enumerate(cols):
            grid[r][m[col].as_long()] = str(cols[0])[0]

    for row in grid:
        print(''.join(row).upper())
