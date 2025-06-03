import cv2

# --- Step 1: Load the image ---
image = cv2.imread('ss.jpg', cv2.IMREAD_GRAYSCALE)  # Load in grayscale
if image is None:
    raise ValueError("Image not found or path is incorrect")

# --- Step 2: Crop the region of interest ---
# Example region (top-left x,y and width, height)
x, y, w, h = 100, 50, 200, 150
# cropped = image[y:y + h, x:x + w]
cropped = image

# --- Step 3: Apply thresholding ---
# Threshold value (e.g., 127); you can adjust this
thresholded = cv2.adaptiveThreshold(
    cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# --- Optionally: Save or display results ---
cv2.imwrite('cropped_thresholded.jpg', thresholded)
cv2.imshow('Thresholded Image', thresholded)
cv2.waitKey(0)
cv2.destroyAllWindows()
