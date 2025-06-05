import time

import cv2
import numpy as np

INCORRECT = '0'
CORRECT = '1'


class State:
    '''A state machine to extract meaning from flashing lights'''

    def __init__(self):
        self.history = []
        self.mode = ''
        self.last_frame_num = 0

    def update(self, state: str, frame_num):
        # ignore duplicate frames (except when waiting on 2nd flash)
        if self.history and self.history[-1] == state:

            # force an update after a period of inactivity (fixes flash detection).
            # during testing, 2nd flash generally occurs after 15-18 frames.
            if self.mode == 'resp 0':
                nframes = frame_num - self.last_frame_num
                # print('Time since 1st resp:', nframes)
                # exit early if the delay is still low
                if nframes < 30:
                    return
            else:
                return

        self.last_frame_num = frame_num
        self.history.append(state)

        enter_seq = ['xxxx', '0xxx', '00xx', '000x', '0000']

        for i in range(1, len(enter_seq)):
            if self.history[-1 - i:] == enter_seq[:i + 1]:
                print('Entered key', i)
                self.mode = f'entering {i}'
                break
        else:
            if self.mode.startswith('entering 4'):
                print('1st response:', state)
                self.mode = 'resp 0'
            elif self.mode == 'resp 0':
                # if the first response is solid (no flashing),
                # the 2nd response will not be interpreted correctly.
                # consider using a time check?
                print('2nd response:', state)
                self.mode = 'resp 1'
            elif self.mode == 'resp 1' and self.history[-1] == '':
                print('Resetting')


def boxes_iou(boxA, boxB):
    """Compute Intersection over Union (IoU) of two boxes."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH

    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]
    unionArea = areaA + areaB - interArea

    if unionArea == 0:
        return 0
    return interArea / unionArea


def non_overlapping_template_match(
    image, template_path, threshold=0.8, iou_threshold=0.1
):
    """Return a non-overlapping list of match bounding boxes."""
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    assert template is not None, f'Failed to load {template_path}'

    h, w = template.shape[:2]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    matches = []

    # Get all potential matches above threshold
    locations = np.where(result >= threshold)
    candidates = list(zip(locations[1], locations[0]))  # (x, y)

    # Sort candidates by match score (descending)
    scores = result[locations]
    sorted_candidates = sorted(zip(candidates, scores), key=lambda x: -x[1])

    for (x, y), score in sorted_candidates:
        box = (x, y, w, h)
        if all(
            boxes_iou(box, existing) < iou_threshold for existing in matches
        ):
            matches.append(box)

    return matches


def find_response_matches(image):
    correct_matches = non_overlapping_template_match(
        image, 'template_correct.png'
    )
    incorrect_matches = non_overlapping_template_match(
        image, 'template_incorrect.png'
    )

    matches = [(m, CORRECT) for m in correct_matches]
    matches += [(m, INCORRECT) for m in incorrect_matches]
    return sorted(matches)


def decode_matches(matches, light_regions: list):
    '''Classifies the currently displayed lights based on matched templates'''

    if light_regions:
        result = list('xxxx')
        for (x, y, w, h), status in matches:
            idx = next(
                i for i, (rx, ry, rw, rh) in enumerate(light_regions)
                if rx <= x + w / 2 < rx + rw
            )
            result[idx] = status
        return ''.join(result)

    return ''.join(status for _, status in matches).ljust(4, 'x')


def main():
    VIDEO_PATH = 'video.mkv'
    REF_FRAME_INDEX = 30

    cap = cv2.VideoCapture(VIDEO_PATH)
    assert cap.isOpened(), 'Failed to open video'

    cap.set(cv2.CAP_PROP_POS_FRAMES, REF_FRAME_INDEX)
    ret, ref_frame = cap.read()
    assert ret, 'Failed to read reference frame'
    ref_frame = ref_frame.copy()

    cap.set(cv2.CAP_PROP_POS_FRAMES, 100)

    state = State()
    light_regions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (ref_frame.shape[1], ref_frame.shape[0]))

        diff = cv2.absdiff(frame, ref_frame)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        cropped = diff_gray[307:307 + 158, 1393:1393 + 544]

        matches = find_response_matches(cropped)

        # remember the locations of lights (so we can detect when they're off)
        if len(matches) == 4:
            light_regions = [region for region, status in matches]

        # decode the currently displayed lights
        result = decode_matches(matches, light_regions)

        # update state machine
        frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        state.update(result, frame_num)

        for (x, y, w, h), status in matches:
            if status == CORRECT:
                cv2.rectangle(
                    frame, (x + 1393, y + 307), (x + 1393 + w, y + 307 + h),
                    (0, 255, 0), 2
                )
            else:
                cv2.rectangle(
                    frame, (x + 1393, y + 307), (x + 1393 + w, y + 307 + h),
                    (0, 0, 255), 2
                )

        # cv2.imshow('Frame Difference (Grayscale)', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
            print(f'Current frame index: {frame_idx}')
        elif key == ord('s'):
            filename = f'diff_frame_{int(time.time())}.png'
            cv2.imwrite(filename, diff_gray)
            print(f'Saved: {filename}')
        elif key == ord('r'):
            # Pause to let me select a region on the current frame
            roi = cv2.selectROI(
                'Select Region', frame, fromCenter=False, showCrosshair=True
            )
            cv2.destroyWindow('Select Region')

            x, y, w, h = roi
            print(f"Selected region: x={x}, y={y}, w={w}, h={h}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
