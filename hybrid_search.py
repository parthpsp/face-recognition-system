import face_recognition
import cv2
import os
import namegenerator
import eel
import pytesseract
import imutils
import numpy as np

from win10toast import ToastNotifier


#eel.init('web')
#@eel.expose
def hybridrecognize():
    messg = ToastNotifier()
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    number_plate = "KL 07 CR 9064"
    vid = cv2.VideoCapture(0)

    #obama_img = face_recognition.load_image_file('./pics/obama.jpg')
    #obama_face_encod = face_recognition.face_encodings(obama_img)[0]

    #trump_img = face_recognition.load_image_file('./pics/trump.jpg')
    #trump_img_encod = face_recognition.face_encodings(trump_img)[0]

    #known_face_encoding = [
    #    obama_face_encod,
    #    trump_img_encod
    #]

    #known_faces_name = [
    #    "obama",
    #    "trump"
    #]

    #file management
    list = os.listdir('pics') # dir is your directory path
    number_files = len(list)
    arr_files_name = os.listdir('pics')

    known_face_encoding = [None] * number_files
    known_faces_name = [None] * number_files
    for i in range(number_files):
        _image = face_recognition.load_image_file('./pics/'+arr_files_name[i])
        known_face_encoding[i] = face_recognition.face_encodings(_image)[0]
        t = arr_files_name[i].split('.')[0]
        known_faces_name[i] = t

    while True:

        check, frame = vid.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        #numberplate start here
        frame = cv2.resize(frame, (620, 480))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None
        # counter = 0
        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            # counter = counter + 1
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
                new_image = cv2.bitwise_and(frame, frame, mask=mask)

                # Now crop
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

                # Read the number plate
                text = pytesseract.image_to_string(Cropped, config='--psm 11')
                if len(text) >= 5:
                    cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
                    if text == number_plate:
                        if not os.path.exists('captured vehicle images/' + number_plate):
                            os.makedirs('captured vehicle images/' + number_plate)
                        save_img_name = 'captured vehicle images/' + number_plate + '/' + namegenerator.gen() + '.jpg'
                        cv2.imwrite(filename=save_img_name, img=frame)
                        messg.show_toast("Number Plate founded", number_plate)

                #   #print("Detected Number is:", text)
                # print("counter = ", counter)

                # cv2.imshow('image', img)
                # cv2.imshow('Cropped', Cropped)
                screenCnt = None

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)

            name = 'unknown'

            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces_name[first_match_index]

            frame = cv2.rectangle(frame, (left, top + 4), (right, bottom), (0, 255, 0), 2)

            frame = cv2.putText(frame, (name), (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 1)

            if name is not 'unknown':
                if not os.path.exists('captured images/'+name):
                    os.makedirs('captured images/'+name)
                save_img_name = 'captured images/' + name + '/' + namegenerator.gen() + '.jpg'
                cv2.imwrite(filename=save_img_name, img=frame)
                messg.show_toast("Person founded", name)

        cv2.imshow("capt", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


#eel.start('home.html')