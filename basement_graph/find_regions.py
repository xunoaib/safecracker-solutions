import json

import cv2
import numpy as np

ss = cv2.imread('ss.png', cv2.IMREAD_COLOR)
template_rgba = cv2.imread('template.png', cv2.IMREAD_UNCHANGED)

template_rgb = template_rgba[:, :, :3]
alpha_mask = template_rgba[:, :, 3]

template_mask = cv2.merge([alpha_mask] * 3)

result = cv2.matchTemplate(
    ss, template_rgb, cv2.TM_CCORR_NORMED, mask=template_mask
)

threshold = 0.93
w, h = template_rgb.shape[1], template_rgb.shape[0]

locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))

matched = []
occupied = np.zeros(ss.shape[:2], dtype=np.uint8)

for pt in sorted(locations, key=lambda x: -result[x[1], x[0]]):
    x, y = pt
    roi = occupied[y:y + h, x:x + w]
    if np.count_nonzero(roi) == 0:
        matched.append((x, y))
        occupied[y:y + h, x:x + w] = 1

for x, y in matched:
    cv2.rectangle(ss, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"{len(matched)} matches")

assert len(matched) == 113

cv2.imwrite('output_with_matches.png', ss)

# sort coordinates
matched_sorted = sorted(matched, key=lambda pt: (pt[1], pt[0]))

template_width, template_height = template_rgb.shape[1], template_rgb.shape[0]
half_w, half_h = template_width // 2, template_height // 2

matched_sorted = sorted(matched, key=lambda pt: (pt[1], pt[0]))

# assign incremental IDs
nodes = [
    {
        "id": int(i),
        "x": int(x + half_w),
        "y": int(y + half_h)
    } for i, (x, y) in enumerate(matched_sorted)
]

# save for later use
with open("nodes.json", "w") as f:
    json.dump(nodes, f, indent=2)
