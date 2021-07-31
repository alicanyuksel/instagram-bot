from utils import get_data, check_if_db_exists, check_if_new_earthquake_exists, filter_by_id
from config import DB_PATH, URL_API_BACKEND
from earthquake import Earthquake
import json


def run_bot(data_json, path: str) -> None:
    """
    To run the instagram bot.

    :param data_json: json_data
    :param path: database path
    :return: None
    """
    # to initialize the database
    if not check_if_db_exists(path=path):
        with open(path, "w") as fl:
            json_object = json.dump(data_json, fl, indent=4)

    # if the db exists, check if there is a new earthquake
    else:
        check_if_new_earthquake_exists(data_json=data_json, path=path)


if __name__ == "__main__":
    data = get_data(url=URL_API_BACKEND)
    run_bot(data_json=data, path=DB_PATH)
