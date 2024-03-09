import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from datetime import timedelta
import random


def pushRandomData():
    cred = credentials.Certificate("./firebaseConfig.json")
    app = firebase_admin.initialize_app(cred, {'storageBucket': 'vigilant-36758.appspot.com'})
    all_db = firestore.client()

    start_date = datetime.datetime(2024, 3, 7, 0, 0)
    end_date = start_date + timedelta(minutes=3)
    frame_id = 1

    while end_date.time() != datetime.time(0, 0):
        print(start_date, end_date)
        female_count = random.randint(0,50)
        male_count = random.randint(0,55)

        arr = {
        "average_age": random.randint(10,55),
        "customer_count": female_count + male_count,
        "fear_count": random.randint(0,10),
        "female_count": female_count,
        "frame_id":frame_id,
        "happy_count":random.randint(0,10),
        "male_count":male_count,
        "neutral_count":random.randint(0,10),
        "sad_count": random.randint(0,10),
        "surprise_count":random.randint(0,10)
        }

        data = {
            "start_date": start_date,
            "end_date": end_date,
            "count": arr["female_count"] + arr["male_count"],
            "storeName": "store1",
            "frames": arr
        }

        arr = all_db.collection("users").document("random_user").collection("stores").document("store1").collection("data").document(start_date.strftime("%d.%m.%Y") + "_" + str(frame_id)).set(data)

        

        if(end_date.time() == datetime.time(0, 0)):
            break

        start_date += timedelta(minutes=3)
        end_date += timedelta(minutes=3)
        frame_id += 1


if __name__ == '__main__':
    pushRandomData()