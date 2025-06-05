import cv2

VIDEO_PATH = 'video.mkv'
REF_FRAME_INDEX = 648

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

    cv2.imshow('Frame Difference (Grayscale)', diff_gray)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        print(f'Current frame index: {frame_idx}')

cap.release()
cv2.destroyAllWindows()
