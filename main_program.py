# This is our main file for our project as it handles almost all the
# bluetooth, facial recognition, and webapp communication on our system.
# How we trained the model is on the other file called training_model.py
import cv2
import numpy as np
import pickle
import serial
import time
import requests
import streamlit as st
import tempfile
import subprocess
import os
# BLE connection with the ESP32
bluetooth = serial.Serial("/dev/rfcomm7", baudrate=9600, timeout=1)
# Facial Recognition setup
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
recognizer = cv2.face.LBPHFaceRecognizer_create()
# .yml file created with 200 Anthony Sandi's facial images
recognizer.read("trainer.yml") 
# Initializing the camera feed
video_capture = cv2.VideoCapture(0)
# Flask application variables
url = 'https://opencv-339022930102.us-west3.run.app/time'

headers = {'Content-type':'application/json','accept': 'application/json'}
# Labels for the trainer.yml file
labels = {"person_name":1}

with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

# Streamlit information for our demo at the Open House
st.title("Video Demo for Senior Design")

frameplaceholder = st.empty()

stop_button = st.button("Stop")
# Main Code
while True:
    received_data = bluetooth.readline().decode('utf-8').strip() # Data from the ESP32
    # Sends the requests post data to the url provided above
    if received_data == "Door Opened!":
         data = {"current_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
         response = requests.post(url, json=data, headers=headers)
    # If the PIR sensor detects movement, then the main code will start
    if received_data == "Someone's Here!":
        print("Someone is here!")
        # Variables for the recognizer and classifer
        ret,frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            id_,conf = recognizer.predict(roi_gray) # Puts the prediction in conf
            # Only labels the face as positive if the confidence is in a certain range
            if conf>=45 and conf<= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame,name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                bluetooth.write("Familiar Face!\n".encode('utf-8'))
            img_item = "my_image.png"
            # Facial Recognition boxes for any face
            cv2.imwrite(img_item, roi_gray)
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
            cv2.imshow('frame',frame)
    # Outputs the frames on the Streamlit application for demo
    frameplaceholder.image(frame, channels="BGR")
    if cv2.waitKey(1) & 0xFF == ord("q") or stop_button:
        break
# Ends the feed once interrupted
video_capture.release()
cv2.destroyAllWindows()
