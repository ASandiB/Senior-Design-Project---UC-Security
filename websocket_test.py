# Beginning stages of code where we tried to use the sockets library to view the stream
# on a cloud service, but unfortunately it was not what we expected.
# Written and implemented by Anthony Sandi

import cv2
import base64
import socketio

sio = socketio.Client()
sio.connect("https://opencv-339022930102.us-south1.run.app/")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    sio.emit('send_frame', frame_base64)
