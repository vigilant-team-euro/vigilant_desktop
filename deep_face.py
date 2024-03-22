import cv2
import os
from deepface import DeepFace
import datetime
import firebase

FIREBASE_PUSH_INTERVAL_SECONDS = 60
SECONDS_IN_MINUTE = 60

def construct_total_result():
   return {
      "total_age": 0,
      "total_customer_count": 0,
      "total_fear_count": 0,
      "total_happy_count": 0,
      "total_neutral_count": 0,
      "total_sad_count": 0,
      "total_surprise_count": 0,
      "total_female_count": 0,
      "total_male_count": 0,
      "start_date": datetime.datetime.now(),
      "end_date": datetime.datetime.now(),
      "frame_id":0,
   }
   
def update_total_result(deepface_result, total_result):
   for person in deepface_result:
      emotion = person["dominant_emotion"]
      gender = person["dominant_gender"]
      age = person["age"]
      
      total_result[f"total_{emotion}_count"] += 1
      
      if gender == "Man":
         total_result["total_male_count"] += 1
      else:
         total_result["total_female_count"] += 1
         
      total_result["total_age"] += age
      total_result["total_customer_count"] += 1
      

def deep_face(video_path:str, frame_interval_seconds:int, username:str, store_name:str, date: datetime):
   output_folder = "output_folder"

   cap = cv2.VideoCapture(video_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))
   frame_number = 0
   result_count = 0
   frame_id = 1
   start_date = date
   end_date = date + datetime.timedelta(minutes=FIREBASE_PUSH_INTERVAL_SECONDS / SECONDS_IN_MINUTE)

   frames_arr = []
   total_result = construct_total_result()

   while True:
      ret, frame = cap.read()
      if not ret:
         break

      if frame_number % (fps * frame_interval_seconds) == 0:
         output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
         cv2.imwrite(output_path, frame)
         result = DeepFace.analyze(output_path, enforce_detection=False)
         update_total_result(result, total_result)
         result_count += 1
         
         if result_count % (FIREBASE_PUSH_INTERVAL_SECONDS / frame_interval_seconds) == 0:
            
            num_of_frames = FIREBASE_PUSH_INTERVAL_SECONDS / frame_interval_seconds

            average_result = {
               "average_age": total_result["total_age"] / total_result["total_customer_count"],
               "customer_count": total_result["total_customer_count"] / num_of_frames,
               "fear_count": total_result["total_fear_count"] / num_of_frames,
               "happy_count": total_result["total_happy_count"] / num_of_frames,
               "neutral_count": total_result["total_neutral_count"] / num_of_frames,
               "sad_count": total_result["total_sad_count"] / num_of_frames,
               "surprise_count": total_result["total_surprise_count"] / num_of_frames,
               "female_count": total_result["total_female_count"] / num_of_frames,
               "male_count": total_result["total_male_count"] / num_of_frames,
               "start_date": start_date,
               "end_date": end_date,
               "frame_id": frame_id,
            }
            
            frame_id += 1
            start_date += datetime.timedelta(minutes=FIREBASE_PUSH_INTERVAL_SECONDS / SECONDS_IN_MINUTE)
            end_date += datetime.timedelta(minutes=FIREBASE_PUSH_INTERVAL_SECONDS / SECONDS_IN_MINUTE)
            frames_arr.append(average_result)
            total_result = construct_total_result()


      frame_number += 1

   firebase.sendToDb(frames_arr, username, store_name, start_date)
   print(frames_arr)

   # remove files
   files = os.listdir(output_folder)
   for file in files:
      os.remove(os.path.join(output_folder, file))

   cap.release()