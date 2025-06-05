import time

import cv2
import numpy as np


class State:

    def __init__(self):
        self.history = []
        self.mode = ''
        self.last_frame_num = 0

    def update(self, state: str, frame_num):

        # ignore duplicate frames
        if self.history and self.history[-1] == state:

            # force an update after a period of inactivity (fixes flash detection).
            # during testing, 2nd flash generally occurs after 15-18 frames.
            if self.mode == 'resp 0':
                nframes = frame_num - self.last_frame_num
                print('Time since 1st resp:', nframes)
                # exit early if the delay is still low
                if nframes < 30:
                    return
            else:
                return

        self.last_frame_num = frame_num
        self.history.append(state)

        enter_seq = ['', '0', '00', '000', '0000']

        for i in range(1, len(enter_seq)):
            if self.history[-1 - i:] == enter_seq[:i + 1]:
                print('Entered', i)
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

        return

        # identify when numbers are being entered
        change = (self.last_state, self.mode)
        if change == ('', '0') and self.entering == 0:
            self.entering = 1
            print('Entering', self.entering, change)
        elif change == ('0', '00') and self.entering == 1:
            self.entering = 2
            print('Entering', self.entering, change)
        elif change == ('00', '000') and self.entering == 2:
            self.entering = 3
            print('Entering', self.entering, change)
        elif change == ('000', '0000') and self.entering == 3:
            self.entering = 4  # last key entered
            print('Entering', self.entering, change)
        elif self.last_state == '0000' and self.entering == 4:
            self.entering = 5  # start reading response
            print('Response:', self.mode)
        elif self.entering == 5:
            print(change)
        # else:
        #     self.entering = 0


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

    matches = [(m, 'correct') for m in correct_matches]
    matches += [(m, 'incorrect') for m in incorrect_matches]
    return sorted(matches)


def classify_frame(matches):
    '''Classifies the current frame based on matched templates'''

    result = ''
    for region, status in matches:
        result += '1' if status == 'correct' else '0'
    return result


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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (ref_frame.shape[1], ref_frame.shape[0]))

        diff = cv2.absdiff(frame, ref_frame)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        cropped = diff_gray[307:307 + 158, 1393:1393 + 544]

        matches = find_response_matches(cropped)

        frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        result = classify_frame(matches)
        state.update(result, frame_num)

        for (x, y, w, h), status in matches:
            if status == 'correct':
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
