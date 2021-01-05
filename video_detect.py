import face_recognition
import cv2
import os
import namegenerator
import eel
from win10toast import ToastNotifier


#eel.init('web')
#@eel.expose
def recognizeface():
    messg = ToastNotifier()

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