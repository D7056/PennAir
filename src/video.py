import cv2
from scipy.ndimage import median_filter
import numpy as np
from skimage.filters import apply_hysteresis_threshold

cap=cv2.VideoCapture("imgs/hard_vid.mp4")



window_size=9

kernel_size=(window_size,window_size, 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    blurred_img=cv2.medianBlur(frame,window_size)


    absolute=cv2.absdiff(frame,blurred_img)


    #mad=median_filter(absolute,kernel_size)
    mad = cv2.medianBlur(absolute, window_size)



    mad_display = cv2.cvtColor(mad, cv2.COLOR_BGR2GRAY)

    mad_display= cv2.normalize(mad_display, None, 0, 255, cv2.NORM_MINMAX)

    lower_black=0
    upper_black=15

    mask= cv2.inRange(mad_display, lower_black, upper_black)

    contours,_=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
        

    for cnt in contours:
        area=cv2.contourArea(cnt)
        m=cv2.moments(cnt)
        if area>1000:


            x=int(m["m10"]/area)
            y=int(m["m01"]/area)


            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            


            cv2.drawContours(frame,[approx], -1, (0,200,0),3)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(frame, text=f"[{x} {y}]", org=(x,y+20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,255,255))

    

    cv2.imshow("Masked", mask)
    cv2.imshow("image", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

