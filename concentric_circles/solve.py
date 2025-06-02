# ring values are specified clockwise starting from their rightmost arrow

GREEN_RING = '...g.b'
BLUE_RING = '..gb.r'
RED_RING = 'g.b..r'

START_STATE = tuple(map(tuple, [RED_RING, GREEN_RING, BLUE_RING]))


def rotate(state, ring_idx: int):
    result = list(state)
    result[ring_idx] = result[ring_idx][1:] + result[ring_idx][:1]
    return tuple(result)


def main():
    state = START_STATE
    print(state)
    print(rotate(state, 0))


if __name__ == '__main__':
    main()
