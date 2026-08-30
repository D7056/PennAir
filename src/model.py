import cv2
from scipy.ndimage import median_filter
import numpy as np

img=cv2.imread("imgs/static.png")

window_size=9

blurred_img=cv2.medianBlur(img,window_size)

kernel_size=(window_size,window_size, 1)



median_img=median_filter(blurred_img, kernel_size)

absolute=np.abs(median_img-blurred_img)

mad=median_filter(absolute,kernel_size)



cv2.imshow("Original Image", img)
cv2.imshow("Blurred", blurred_img)
cv2.imshow("MAD", mad)
cv2.waitKey(0)
cv2.destroyAllWindows()
