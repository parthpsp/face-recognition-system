import cv2
import imutils
import os
import namegenerator
import numpy as np
import pytesseract
from PIL import Image
from win10toast import ToastNotifier


def platerecognition():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    messg = ToastNotifier()

    number_plate = "KL 07 CR 9064"
    vid = cv2.VideoCapture(0)

    while True:

        check, img = vid.read()

    #img = cv2.imread('testcar.jpg', cv2.IMREAD_COLOR)

        img = cv2.resize(img, (620, 480))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None
        #counter = 0
        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            #counter = counter + 1
        #    print("c = ", approx)
            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx


            if screenCnt is None:
                detected = 0
            else:


                # Masking the part other than the number plate
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
                new_image = cv2.bitwise_and(img, img, mask=mask)

                # Now crop
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

                # Read the number plate
                text = pytesseract.image_to_string(Cropped, config='--psm 11')
                if len(text) >= 5:
                    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
                    if text == number_plate:
                        if not os.path.exists('captured vehicle images/' + number_plate):
                            os.makedirs('captured vehicle images/' + number_plate)
                        save_img_name = 'captured vehicle images/' + number_plate + '/' + namegenerator.gen() + '.jpg'
                        cv2.imwrite(filename=save_img_name, img=img)
                        messg.show_toast("Number Plate founded", number_plate)

                #   #print("Detected Number is:", text)
                    #print("counter = ", counter)

                # cv2.imshow('image', img)
                # cv2.imshow('Cropped', Cropped)
                screenCnt = None

        cv2.imshow('image', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
