from instagrapi import Client
import json
import datetime
import logging

# intern package
from config import (
    ACCOUNT_USERNAME,
    ACCOUNT_PASSWORD,
    PATH_JPG,
    JSON_PATH,
    hashtag
)
from utils import *

# detect the earthquakes and save them into json file
earthquakes_detected = detect_earthquakes(data)

# save maps generated from MapBox API
save_maps_images(earthquakes_detected)

#  create the log files
log = open("log.txt", "a+")
logging.basicConfig(filename='log_bot.log')

# Get all of the earthquakes detected (magnitude => 3.0)
json_file_detected = open(JSON_PATH["earthquakes_detected"], "r")
earthquakes_detected = json.load(json_file_detected)

# Create a json file to store the earthquakes posted on our account
if not os.path.exists(JSON_PATH["earthquakes_posted"]):
    create_json(dictionary={}, path=JSON_PATH["earthquakes_posted"])

# Get all of the earthquakes already posted on instagram
json_file_posted = open(JSON_PATH["earthquakes_posted"])
earthquakes_posted = json.load(json_file_posted)

# Get all of the ids of earthquakes posted if earthquakes_posted is not empty file
posted_earthquakes_ids = list(earthquakes_posted.keys() if earthquakes_posted else "")

new_earthquakes_to_post = {}

for earthquake_id, earthquake_info in earthquakes_detected.items():
    if earthquake_id not in posted_earthquakes_ids:
        new_earthquakes_to_post[earthquake_id] = earthquake_info

if new_earthquakes_to_post:
    # login
    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    # logging 
    cl.request_logger = logging.getLogger("private_request")

    count = 0
    for earthquake_id, earthquake_info in reversed(list(new_earthquakes_to_post.items())):
        description_earthquake = f"""\nLokasyon : {earthquake_info['location']}\nBüyüklük : {earthquake_info['magnitude']}\nDerinlik : {earthquake_info['depth']}\nTarih - Saat : {earthquake_info['date']} - {earthquake_info['time']}\n\nDaha fazla detay için : depremneredeoldu.com\n\n{hashtag}"""

        PATH = f'{PATH_JPG}/{earthquake_id}.jpg'

        # set timeout 
        cl.request_timeout = 5

        cl.photo_upload(PATH,
                        caption=description_earthquake)

        with open(JSON_PATH["earthquakes_posted"], "r+") as file:
            data = json.load(file)
            data.update({earthquake_id: earthquake_info})
            file.seek(0)
            json.dump(data, file, indent=4)

        count += 1

    log.write(f"{count} file posted ! - {datetime.datetime.now()}\n")
