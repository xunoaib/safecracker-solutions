# ring values are specified clockwise starting from their rightmost arrow
'''
after rotating red cw:
    blue[1] = red[4]
    green[2] = red[3]
    blue[3] = red[2]
    green[4] = red[1]

after rotating green cw:
    red[1] = green[4]
    blue[2] = green[3]
    red[3] = green[2]
    blue[4] = green[1]

after rotating blue cw:
    green[1] = blue[4]
    red[2] = blue[3]
    green[3] = blue[2]
    red[4] = blue[1]
'''

RED, GREEN, BLUE = range(3)

RED_RING = 'g.b..r'
GREEN_RING = '...g.b'
BLUE_RING = '..gb.r'

START_STATE = tuple(map(tuple, [RED_RING, GREEN_RING, BLUE_RING]))


def rotate_cw(state, ring_idx: int):
    result = list(map(list, state))
    result[ring_idx] = result[ring_idx][-1:] + result[ring_idx][:-1]

    others = {
        RED: (BLUE, GREEN),
        GREEN: (RED, BLUE),
        BLUE: (GREEN, RED),
    }[ring_idx]

    for i in range(4):
        result[others[i % 2]][i + 1] = result[ring_idx][4 - i]

    return tuple(map(tuple, result))


def rotate_ccw(state, ring_idx: int):
    for _ in range(len(RED_RING) - 1):
        state = rotate_cw(state, ring_idx)
    return state


def main():
    state = START_STATE
    print(state)
    print(rotate_ccw(rotate_cw(state, 0), 0))


if __name__ == '__main__':
    main()
