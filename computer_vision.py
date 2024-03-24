import cv2
import os
from deepface import DeepFace
import supervision as sv
from ultralytics import YOLO
import datetime
import firebase
import threading

YOLO_MODEL_PATH = os.path.join("detection_models", 'yolov8n.pt')

TEMP_HEATMAP_LOCATION = os.path.join("heatmaps, heatmap.png")

AGE_INTERVALS = [0, 15, 30, 45, 60]

# Global Variables for threading
frames_arr = []
annotated_frame = None
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
      
      
def analyze(video_path:str, frame_interval_seconds:int, date: datetime):
   model = YOLO(YOLO_MODEL_PATH)
   
   cap = cv2.VideoCapture(video_path)
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
         
         start_date += datetime.timedelta(seconds=frame_interval_seconds)
         end_date += datetime.timedelta(seconds=frame_interval_seconds)


      frame_number += 1
      
   cap.release()

def generate_heatmap(source_path:str, interval_seconds:int, heatmap_generation:bool):
   if not heatmap_generation:
      return
   global annotated_frame
   model = YOLO(YOLO_MODEL_PATH)
   cap = cv2.VideoCapture(source_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))

   heat_map_annotator = sv.HeatMapAnnotator()
   frames_generator = sv.get_video_frames_generator(source_path=source_path, stride=interval_seconds * fps)

   for frame in frames_generator:
      result = model(frame)[0]
      print(result)
      detections = sv.Detections.from_ultralytics(result)
      annotated_frame = heat_map_annotator.annotate(
         scene=frame.copy(),            
         detections=detections)
      
      
def process_video(video_path:str, frame_interval_seconds:int, username:str, store_name:str, date: datetime, heatmap_generation:bool):
   t1 = threading.Thread(target=analyze, args=(video_path, frame_interval_seconds, date))
   t2 = threading.Thread(target=generate_heatmap, args=(video_path, frame_interval_seconds, heatmap_generation))
   
   t1.start()
   t2.start()
   
   t1.join()
   t2.join()
   
   firebase.sendToDb(frames_arr, username, store_name, date)
   
   if heatmap_generation:
      cv2.imwrite(TEMP_HEATMAP_LOCATION, annotated_frame)
      firebase.send_heatmap(username, store_name, date)
   
   # remove files
   files = os.listdir(output_folder)
   for file in files:
      os.remove(os.path.join(output_folder, file))