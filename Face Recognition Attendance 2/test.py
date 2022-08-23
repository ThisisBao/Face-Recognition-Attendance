import cv2

cam = cv2.VideoCapture(0)
while True:
    ret, img = cam.read()
    cv2.imshow("hi",img)
    cv2.waitKey(1)