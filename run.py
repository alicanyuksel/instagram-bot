from utils2 import get_data, check_if_db_exists, check_if_new_earthquake_exists
from config import DB_PATH, URL_API_BACKEND
from earthquake import Earthquake
import json


def run_bot(data_json, path):
    # to initialize the database
    if not check_if_db_exists(path=path):
        with open(path, "w") as fl:
            json_object = json.dump(data_json, fl, indent=4)

    # add new earthquakes
    else:
        check_if_new_earthquake_exists(data_json=data_json, path=path)


if __name__ == "__main__":
    data = get_data(url=URL_API_BACKEND)
    run_bot(data_json=data, path=DB_PATH)
