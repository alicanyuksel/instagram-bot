from instagrapi import Client
import json
import datetime

# intern package
from config import ACCOUNT_USERNAME, ACCOUNT_PASSWORD, PATH_JPG
from utils import *

earthquakes_detected = detect_earthquakes(data)
save_maps_images(earthquakes_detected)


log = open("log.txt", "a+")

def login():
    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)


# Get all of the earthquakes detected (magnitude => 3.0)
json_file_detected = open('earthquakes_detected.json')
earthquakes_detected = json.load(json_file_detected)

# Get all of the earthquakes already posted on instagram
json_file_posted = open('earthquakes_posted.json')
earthquakes_posted = json.load(json_file_posted)


# Get all of the ids of earthquakes posted if earthquakes_posted is not empty file
posted_earthquakes_ids = list(earthquakes_posted.keys() if earthquakes_posted else "")

new_earthquakes_to_post = {}

for earthquake_id, earthquake_info in earthquakes_detected.items():
    if earthquake_id not in posted_earthquakes_ids:
        new_earthquakes_to_post[earthquake_id] = earthquake_info


if new_earthquakes_to_post:
    # we can login
    login()

    count = 0
    for earthquake_id, earthquake_info in new_earthquakes_to_post.items():
        description_earthquake = f"""\nLokasyon : {earthquake_info['location']}\nŞiddet : {earthquake_info['magnitude']}\nDerinlik : {earthquake_info['depth']}\nTarih - Saat : {earthquake_info['date']} - {earthquake_info['time']}"""

        # PATH = f'{PATH_JPG}/{earthquake_id}.jpg'

        # cl.photo_upload(PATH,
        #                 caption=description_earthquake)

        with open("earthquakes_posted.json", "r+") as file:
            data = json.load(file)
            data.update({earthquake_id : earthquake_info})
            file.seek(0)
            json.dump(data, file, indent=4)

        count += 1
        
    log.write(f"{count} file posted ! - {datetime.datetime.now()}\n")

else:
    log.write(f"Nothing to post ! - {datetime.datetime.now()}\n")


