import requests
import json
import os
from config import FILTER_MAGNITUDE
from earthquake import Earthquake


def get_data(url):
    # get the data from Deprem Nerede Oldu API
    return requests.get(url).json()


def check_if_db_exists(path: str) -> bool:
    return os.path.isfile(path)


def filter_by_id(id, path):
    # our database
    db = open(path, "r")
    data = json.load(db)

    all_earthquakes_id_posted = [item["earthquake_id"]
                                 for item in data["earthquakes"]]

    if id in all_earthquakes_id_posted:
        return True

    return False


def check_if_new_earthquake_exists(data_json, path):
    for item in data_json["earthquakes"]:
        result = filter_by_id(id=item["earthquake_id"], path=path)

        # if result returns False, that means this is a new earthquake
        # check if his magnitude is greater than 3.5
        # and save it in the db

        if not result:  # and float(item["magnitude"]) >= FILTER_MAGNITUDE:
            earthquake = Earthquake(**item)
            created_img_path = earthquake.genereate_earthquake_image()
            response_instagram = earthquake.upload_photo_to_intagram(
                img_path=created_img_path)

            if response_instagram:
                earthquake.save_to_db()
