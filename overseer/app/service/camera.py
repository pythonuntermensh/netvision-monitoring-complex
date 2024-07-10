from typing import Any

import requests

from config import CENSUS_URL


def get_camera_list() -> Any:
    response = requests.get(CENSUS_URL + "/cameras")

    if response.status_code == 200:
        return response.json()

    return None

