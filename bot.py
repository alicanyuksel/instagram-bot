from instagrapi import Client
import json
import datetime

# intern package
from config import (
    ACCOUNT_USERNAME,
    ACCOUNT_PASSWORD, 
    PATH_JPG, 
    earthquakes_detected_path, 
    earthquakes_posted_path,
    hashtag
)
from utils import *

earthquakes_detected = detect_earthquakes(data)
save_maps_images(earthquakes_detected)


log = open("log.txt", "a+")


# Get all of the earthquakes detected (magnitude => 3.0)
json_file_detected = open(earthquakes_detected_path)
earthquakes_detected = json.load(json_file_detected)

# Get all of the earthquakes already posted on instagram
json_file_posted = open(earthquakes_posted_path)
earthquakes_posted = json.load(json_file_posted)


# Get all of the ids of earthquakes posted if earthquakes_posted is not empty file
posted_earthquakes_ids = list(earthquakes_posted.keys() if earthquakes_posted else "")

new_earthquakes_to_post = {}

for earthquake_id, earthquake_info in earthquakes_detected.items():
    if earthquake_id not in posted_earthquakes_ids:
        new_earthquakes_to_post[earthquake_id] = earthquake_info


if new_earthquakes_to_post:
    # device settings
    settings = {'uuids': {'phone_id': 'f08ac5d5-a18f-4699-9fbc-6922343b7d63',
                'uuid': 'e3f9dfa5-b748-4d5d-88a6-08cc9148faab',
                'client_session_id': '03b01d51-9c40-40f6-acd1-780d45c1603e',
                'advertising_id': '1bcbc91b-60f3-471a-ab0f-5a2058685f33',
                'device_id': 'android-1dd69f505b6b0a99'},
                'cookies': {},
                'last_login': None,
                'device_settings': {'app_version': '105.0.0.18.119',
                'android_version': 28,
                'android_release': '9.0',
                'dpi': '640dpi',
                'resolution': '1440x2560',
                'manufacturer': 'samsung',
                'device': 'SM-G965F',
                'model': 'star2qltecs',
                'cpu': 'samsungexynos9810',
                'version_code': '168361634'},
                'user_agent': 'Instagram 105.0.0.18.119 Android (28/9.0; 640dpi; 1440x2560; samsung; SM-G965F; star2qltecs; samsungexynos9810; en_US; 168361634)'}

    #login
    cl = Client(settings=settings)
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    # set dns
    cl.set_proxy("socks5://127.0.0.1:30235")

    # set timeout 
    cl.request_timeout = 5

    count = 0
    for earthquake_id, earthquake_info in reversed(list(new_earthquakes_to_post.items())):
        description_earthquake = f"""\nLokasyon : {earthquake_info['location']}\nŞiddet : {earthquake_info['magnitude']}\nDerinlik : {earthquake_info['depth']}\nTarih - Saat : {earthquake_info['date']} - {earthquake_info['time']}\n\nDaha fazla detay için : depremneredeoldu.com\n\n{hashtag}"""

        PATH = f'{PATH_JPG}/{earthquake_id}.jpg'

        cl.photo_upload(PATH,                 
                        caption=description_earthquake)

        with open(earthquakes_posted_path, "r+") as file:
            data = json.load(file)
            data.update({earthquake_id : earthquake_info})
            file.seek(0)
            json.dump(data, file, indent=4)

        count += 1
        
    log.write(f"{count} file posted ! - {datetime.datetime.now()}\n")


