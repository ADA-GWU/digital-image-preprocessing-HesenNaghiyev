import cv2
import numpy as np
import os

# Define the path to the noisy images
noisy_path = 'noisy/speckle'

# Define the path to the cleaned images
clean_path = 'task2'

# Create the output directory if it doesn't exist
if not os.path.exists(clean_path):
    os.makedirs(clean_path)

# Loop over all the images in the noisy directory
for filename in os.listdir(noisy_path):
    if filename.endswith('.jpeg') or filename.endswith('.png'):
        # Load the noisy image
        img = cv2.imread(os.path.join(noisy_path, filename), 0)

        # Apply morphology
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        # Apply spatial filters
        median = cv2.medianBlur(opening, 3)
        bilateral = cv2.bilateralFilter(median, 9, 75, 75)

        # Save the cleaned image
        cv2.imwrite(os.path.join(clean_path, filename), bilateral)
