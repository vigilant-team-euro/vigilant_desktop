import pyrebase


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
    


