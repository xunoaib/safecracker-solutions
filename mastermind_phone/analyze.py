import time

import cv2
import numpy as np


def non_overlapping_template_match(image, template_path, threshold=0.8):
    '''Return a non-overlapping list of match bounding boxes'''
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    assert template is not None, f'Failed to load {template_path}'

    h, w = template.shape[:2]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    matches = []

    result_copy = result.copy()

    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_copy)
        if max_val < threshold:
            break

        x, y = max_loc
        matches.append((x, y, w, h))

        # Suppress this region by zeroing it out
        result_copy[y:y + h, x:x + w] = 0

    return matches


def classify_frame(matches):
    '''Classifies the current frame based on matched templates'''

    print(len(matches))


VIDEO_PATH = 'video.mkv'
REF_FRAME_INDEX = 30

cap = cv2.VideoCapture(VIDEO_PATH)
assert cap.isOpened(), 'Failed to open video'

cap.set(cv2.CAP_PROP_POS_FRAMES, REF_FRAME_INDEX)
ret, ref_frame = cap.read()
assert ret, 'Failed to read reference frame'
ref_frame = ref_frame.copy()

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (ref_frame.shape[1], ref_frame.shape[0]))

    diff = cv2.absdiff(frame, ref_frame)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    count = (diff_gray < 15).sum()

    cropped = diff_gray[307:307 + 158, 1393:1393 + 544]

    correct_matches = non_overlapping_template_match(
        cropped, 'template_correct.png'
    )
    incorrect_matches = non_overlapping_template_match(
        cropped, 'template_incorrect.png'
    )

    matches = [(m, 'correct') for m in correct_matches]
    matches += [(m, 'incorrect') for m in incorrect_matches]
    matches.sort()

    classify_frame(matches)

    for (x, y, w, h) in correct_matches:
        cv2.rectangle(
            frame, (x + 1393, y + 307), (x + 1393 + w, y + 307 + h),
            (0, 255, 0), 2
        )
    for (x, y, w, h) in incorrect_matches:
        cv2.rectangle(
            frame, (x + 1393, y + 307), (x + 1393 + w, y + 307 + h),
            (0, 0, 255), 2
        )

    # if count < 3600000:
    #     diff_gray[:] = 0

    cv2.imshow('Frame Difference (Grayscale)', frame)
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
