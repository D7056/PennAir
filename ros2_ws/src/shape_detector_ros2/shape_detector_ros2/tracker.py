import cv2
import math

def tracker(img):
    height, width, channel = img.shape
    centerx = width // 2
    centery = height // 2
    window_size = 9

    # Replacing each pixel by the median of its region
    blurred_img = cv2.medianBlur(img, window_size)

    #Taking the difference between the median and original image
    absolute = cv2.absdiff(img, blurred_img)

     #Taking the median of that image to find the anomality of the pixels in a particular section of the image
    mad = cv2.medianBlur(absolute, window_size)

    mad_display = cv2.cvtColor(mad, cv2.COLOR_BGR2GRAY)
    mad_display = cv2.normalize(mad_display, None, 0, 255, cv2.NORM_MINMAX)

     #Isolating the dark regions of the image
    mask = cv2.inRange(mad_display, 0, 15)

    #Drawing a contour around those regions
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ratio = 0
    area_circle = 0
    shapes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)

         #Filtering by size
        if area > 1000:
            circularity = 4 * math.pi * area / perimeter**2

             #Checking the circularity to find the area of the circle
            if ratio < circularity:
                ratio = circularity
                area_circle = area

            m = cv2.moments(cnt)
            x = int(m["m10"] / area)
            y = int(m["m01"] / area)

            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            outline = [(int(p[0][0]), int(p[0][1])) for p in approx]

            shapes.append({"center_px": (x, y), "outline": outline})

    if area_circle == 0:
        return []

    radius = math.sqrt(area_circle / math.pi)
    fx = 2564.3186869
    fy = 2569.70273111

    real = 10

    fav = (fx + fy) / 2

     #caclulating the depth relative to the circles' radius

    z = fav * real / radius

    detections = []
    for s in shapes:
        x, y = s["center_px"]
        X = (x - centerx) * z / fx
        Y = (y - centery) * z / fy

        detections.append({"position": (X, Y, z), "outline": s["outline"]})

    return detections
