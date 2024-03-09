import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from datetime import timedelta
import random

cred = credentials.Certificate("./firebaseConfig.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'vigilant-36758.appspot.com'})
all_db = firestore.client()

def pushRandomData(username:str, storename:str, day:int, month:int, year:int, interval:int):
    
    start_date = datetime.datetime(year, month, day, 0, 0)
    end_date = start_date + timedelta(minutes=interval)
    frame_id = 1
    
    frames_arr = []
    
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
        "surprise_count":random.randint(0,10),
        "start_date": start_date,
        "end_date": end_date
        }
        
        frames_arr.append(arr)

        if(end_date.time() == datetime.time(0, 0)):
            break

        start_date += timedelta(minutes=interval)
        end_date += timedelta(minutes=interval)
        frame_id += 1
        
    data = {
            "storeName": "store1",
            "frames": frames_arr
        }

    arr = all_db.collection("users").document(username).collection("stores").document(storename).collection("data").document(f"{day}_{month}_{year}").set(data)


if __name__ == '__main__':
    pushRandomData("random_user2", "store1", 8, 3, 2024, 3)
    pushRandomData("random_user2", "store1", 9, 3, 2024, 5)
    pushRandomData("random_user2", "store1", 10, 3, 2024, 10)
    pushRandomData("random_user2", "store1", 11, 3, 2024, 15)