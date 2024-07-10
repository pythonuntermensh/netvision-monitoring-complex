from typing import List

import requests

from dto.request import CameraIn
from exception import CensusUnavailable
from config import CENSUS_URL


def get_camera_list() -> List[CameraIn]:
    response = requests.get(CENSUS_URL + "/cameras/")

    if response.status_code != 200:
        raise CensusUnavailable("Couldn't send camera list request to the census server")

    return response.json()

