import os
import sqlite3

CAMERA_INFO_FOLDER = "camera_info_data"
CAMERA_INFO_DB_FILE = "camera_information.db"

#auth from firebase, return True if success
def auth_user(username, password):
    return True

#logout from firebase, return True if success
def is_user_logged_out():
    return True

#camera utilies, use id of the cameras
def get_cameras():
    pass

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

def edit_camera():
    pass

def remove_camera():
    pass

#video utils
def add_video():
    pass

def process_video():
    pass