import cv2
import os
from deepface import DeepFace
import json

def deep_face(video_path:str, interval_seconds:int):
   # video_path = "videos\store.mp4" # Change this
   output_folder = "output_folder"

   cap = cv2.VideoCapture(video_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))
   frame_number = 0

   while True:
      ret, frame = cap.read()
      if not ret:
         break

      if frame_number % (fps * interval_seconds) == 0:
         output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
         cv2.imwrite(output_path, frame)
         result = DeepFace.analyze(output_path, enforce_detection=False)
         print(f"Analysis result: {result}")  

      frame_number += 1

   # remove files
   files = os.listdir(output_folder)
   for file in files:
      os.remove(f"{output_folder}/{file}")  

   cap.release()


# def sendToDb(result:str):
#    cred = credentials.Certificate('/firebaseConfig.json')
#    app = firebase_admin.initialize_app(cred) 
#    db = firestore.client()

#    users_ref = db.collection("users")
#    docs = users_ref.stream()

#    for doc in docs:
#       print(f"{doc.id} => {doc.to_dict()}")

