import os
import time

import cv2
import mss
import numpy as np
from solve import create_guesser

INCORRECT = '0'
CORRECT = '1'

MONITOR_ID = 1

# FRAME_TIMEOUT = 30  # recorded video file
FRAME_TIMEOUT = 400  # live screen capture

# % of pixels which must match reference
PERCENT_MATCH = 0.90

# brightness diff from 0-255 (0 = exact match, 255 = include all)
MATCH_THRESHOLD = 40


class State:
    '''A state machine to extract meaning from flashing lights'''

    FLASH1 = '1st flash'
    FLASH2 = '2nd flash'
    RESETTING = 'Resetting'

    def __init__(self):
        self.history = []
        self.mode = ''
        self.last_frame_num = 0
        self.flash_states = []
        self._last_response = None

    @property
    def response(self) -> str | None:
        if len(self.flash_states) != 2 or self.mode not in (
            self.FLASH2,
            self.RESETTING,
        ):
            return None

        response = ''
        for a, b in zip(*self.flash_states):
            if a == b == '1':
                response += 'c'  # correct
            elif a == b == '0':
                response += 'w'  # wrong
            elif {a, b} == {'1', 'x'}:
                response += 'p'  # partial
        return response

    def update(
        self,
        state: str,
        frame_num,
        timeout=FRAME_TIMEOUT,
    ) -> str | None:
        '''Updates the state machine with new information. When a new response
        is detected, it will be be returned once (but never again).'''

        # ignore duplicate frames (except when waiting on 2nd flash)
        if self.history and self.history[-1] == state:
            # force an update after a period of inactivity waiting for the 2nd
            # flash, which may not come. during testing, 2nd flash generally
            # occurs after 15-18 frames (from captured video) or 308 frames
            # during live capture (on my machine).
            nframes = frame_num - self.last_frame_num
            if self.mode != self.FLASH1 or nframes < timeout:
                return None

        self.last_frame_num = frame_num
        self.history.append(state)
        self.history = self.history[-500:]

        enter_seq = ['xxxx', '0xxx', '00xx', '000x', '0000']

        for i in range(1, len(enter_seq)):
            if self.history[-1 - i:] == enter_seq[:i + 1]:
                print('Entered key', i)
                self.mode = f'Entered {i}'
                break
        else:
            if self.mode.startswith('Entered 4'):
                print('1st response:', state)
                self.mode = self.FLASH1
                self.flash_states = [state]
            elif self.mode == self.FLASH1:
                print('2nd response:', state)
                self.mode = self.FLASH2
                self.flash_states.append(state)
            elif self.mode == self.FLASH2 and self.history[-1] == '':
                print('Resetting')
                self.mode = self.RESETTING
                self.flash_states = []

        new_response = self.response
        if new_response and new_response != self._last_response:
            self._last_response = new_response
            print('New response:', new_response)
            return new_response
        else:
            return None


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


def grab_screen_region(region):
    '''
    Capture a specific region (x, y, width, height) of the primary monitor.
    region: (x, y, width, height) relative to the primary monitor.
    '''
    with mss.mss() as sct:
        # index 1 is always the primary monitor
        monitor = sct.monitors[MONITOR_ID]
        region_abs = {
            "top": monitor["top"] + region['top'],
            "left": monitor["left"] + region['left'],
            "width": region['width'],
            "height": region['height']
        }
        screenshot = sct.grab(region_abs)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def select_screen_region():
    '''Use mss to capture the full screen, then let user select a region'''
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]  # full primary screen
        screenshot = sct.grab(monitor)
        full_image = np.array(screenshot)
        full_image_bgr = cv2.cvtColor(full_image, cv2.COLOR_BGRA2BGR)

    roi = cv2.selectROI(
        "Select Region", full_image_bgr, fromCenter=False, showCrosshair=True
    )
    cv2.destroyWindow("Select Region")

    x, y, w, h = roi
    return {'left': x, 'top': y, 'width': w, 'height': h}


def main():

    print(
        'Press "f" when all lights are off to save a reference frame (ss.jpg)'
    )
    print('Press "r" to select the region containing lights')

    # relative coords (to primary monitor)
    region = {'left': 1296, 'top': 216, 'width': 636, 'height': 252}

    state = State()
    light_regions = []

    if os.path.exists('ss.jpg'):
        subtractive_frame = cv2.imread('ss.jpg')
    else:
        print('Subtractive frame not found')
        subtractive_frame = np.zeros([0, 0])

    # create solver objects to generate guesses and deductions
    guesser = create_guesser()

    # suggest a first guess
    guess = guesser.best_guess()
    print('Guess:', guess)

    while True:
        frame = grab_screen_region(region)
        x, y, w, h = [region[v] for v in ['left', 'top', 'width', 'height']]
        cropped_subtractive_frame = subtractive_frame[y:y + h, x:x + w]
        diff = cv2.absdiff(frame, cropped_subtractive_frame)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        matches = find_response_matches(diff_gray)

        # when 4 lights are visible, save their regions
        if len(matches) == 4:
            light_regions = [region for region, _ in matches]

        # decode lights from regions (if available)
        result = decode_matches(matches, light_regions)

        # update state machine, and retrieve any emitted response
        if response := state.update(result, int(time.time() * 1000)):
            guess = guesser.best_guess()
            guesser.add(guess, response)
            print('Guess:', guesser.best_guess())

        for (x, y, w, h), status in matches:
            color = (0, 255, 0) if status == CORRECT else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        total_pixels = (diff_gray.shape[0] * diff_gray.shape[1])
        percent_black = np.sum(diff_gray < MATCH_THRESHOLD) / total_pixels

        # draw status text
        # color = (0, 255, 0) if percent_black > PERCENT_MATCH else (0, 0, 255)
        color = (0, 0, 255)
        text1 = f'% match: {percent_black:.4f}'
        text2 = f'code: {state.history[-1]}'
        text3 = f'mode: {state.mode}'
        text4 = f'resp: {state.response or ""}'
        for y, text in zip([30, 55, 80, 105], [text1, text2, text3, text4]):
            cv2.putText(
                frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
            )

        cv2.imshow('Live Screen Difference', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f'diff_frame_{int(time.time())}.png'
            cv2.imwrite(filename, diff_gray)
            print(f'Saved: {filename}')
        elif key == ord('r'):
            region = select_screen_region()
            print(f"Selected new region: {region}")
        elif key == ord('f'):
            print('Saving fullscreen subtractive frame')
            with mss.mss() as sct:
                screenshot = sct.grab(sct.monitors[MONITOR_ID])
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                cv2.imwrite('ss.jpg', img)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
