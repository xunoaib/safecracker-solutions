from z3 import And, Distinct, Int, Solver, sat

N = 6

cols = [Int(f'q{i}') for i in range(N)]

s = Solver()
s.add([And(0 <= c, c < N) for c in cols])
s.add(Distinct(*cols))

for i in range(N):
    for j in range(N):
        if i != j:
            s.add(cols[i] - cols[j] != i - j)
            s.add(cols[i] - cols[j] != j - i)

assert s.check() == sat
m = s.model()
for r, col in enumerate(cols):
    print((r, m[col].as_long()))
