import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from datetime import timedelta
import random

cred = credentials.Certificate("./firebaseConfig.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'vigilant-36758.appspot.com'})
all_db = firestore.client()
AGE_INTERVALS = [0, 15, 30, 45, 60]

def pushRandomData(username:str, storename:str, day:int, month:int, year:int, interval:int):
    
    start_date = datetime.datetime(year, month, day, 0, 0)
    date = datetime.datetime(year, month, day, 0, 0, 0)
    end_date = start_date + timedelta(minutes=interval)
    frame_id = 1
    
    frames_arr = []
    
    while end_date.time() != datetime.time(0, 0):
        print(start_date, end_date)
        female_count = random.randint(0,20)
        male_count = random.randint(0,20)

        arr = {
        "frame_id":frame_id,
        "start_date": start_date,
        "end_date": end_date,
        "customer_count": female_count + male_count,
        "female_count": female_count,
        "male_count":male_count,
        "fear_count": random.randint(0,5),
        "happy_count":random.randint(0,5),
        "happy_count": random.randint(0,5),
        "surprise_count":random.randint(0,5),
        }

        customer_count = arr["customer_count"]
        arr["neutral_count"] = customer_count - (arr["fear_count"] + arr["happy_count"] + arr["happy_count"] + arr["surprise_count"])

        tmp_count = 0
        for i in range(len(AGE_INTERVALS) - 2):
            arr[f"{AGE_INTERVALS[i]}-{AGE_INTERVALS[i + 1]}_age_count"] = random.randint(0,5)
            tmp_count += arr[f"{AGE_INTERVALS[i]}-{AGE_INTERVALS[i + 1]}_age_count"]
        
        arr["45-60_age_count"] = customer_count - tmp_count

        frames_arr.append(arr)

        if(end_date.time() == datetime.time(0, 0)):
            break

        start_date += timedelta(minutes=interval)
        end_date += timedelta(minutes=interval)
        frame_id += 1

    data = {
            "storeName": "store1",
            "date": date,
            "frames": frames_arr
        }

    arr = all_db.collection("users").document(username).collection("stores").document(storename).collection("data").document(f"{day}_{month}_{year}").set(data)


if __name__ == '__main__':
    month = 4
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 21, month, 2024, 3)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 22, month, 2024, 5)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 23, month, 2024, 10)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 24, month, 2024, 15)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 25, month, 2024, 20)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 26, month, 2024, 6)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 27, month, 2024, 12)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 28, month, 2024, 5)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 29, month, 2024, 10)
    pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "17kG38Y5tTJWh74TyM84", 30, month, 2024, 10)

    # pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "8rhk8kbOqpZmFYTARwgo", 15, month, 2024, 240)
    # pushRandomData("F3sSGpLf1YORxmOPuniEBCUZrH22", "8rhk8kbOqpZmFYTARwgo", 16, month, 2024, 480)