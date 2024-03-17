import cv2
import os
from deepface import DeepFace
import supervision as sv
from ultralytics import YOLO

FRAMES_OUTPUT_FOLDER = "frames"

def analyze_deep_face(source_path:str, interval_seconds:int): # Path can be RTSP URL or local file path
   frames_output_path = os.path.join(os.getcwd(), FRAMES_OUTPUT_FOLDER)
   if not os.path.exists(frames_output_path):
      os.makedirs(FRAMES_OUTPUT_FOLDER)
      
   cap = cv2.VideoCapture(source_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))
   frame_number = 0

   while True:
      ret, frame = cap.read()
      if not ret:
         break

      if frame_number % (fps * interval_seconds) == 0:
         output_path = os.path.join(frames_output_path, f"frame_{frame_number}.jpg")
         cv2.imwrite(output_path, frame)
         result = DeepFace.analyze(output_path, enforce_detection=False)
         print(f"Analysis result: {result}")  

      frame_number += 1

   # remove files
   files = os.listdir(frames_output_path)
   for file in files:
      os.remove(os.path.join(frames_output_path, file))

   cap.release()
   
HEATMAP_DEFAULT_PATH = 'images/heatmap.png'

def generate_heatmap(source_path:str, interval_seconds:int):
   model = YOLO('yolov8x.pt')
   cap = cv2.VideoCapture(source_path)
   fps = int(cap.get(cv2.CAP_PROP_FPS))

   heat_map_annotator = sv.HeatMapAnnotator()

   video_info = sv.VideoInfo.from_video_path(video_path=source_path)
   frames_generator = sv.get_video_frames_generator(source_path=source_path, stride=interval_seconds * fps)

   annotated_frame = None

   for frame in frames_generator:
      result = model(frame)[0]
      detections = sv.Detections.from_ultralytics(result)
      annotated_frame = heat_map_annotator.annotate(
         scene=frame.copy(),            
         detections=detections)
         
   cv2.imwrite(HEATMAP_DEFAULT_PATH, annotated_frame)