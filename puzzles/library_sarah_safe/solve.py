NUM_LETTERS = {
    2: 'DRBP',
    3: 'UFQ',
    4: 'NGV',
    5: 'CWHX',
    6: 'AIY',
    7: 'LMJZ',
    8: 'TSK',
    9: 'EO',
}

LETTER_NUM = {
    letter: num
    for num, letters in NUM_LETTERS.items()
    for letter in letters
}

print(*(LETTER_NUM[l] for l in 'SARAH'), sep='')
