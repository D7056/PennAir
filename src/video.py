import cv2
from scipy.ndimage import median_filter
import numpy as np
from skimage.filters import apply_hysteresis_threshold
from src.model import tracker

cap=cv2.VideoCapture("imgs/hard_vid.mp4")





while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    tracker(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

