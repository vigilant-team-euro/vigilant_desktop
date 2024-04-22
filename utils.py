import os
import sqlite3
import cv2
from firebase import authWithMail, getStores
import numpy as np
from PIL import Image

CAMERA_INFO_FOLDER = "camera_info_data"
CAMERA_INFO_DB_FILE = "camera_information.db"

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;1000"

#auth from firebase, return True if success
def auth_user(username, password):
    user = authWithMail(username, password)
    stores = getStores(user)

    user_info = {
        'user': user,
        'stores': stores
    }
    return user_info
        
def auth_user_google():
    return True

#logout from firebase, return True if success
def is_user_logged_out():
    return True

def get_cameras():
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT camera_name, ip_address, store_name FROM cameras")
    cameras = cursor.fetchall()
    connection.close()
    return cameras

def add_camera(camera_name, camera_ip, camera_port, camera_username, camera_password, store_name):
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    primary_key_error = ""
    try:
        cursor.execute(f"INSERT INTO cameras (camera_name, ip_address, port, username, password, store_name) VALUES ('{camera_name}', '{camera_ip}', {camera_port}, '{camera_username}', '{camera_password}', '{store_name}')")
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        print("Failed to insert data due to duplicate primary key")
        primary_key_error = "Camera names should be unique"
    finally:
        connection.close()
        return primary_key_error

def edit_camera_ip(camera_name, new_ip):
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    db_error = ""
    try:
        cursor.execute(f"UPDATE cameras SET ip_address = '{new_ip}' WHERE camera_name = '{camera_name}'")
        connection.commit()
    except sqlite3.Error as e:
        db_error = e
    finally:
        connection.close()
        return db_error

def remove_camera(camera_name):
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    db_error = ""
    try:
        cursor.execute(f"DELETE FROM cameras WHERE camera_name = '{camera_name}'")
        connection.commit()
    except sqlite3.Error as e:
        db_error = e
    finally:
        connection.close()
        return db_error

def get_store_cameras(store_name):
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(f"SELECT camera_name FROM cameras WHERE store_name = '{store_name}'")
    result = cursor.fetchall()
    connection.close()

    camera_names = []
    for camera in result:
        camera_names.append(camera[0])
    return camera_names

def construct_rtsp_url(camera_name):
    db_file = os.path.join(CAMERA_INFO_FOLDER, CAMERA_INFO_DB_FILE)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(f"SELECT ip_address, port, username, password FROM cameras WHERE camera_name = '{camera_name}'")
    camera_info = cursor.fetchone()
    
    ip_address = camera_info[0]
    port = camera_info[1]
    username = camera_info[2]
    password = camera_info[3]
    
    connection.close()
    
    return f"rtsp://{username}:{password}@{ip_address}:{port}/stream2"

def show_live_footage(camera_name):
    error = ""
    
    rtsp_url = construct_rtsp_url(camera_name)
    
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        error = "Failed to open RTSP stream"
        return error

    while True:
        # Read a frame from the RTSP stream
        ret, frame = cap.read()

        # Check if the frame is read correctly
        if not ret:
            error = "Failed to read frame"
            return error

        # Display the frame
        cv2.imshow("RTSP Stream", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the RTSP stream and close the window
    cap.release()
    cv2.destroyAllWindows()
    return error

def resize_heatmap(heatmap_arr: np.ndarray, target_height):
    new_heatmap_arr = []
    for heatmap in heatmap_arr:
        heatmap_img = Image.fromarray(heatmap)
        aspect_ratio = heatmap_img.width / heatmap_img.height
        new_width = int(target_height * aspect_ratio)
        new_height = target_height
        
        heatmap_img = heatmap_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_heatmap_arr.append(np.array(heatmap_img))
        
    return np.array(new_heatmap_arr)