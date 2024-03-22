import cv2
import os
from deepface import DeepFace
import datetime
import firebase

def createFrame():
      list = {
         "average_age": 0,
         "customer_count":0,
         "fear_count":0,
         "happy_count":0,
         "neutral_count":0,
         "sad_count":0,
         "surprise_count":0,
         "female_count":0,
         "male_count":0,
         "start_date": datetime.datetime.now(),
         "end_date": datetime.datetime.now(),
         "frame_id":0,
      }
      return list

def pushResult(result:dict, list:list):
   for result_list in result:
      emotion = result_list["dominant_emotion"]
      gender = result_list["dominant_gender"]
      age = result_list["age"]

      if emotion == "sad":
         list["sad_count"] += 1
      if emotion == "fear":
         list["fear_count"] += 1
      if emotion == "happy":
         list["happy_count"] += 1
      if emotion == "neutral":
         list["neutral_count"] += 1
      if emotion == "surprise":
         list["surprise_count"] += 1

      if gender == "Man":
         list["male_count"] += 1
      if gender == "Woman":
         list["female_count"] += 1

      list["average_age"] += age
      list["customer_count"] += 1

def deep_face(video_path:str, interval_seconds:int, username:str, store_name:str, date: datetime):
   output_folder = "output_folder"

   cap = cv2.VideoCapture(video_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))
   frame_number = 0
   result_count = 0
   frame_id = 1
   start_date = date
   end_date = date + datetime.timedelta(minutes=3)

   frames_arr = []
   frame = {}
   frameResult = createFrame()
   result = []

   while True:
      ret, frame = cap.read()
      if not ret:
         frameResult["average_age"] = (int) (frameResult["average_age"] / frameResult["customer_count"])
         frameResult["frame_id"] = frame_id
         frameResult["start_date"] = start_date
         frameResult["end_date"] = end_date
         frames_arr.append(frameResult)
         break

      if frame_number % (fps * interval_seconds) == 0:
         output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
         cv2.imwrite(output_path, frame)
         result = DeepFace.analyze(output_path, enforce_detection=False)
         pushResult(result, frameResult)
         result_count += 1
         
         if result_count % (180 / interval_seconds) == 0:
            frameResult["average_age"] = (int) (frameResult["average_age"] / frameResult["customer_count"])
            frameResult["frame_id"] = frame_id
            frameResult["start_date"] = start_date
            frameResult["end_date"] = end_date

            frame_id += 1
            start_date += datetime.timedelta(minutes=3)
            end_date += datetime.timedelta(minutes=3)
            frames_arr.append(frameResult)
            frameResult = createFrame()


      frame_number += 1

   firebase.sendToDb(frames_arr, username, store_name, start_date)
   print(frames_arr)

   # remove files
   files = os.listdir(output_folder)
   for file in files:
      os.remove(f"{output_folder}/{file}")  

   cap.release()


