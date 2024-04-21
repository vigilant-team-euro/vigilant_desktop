import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime
import os
import numpy as np
from PIL import Image

TEMP_HEATMAP_LOCATION = os.path.join("heatmaps, heatmap.png")

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
        return user["localId"]
    except:
        return ""

def authWithGoogle():
    return True

# FIRESTORE
cred = credentials.Certificate("./firebaseConfig.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'vigilant-36758.appspot.com'})
all_db = firestore.client()
bucket = storage.bucket(app=app)

def getStores(userId):
    stores = {}
    arr = all_db.collection("users").document(userId).collection("stores").stream()
    for a in arr:
        stores[a.to_dict()["storeName"]] =  a.id
            
    return stores

def sendToDb(frames_arr:dict, username:str, store_id:str, date:datetime.datetime ):

    data = {
            "storeName": store_id,
            "frames": frames_arr
        }
    
    arr = all_db.collection("users").document(username).collection("stores").document(store_id).collection("data").document(f"{date.day}_{date.month}_{date.year}").set(data)

def send_heatmap(heatmap:np.ndarray, username:str, store_name:str, date, camera_name:str):
    
    file_name_firebase = f"view_{date}.png" if camera_name == None else f"{camera_name}_{date}.png"
    file_path_firebase = f"{username}/{store_name}/{file_name_firebase}"
    
    blob = bucket.blob(file_path_firebase)
    
    heatmap_image = Image.fromarray(heatmap)
    heatmap_image.save(TEMP_HEATMAP_LOCATION)
    
    blob.upload_from_filename(TEMP_HEATMAP_LOCATION)
    os.remove(TEMP_HEATMAP_LOCATION)