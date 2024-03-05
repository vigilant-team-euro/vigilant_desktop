from firebase import authWithMail

#auth from firebase, return True if success
def auth_user(username, password):
    user = authWithMail(username, password)
    if "@" in user:
        return user
    else:
        return ""
        
def auth_user_google():
    return True

#logout from firebase, return True if success
def is_user_logged_out():
    return True

#camera utilies, use id of the cameras
def get_cameras():
    pass

def add_camera():
    pass

def edit_camera():
    pass

def remove_camera():
    pass

#video utils
def add_video():
    pass

def process_video():
    pass


#employee utilities, use id's of the employees from database
def get_employees():
    pass

def add_employee():
    pass

def edit_employee():
    pass

def remove_employee():
    pass

#store utilities
def get_store_info():  
    pass



