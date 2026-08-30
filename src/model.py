import cv2
from scipy.ndimage import median_filter
import numpy as np
from skimage.filters import apply_hysteresis_threshold

img=cv2.imread("imgs/static.png")



window_size=9

blurred_img=cv2.medianBlur(img,window_size)

kernel_size=(window_size,window_size, 1)





absolute=cv2.absdiff(img,blurred_img)


mad=median_filter(absolute,kernel_size)

print(mad)
print(np.max(mad))
print(np.mean(mad))

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
        cv2.drawContours(img,[cnt], -1, (0,200,0),3)
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(img, text=f"[{x} {y}]", org=(x,y+20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,255,255))



cv2.imshow("Masked", mask)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



"""edges= absolute/(mad+0.3)

edges=edges.astype(np.float32)




edges_display = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

connected=apply_hysteresis_threshold(edges_display, 2, 6)

print("min:", edges_display.min())
print("max:", edges_display.max())
print("mean:", edges_display.mean())
print("median:", np.median(edges_display))
print("90th percentile:", np.percentile(edges_display, 90))
print("99th percentile:", np.percentile(edges_display, 99))
print("99.9th percentile:", np.percentile(edges_display, 99.9))

edges_display= cv2.normalize(edges_display, None, 0, 255, cv2.NORM_MINMAX)



connected_display = (connected.astype(np.uint8) * 255)

kernel = np.ones((3, 3), np.uint8)
closed = cv2.dilate(connected_display, kernel, iterations=1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel, iterations=2)





contour, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(contour)
min_area = 100

filtered_contours = [c for c in contour if cv2.contourArea(c) >= min_area]



print(len(filtered_contours))

for i in filtered_contours:
    print(cv2.contourArea(i))

smoothed_contours = []
for c in filtered_contours:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    smoothed_contours.append(approx)



cv2.imshow("Original Image", img)
cv2.imshow("Blurred", blurred_img)
cv2.imshow("MAD", mad_display)
cv2.imshow("Absolute", absolute)
cv2.imshow("edges", edges_display)
cv2.imshow("connected", connected_display)
cv2.imshow("closed", closed)
cv2.drawContours(img, smoothed_contours, -1, (0,0,0), 2)
cv2.imshow("Drawn Contour", img)

cv2.imshow("Masked", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
