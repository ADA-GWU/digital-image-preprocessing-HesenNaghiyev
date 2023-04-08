import os
import cv2
import numpy as np

# Load image
img = cv2.imread('noisy/chemical/inchi4.png', 0)

# Apply morphology
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Apply spatial filters
gaussian = cv2.GaussianBlur(img, (5, 5), 0)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# Apply frequency filter
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20 * np.log(np.abs(fshift))
rows, cols = img.shape
crow, ccol = rows // 2, cols // 2
fshift[crow - 30:crow + 30, ccol - 30:ccol + 30] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

# Add Gaussian noise
noise = np.random.normal(0, 10, img.shape)
noisy_img = img + noise

# Create directory if it does not exist
if not os.path.exists('task1'):
    os.makedirs('task1')

# Write processed images to files
cv2.imwrite('task1/original.png', img)
cv2.imwrite('task1/erosion.png', erosion)
cv2.imwrite('task1/opening.png', opening)
cv2.imwrite('task1/gaussian.png', gaussian)
cv2.imwrite('task1/noisy.png', noisy_img)
cv2.imwrite('task1/filtered.png', img_back)
