from application.Models.models import User
from flask import escape
from base64 import b64decode, b64encode
import json
from datetime import datetime
from application import app
import os
from geopy.distance import geodesic

notLoggedIn = dict({
    "isLoggedIn": False,
    'message': 'Your are not logged in'
})
found = dict({
    "isLoggedIn": True,
})

dataUpdateResponse = dict({
    "isLoggedIn": True,
    'isUpdated': True,
})

dataNotUpdateResponse = dict({
    "isLoggedIn": True,
    'isUpdated': False,
})

dataSavedResponse = dict({
    "isLoggedIn": True,
    'isSaved': True,
})

dataNotSavedResponse = dict({
    "isLoggedIn": True,
    'isSaved': False,
})

invalidArgsResponse = dict({
    "isLoggedIn": True,
    "isError": True,
    'message': 'Invalid data',
})
def AuthorizeRequest(headers):
    if not 'Authorization' in headers:
        return False

    token = headers['Authorization']
    # token = escape(token)
    # token_str = str(token).encode('ascii')
    # missing_padding = len(token_str) % 4
    # if missing_padding:
    #     return False
    #
    # token = b64decode(token_str)
    user = User.query.filter_by(token=token)
    if not user.count() > 0:
        return False

    return user.first()


def isBase64(s):
    try:
        if b64encode(b64decode(s)) == s:
            return get_decoded(s)
        return False
    except Exception:
        return False

def get_decoded(data):
    data = str(data).encode('ascii')
    missing_padding = len(data) % 4
    if missing_padding:
        return False
    try:
        data = b64decode(data)
        data = json.loads(data)
        return data
    except:
        return False

def b64_to_data(data):
    data = str(data).encode('ascii')
    missing_padding = len(data) % 4
    if missing_padding:
        return False

    try:
        data = b64decode(data)
        return data
    except:
        return False


def uploadPostImage(image, user):
    dt_obj = datetime.strptime(
        str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f"
    )
    millisec = str(dt_obj.timestamp() * 1000)
    time = millisec.replace(".", "")
    imageName = user.fullname.replace(" ","") + str(user.user_id) + time + ".jpg"
    try:
        folder = os.path.join(app.root_path, 'static/posts')
        file_path = os.path.join(folder, imageName)
        image.save(file_path)
        return True, imageName
    except Exception as e:
        print(e)
        return False, None

def get_location_distance(location_1, location_2):
    return geodesic(location_1, location_2).km

