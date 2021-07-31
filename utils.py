import requests
import json
import os
from config import FILTER_MAGNITUDE
from earthquake import Earthquake


def get_data(url: str):
    """
    To get the data from Depremneredeoldu Earthquake API.

    :param url: API url
    :return: json data
    """
    # get the data from Deprem Nerede Oldu API
    return requests.get(url).json()


def check_if_db_exists(path: str) -> bool:
    """
    To check if the db already exists.

    :param path: database path
    :return: true or false
    """
    return os.path.isfile(path)


def filter_by_id(id: str, path: str) -> bool:
    """
    To filter earthquakes by id.

    :param id: id
    :param path: database path
    :return: true or false
    """
    # our database
    db = open(path, "r")
    data = json.load(db)

    all_earthquakes_id_posted = [item["earthquake_id"]
                                 for item in data["earthquakes"]]

    if id in all_earthquakes_id_posted:
        return True

    return False


def check_if_new_earthquake_exists(data_json, path: str) -> None:
    """
    To check if new earthquakes exist.

    :param data_json: json data
    :param path: database path
    :return: None
    """
    for item in data_json["earthquakes"]:
        result = filter_by_id(id=item["earthquake_id"], path=path)

        # if result returns False, that means this is a new earthquake
        # check if his magnitude is greater than 3.5
        # and save it in the db
        if not result and float(item["magnitude"]) >= FILTER_MAGNITUDE:
            earthquake = Earthquake(**item)
            created_img_path = earthquake.generate_earthquake_image()
            response_instagram = earthquake.upload_photo_to_instagram(
                img_path=created_img_path)

            if response_instagram:
                earthquake.save_to_db()
