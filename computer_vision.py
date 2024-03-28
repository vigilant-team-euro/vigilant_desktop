import cv2
import os
from deepface import DeepFace
import supervision as sv
from ultralytics import YOLO
import datetime
import firebase
import threading

YOLO_MODEL_PATH = os.path.join("detection_models", 'yolov8n.pt')

AGE_INTERVALS = [0, 15, 30, 45, 60]

output_folder = "output_folder"

def construct_result(deepface_result, people_count, start_date, end_date):
   
   result = {
      "customer_count": 0,
      "fear_count": 0,
      "happy_count": 0,
      "neutral_count": 0,
      "sad_count": 0,
      "surprise_count": 0,
      "angry_count": 0,
      "female_count": 0,
      "male_count": 0,
      "start_date": start_date,
      "end_date": end_date,
   }
   
   for i in range(len(AGE_INTERVALS) - 1):
      result[f"{AGE_INTERVALS[i]}-{AGE_INTERVALS[i]}_age_count"] = 0
   
   for person in deepface_result:
      emotion = person["dominant_emotion"]
      gender = person["dominant_gender"]
      age = person["age"]
      
      result[f"total_{emotion}_count"] += 1
      
      if gender == "Man":
         result["total_male_count"] += 1
      else:
         result["total_female_count"] += 1
         
      for i in range(1, len(AGE_INTERVALS)):
         if age <= AGE_INTERVALS[i]:
            result[f"{AGE_INTERVALS[i - 1]}-{AGE_INTERVALS[i]}_age_count"] += 1
      
         
   result["customer_count"] = people_count
   
   return result
      
      
def analyze(source:str, frame_interval_seconds:int, date: datetime, heatmap_generation:bool):
   frames_arr = []
   annotated_frame_arr = {}
   
   model = YOLO(YOLO_MODEL_PATH)
   heat_map_annotator = sv.HeatMapAnnotator()
   
   cap = cv2.VideoCapture(source)
   fps = int(cap.get(cv2.CAP_PROP_FPS))
   frame_number = 0
   start_date = date
   end_date = date + datetime.timedelta(seconds=frame_interval_seconds)

   while True:
      ret, frame = cap.read()
      if not ret:
         break

      if frame_number % (fps * frame_interval_seconds) == 0:
         output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
         cv2.imwrite(output_path, frame)
         
         # Deepface analysis
         deepface_result = DeepFace.analyze(output_path, enforce_detection=False)
         
         # Counting people with YOLO
         image = cv2.imread(output_path)
         detection_result = model(image)[0]
         detections = sv.Detections.from_ultralytics(detection_result)
         detections = detections[detections.class_id == 0] # Only count people
         people_count = len(detections)
         
         result = construct_result(deepface_result, people_count, start_date, end_date)
         frames_arr.append(result)
         
         if heatmap_generation:
            annotated_frame = heat_map_annotator.annotate(scene=frame.copy(), detections=detections)
            annotated_frame_arr[start_date] = annotated_frame.tolist()
         
         start_date += datetime.timedelta(seconds=frame_interval_seconds)
         end_date += datetime.timedelta(seconds=frame_interval_seconds)

      frame_number += 1
      
   cap.release()
   
   return frames_arr, annotated_frame_arr
      
def process_video(video_path:str, frame_interval_seconds:int, username:str, store_name:str, date: datetime, heatmap_generation:bool):
   frames_arr, annotated_frame_arr = analyze(video_path, frame_interval_seconds, date, heatmap_generation)
   
   firebase.sendToDb(frames_arr, username, store_name, date)
   
   if heatmap_generation:
      firebase.send_heatmap(annotated_frame_arr, username, store_name, None)
   
   files = os.listdir(output_folder)
   for file in files:
      os.remove(os.path.join(output_folder, file))
      
def process_live_camera_footage(rtsp_url:str, frame_interval_seconds:int, username:str, store_name:str, camera_name: str, date: datetime, heatmap_generation:bool):
   frames_arr, annotated_frame_arr = analyze(rtsp_url, frame_interval_seconds, date, heatmap_generation)
   
   firebase.sendToDb(frames_arr, username, store_name, date)
   
   if heatmap_generation:
      firebase.send_heatmap(annotated_frame_arr, username, store_name, camera_name)
      
   files = os.listdir(output_folder)
   for file in files:
      os.remove(os.path.join(output_folder, file))