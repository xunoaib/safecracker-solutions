ENC = 'ZPEMVBYVULADV'

amount = ord('E') - ord('L')
solution = ''.join(
    chr(ord('A') + (ord(m) - ord('A') + amount) % 26) for m in ENC
)

print(solution)
