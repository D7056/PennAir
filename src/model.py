import cv2
from scipy.ndimage import median_filter
import numpy as np
from skimage.filters import apply_hysteresis_threshold
import math



img=cv2.imread("imgs/noisy.png")

def tracker(img):
    

     
    height, width, channel= img.shape
    centerx=width//2
    centery=height//2

    window_size=9



    # Replacing each pixel by the median of its region
    blurred_img=cv2.medianBlur(img,window_size)



    kernel_size=(window_size,window_size, 1)




    #Taking the difference between the median and original image
    absolute=cv2.absdiff(img,blurred_img)

    #Taking the median of that image to find the anomality of the pixels in a particular section of the image
    mad=cv2.medianBlur(absolute,window_size)

    
    mad_display = cv2.cvtColor(mad, cv2.COLOR_BGR2GRAY)

    mad_display= cv2.normalize(mad_display, None, 0, 255, cv2.NORM_MINMAX)

    lower_black=0
    upper_black=15

    #Isolating the dark regions of the image
    mask= cv2.inRange(mad_display, lower_black, upper_black)

    

    



    


    #Drawing a contour around those regions
    contours,_=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    
    



    ratio=0
    area_circle=0

    later=[]
    for cnt in contours:
        area=cv2.contourArea(cnt)
        perimeter=cv2.arcLength(cnt, closed=True)

        
            


        m=cv2.moments(cnt)

        #Filtering by size

        if area>1000:
            #Checking the circularity to find the area of the circle
            if ratio < 4*math.pi*area/perimeter**2:
                    ratio=4*math.pi*area/perimeter**2
                    area_circle=area
            x=int(m["m10"]/area)
            y=int(m["m01"]/area)
            print(area)
            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.drawContours(img,[approx], -1, (0,200,0),3)
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            later.append((x,y))

    radius=math.sqrt(area_circle/math.pi)


        


    fx=2564.3186869

    fy=2569.70273111
    real=10

    fav=(fx+fy)/2

    #caclulating the depth relative to the circles' radius

    z=fav*real/radius


    

    for i in later:
        
        x,y=i

        X=(x-centerx)*z/fx
        Y=(y-centery)*z/fy
        cv2.putText(img, text=f"[{X:.2f}, {Y:.2f}, {z:.2f}]", org=(x,y+20), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,255,255))

    cv2.circle(img, (centerx,centery), 5, (255,255,255), -1)
   

    cv2.imshow("image", img)
    



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
