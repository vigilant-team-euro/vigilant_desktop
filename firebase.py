import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from datetime import timedelta

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

def getStoreNames(username):
    store_names = []
    arr = all_db.collection("users").document(username).collection("stores").stream()

    for a in arr:
        store_names.append(a.to_dict()["store_name"])
    
    return store_names





