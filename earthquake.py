from config import (
    DB_PATH,
    ICON_URL,
    PATH_JPG_IMAGES,
    HASHTAG
)
import json
import requests
import os
from instagrapi import Client

from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')


class Earthquake:
    def __init__(self, earthquake_id, date, depth, location, latitude, longitude, magnitude, time) -> None:

        self.earthquake_id = earthquake_id
        self.date = date
        self.depth = depth
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.magnitude = magnitude
        self.time = time

    def json(self):
        return {
            "earthquake_id": self.earthquake_id,
            "date": self.date,
            "time": self.time,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "depth": self.depth,
            "magnitude": self.magnitude,
            "location": self.location,
        }

    def save_to_db(self, db_path=DB_PATH):
        with open(db_path, 'r+') as file:
            # First we load existing database into a dict.
            db = json.load(file)

            # Join new_data
            db["earthquakes"].append(self.json())

            # Sets file's current position at offset.
            file.seek(0)

            # convert back to json
            json.dump(db, file, indent=4)

    def genereate_earthquake_image(self, path_png=PATH_JPG_IMAGES):
        img_path = os.path.join(path_png, f"{self.earthquake_id}.jpg")
        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        img = open(img_path, "wb")

        path = f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/url-{ICON_URL}({self.longitude},{self.latitude})/{self.longitude},{self.latitude},6.5,0.00,0.00/1000x600@2x?access_token={ACCESS_TOKEN}"

        img.write(requests.get(path).content)
        img.close()

        return img_path

    def upload_photo_to_instagram(self, img_path, account_username=ACCOUNT_USERNAME, account_password=ACCOUNT_PASSWORD) -> bool:
        # login
        cl = Client()
        cl.login(account_username, account_password)

        cl.request_timeout = 5  # seconds

        # description for photo
        description_earthquake = f"""
                                Lokasyon : {self.location}\nBüyüklük : {self.magnitude}\nDerinlik : {self.depth}
                                \nTarih - Saat : {self.date} - {self.time}
                                \n\nDaha fazla detay için : depremneredeoldu.com\n\n{HASHTAG}
                                """

        # upload photo
        try:
            cl.photo_upload(img_path,
                            caption=description_earthquake)
            return True

        except:
            return False
