# Beginning stages of code where we tried to use the requests library to view the stream
# on a cloud service, but unfortunately it was not what we expected.
# Written and implemented by Anthony Sandi

import requests
import cv2

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

def detect_bounding_box(cap):
    gray_image = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(cap, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

while True:
    success, img = cap.read()
    if success:
        faces = detect_bounding_box(
            img)
        cv2.imshow("OUTPUT", img)
        _, imdata = cv2.imencode('.JPG', img)
        print('.', end='', flush=True)
        requests.put('https://opencv-339022930102.us-west2.run.app/upload', data=imdata.tobytes())

    if cv2.waitKey(40) == 27: 
        break

cv2.destroyAllWindows()
cap.release()
