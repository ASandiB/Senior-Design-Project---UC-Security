# We trained our model for the facial recognition using this python script. We kept the file locally on
# the Raspberry Pi, but for future editions, this file would be uploaded to a cloud for keeping.
# Written and implemented by Anthony Sandi

import os
import numpy as np
import cv2
from PIL import Image
import pickle

# Path containing 200 of Anthony Sandi
image_dir = '/home/project/dataset/1'

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
# Recognizer that we used for facial recognition
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

# Written with help of various Youtube videos, offical documentation, and Stackoverflow
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace("", "-").lower()
            print(label,path)
            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id += 1
                
            id_ = label_ids[label]
            
            pil_image = Image.open(path).convert("L")
            image_array = np.array(pil_image, "uint8")
            
            faces = face_cascade.detectMultiScale(image_array, 1.1, 5)
            
            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids,f)
recognizer.train(x_train,np.array(y_labels))
# Saves the file as trainer.yml
recognizer.save("trainer.yml")
