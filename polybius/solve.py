CODE = '34331544523443245321245115'

SQUARE = (
    tuple('abcde'),
    tuple(('f', 'g', 'h', 'i', 'k')),  # i or j
    tuple('lmnop'),
    tuple('qrstu'),
    tuple('vwxyz'),
)

for i in range(0, len(CODE), 2):
    r, c = map(int, CODE[i:i + 2])
    print(SQUARE[r - 1][c - 1], end='')
print()
