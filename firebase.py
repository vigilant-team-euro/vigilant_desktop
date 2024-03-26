import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime
from datetime import timedelta
import os
import json

TEMP_HEATMAP_LOCATION = os.path.join("heatmaps, heatmap.json")

firebaseConfig = {
  "apiKey": "AIzaSyBxDTNJ-jV6_ln3tSCyASYYacMcESgZtRk",
  "authDomain": "vigilant-36758.firebaseapp.com",
  "projectId": "vigilant-36758",
  "storageBucket": "vigilant-36758.appspot.com",
  "messagingSenderId": "14332637896",
  "appId": "1:14332637896:web:7e53a790a003cb2204abfd",
  "measurementId": "G-K0GKXG9BX9",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def authWithMail(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user["email"]
    except:
        return ""

def authWithGoogle():
    return True

# FIRESTORE
cred = credentials.Certificate("./firebaseConfig.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'vigilant-36758.appspot.com'})
all_db = firestore.client()
bucket = storage.bucket(app=app)

def getStoreNames(username):
    store_names = []
    arr = all_db.collection("users").document(username).collection("stores").stream()

    for a in arr:
        store_names.append(a.to_dict()["store_name"])
    
    return store_names

def sendToDb(frames_arr:dict, username:str, store_name:str, date:datetime.datetime ):

    data = {
            "storeName": store_name,
            "frames": frames_arr
        }
    
    arr = all_db.collection("users").document(username).collection("stores").document(store_name).collection("data").document(f"{date.day}_{date.month}_{date.year}").set(data)

def send_heatmap(annotated_frames:dict, username:str, store_name:str, camera_name:str):
    
    file_name_firebase = f"view_heatmap.json" if camera_name == None else f"{camera_name}_heatmap.json"
    file_path_firebase = f"{username}/{store_name}/{file_name_firebase}"
    
    temp_annotated_frames = {}
    blob = bucket.blob(file_path_firebase)
    
    if blob.exists():
        blob.download_to_filename(TEMP_HEATMAP_LOCATION)
        with open(TEMP_HEATMAP_LOCATION, "r") as f:
            data = f.read()
            
        temp_annotated_frames = json.loads(data)
        
        for key, value in annotated_frames.items():
            temp_annotated_frames[key] = value
    else:
        temp_annotated_frames = annotated_frames
    
    json_data = json.dumps(temp_annotated_frames)
    blob.upload_from_string(json_data)