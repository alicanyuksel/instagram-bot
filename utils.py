import requests
import cv2
import json
import string
import glob
import os
import datetime

# intern package
from config import mapbox_api_key, url_api_backend, PATH_PNG

# to create an id unique, we will use the date, time and magnitude concataneted without punctuation
exclude = string.punctuation

# get the data from Deprem Nerede Oldu API
data = requests.get(url_api_backend).json()

# log file
log = open("log.txt", "a+")


def create_json(dictionary, json_file_name):
    with open(f"{json_file_name}.json", "w") as fl:  
        json_object = json.dump(dictionary, fl, indent = 4)


def detect_earthquakes(data):
    earthquakes_detected = {}
    for earthquake in data["earthquakes"]:
        if float(earthquake["magnitude"]) >= 3.0:
            date_time_magnitude = f"{earthquake['date']}-{earthquake['time']}-{earthquake['magnitude']}"

            earthquake_id = "".join([ch for ch in date_time_magnitude if ch not in exclude])
            
            earthquakes_detected[earthquake_id] = earthquake


    create_json(dictionary=earthquakes_detected, json_file_name="earthquakes_detected")

    return earthquakes_detected
    
    

def genereate_earthquakes_images(earthquake_id, earthquake_detail, mapbox_api_key):
    all_png_files = [os.path.basename(image_file).split(".png")[0] for image_file in glob.glob(f"{PATH_PNG}/*.png")]

    if earthquake_id not in all_png_files:
        img = open(f"img/png/{earthquake_id}.png","wb")
        

        ACCESS_TOKEN = mapbox_api_key
        latitude = earthquake_detail["latitude"]
        longitude = earthquake_detail["longitude"]

        ICON_URL = 'https%3A%2F%2Fdepremneredeoldu.com%2Ffavicon%2Fmstile-150x150.png'

        path = f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/url-{ICON_URL}({longitude},{latitude})/{longitude},{latitude},5.5,0.00,0.00/1000x600?access_token={ACCESS_TOKEN}"

        img.write(requests.get(path).content)
        img.close()

        # Load .png image
        image = cv2.imread(f'img/png/{earthquake_id}.png')

        # Save .jpg image
        cv2.imwrite(f'img/jpg/{earthquake_id}.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        return True
    
    else:
        return False


def save_maps_images(earthquakes_detected):
    count = 0
    for key, earthquake_info in earthquakes_detected.items():
            result = genereate_earthquakes_images(
                earthquake_id=key,
                earthquake_detail=earthquake_info,
                mapbox_api_key=mapbox_api_key
            )

            if result:
                count+=1

    
    log.write(f"{count} new images created ! - {datetime.datetime.now()}\n")









