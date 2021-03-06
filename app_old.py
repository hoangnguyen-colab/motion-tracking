import cv2
import numpy as np

min_contour_width = 40  # 40
min_contour_height = 40  # 40
offset = 10  # 10
line_height = 530  # 530
matches = []
cars = 0
motors = 0
car_desire_length = 100
scale_percent = 60 # percent of original size

def get_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx, cy

cap = cv2.VideoCapture('traffic.mp4')

# cap.set(3, 1080)
# cap.set(4, 720)

if cap.isOpened():
    ret, frame1 = cap.read()
else:
    ret = False
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while ret:
    d = cv2.absdiff(frame1, frame2)
    grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(th, np.ones((3, 3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contours, h = cv2.findContours(
        closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for(i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)

        if not contour_valid:
            continue
        cv2.rectangle(frame1, (x-10, y-10), (x+w+10, y+h+10), (255, 0, 0), 2)
        cv2.line(frame1, (0, line_height), (1200, line_height), (0, 255, 0), 2)

        center = get_center(x, y, w, h)
        matches.append(center)
        cv2.circle(frame1, center, 5, (0, 255, 0), -1)
        cx, cy = get_center(x, y, w, h)

        for (x, y) in matches:
            if y < (line_height+offset) and y > (line_height-offset):
                if w > car_desire_length:
                    cars = cars+1
                else:
                    motors = motors+1

                matches.remove((x, y))

    cv2.putText(frame1, "Cars: " + str(cars), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 170, 0), 2)
    cv2.putText(frame1, "Motors: " + str(motors), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 170, 0), 2)

    width = int(frame1.shape[1] * scale_percent / 100)
    height = int(frame1.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame1, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("Original", resized)
    
    if cv2.waitKey(1) == 27:
        break
    frame1 = frame2
    ret, frame2 = cap.read()
# print(matches)

cv2.destroyAllWindows()
cap.release()
