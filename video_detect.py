import face_recognition
import cv2

vid = cv2.VideoCapture('./pics/Trump_Obama_vid.mp4')

obama_img = face_recognition.load_image_file('./pics/obama.jpg')
obama_face_encod = face_recognition.face_encodings(obama_img)[0]

trump_img = face_recognition.load_image_file('./pics/trump.jpg')
trump_img_encod = face_recognition.face_encodings(trump_img)[0]

known_face_encoding = [
    obama_face_encod,
    trump_img_encod
]

known_faces_name = [
    "obama",
    "trump"
]

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

        frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
        frame = cv2.putText(frame, (name), (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    cv2.imshow("capt", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()