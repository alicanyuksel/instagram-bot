from config import (
    DB_PATH,
    ICON_URL,
    PATH_PNG_IMAGES,
    PATH_JPG_IMAGES,
    HASHTAG
)
import json
import requests
import os
import cv2
from instagrapi import Client
import logging
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')


logging.basicConfig(filename='bot.log', level=logging.DEBUG)


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

    def save_to_db(self, db_path: str = DB_PATH) -> None:
        """
        To save the earthquake in the database.

        :param db_path: database path
        :return: None
        """
        with open(db_path, 'r+') as file:
            # First we load existing database into a dict.
            db = json.load(file)

            # Join new_data
            db["earthquakes"].append(self.json())

            # Sets file's current position at offset.
            file.seek(0)

            # convert back to json
            json.dump(db, file, indent=4)

            logging.info('Data saved.')

    def generate_earthquake_image(self, path_png: str = PATH_PNG_IMAGES, path_jpg: str = PATH_JPG_IMAGES) -> str:
        """
        To generate earthquake images with Mapbox API in order to post it on Instagram.

        :param path_png: PNG images path
        :param path_jpg: JPG images path
        :return: JPG images path
        """
        img_png_path = os.path.join(path_png, f"{self.earthquake_id}.png")
        os.makedirs(os.path.dirname(img_png_path), exist_ok=True)

        img = open(img_png_path, "wb")

        path = f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/url-{ICON_URL}({self.longitude},{self.latitude})/{self.longitude},{self.latitude},6.5,0.00,0.00/1000x600@2x?access_token={ACCESS_TOKEN}"

        img.write(requests.get(path).content)
        img.close()

        # Load .png image
        image = cv2.imread(img_png_path)

        # Save .jpg image to post on Instagram (only JPG files)
        img_jpg_path = os.path.join(path_jpg, f"{self.earthquake_id}.jpg")
        cv2.imwrite(img_jpg_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        logging.info(
            f'Earthquake image generated with id : {self.earthquake_id}')

        return img_jpg_path

    def upload_photo_to_instagram(self,
                                  img_path: str,
                                  account_username: str = ACCOUNT_USERNAME,
                                  account_password: str = ACCOUNT_PASSWORD) -> bool:
        """
        To upload the generated image on Instagram.

        :param img_path: generated image path
        :param account_username: instagram username
        :param account_password: instagram password
        :return: true or false
        """
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
            logging.info('Generated image posted to Instagram !')
            return True

        except:
            logging.warning('Some problem about the Instagram connection...')
            return False
