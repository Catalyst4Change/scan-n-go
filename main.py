import cv2
import numpy as np
from pyzbar.pyzbar import decode
import winsound

savedData = []


def beep():
    winsound.Beep(150, 1000)


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        string = "Data: " + str(barcodeData)

        checkDatabase(barcodeData)

        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        print(string)


def checkDatabase(barcode):
    if barcode not in savedData:
        savedData.append(barcode)
        beep()
    print("LIST: ", savedData)


# this function should only run after SCAN button pressed,
# stop after scan complete,
# display read info,
# ask for confirmation before submitting
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
