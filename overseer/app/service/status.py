from typing import Any, List

import requests, json

from config import CAMERA_CHECK_PROTOCOL
from dto.request import CameraIn
from dto.response import CameraStatusOut
from type import CameraStatus
from exception import CensusUnavailable
from config import CENSUS_URL


def get_statuses(cameras: List[CameraIn]) -> List[CameraStatusOut]:
    result = list()
    for camera in cameras:
        try:
            resp = requests.get(CAMERA_CHECK_PROTOCOL + camera.ip)
            if resp.status_code != 200:
                raise ConnectionError()

            camera_to_status: CameraStatusOut = CameraStatusOut(uuid=camera["uuid"],
                                                                status=CameraStatus.OK.value)

        except Exception as err:  # Впадлу мне смотреть че там за ошибки, так что обобщим.
            camera_to_status: CameraStatusOut = CameraStatusOut(uuid=camera["uuid"],
                                                                status=CameraStatus.BAD.value)

        result.append(camera_to_status)
    return result


def send_statuses(cameras_to_statuses: List[CameraStatusOut]) -> None:
    data_to_send = [x.to_dict() for x in cameras_to_statuses]
    response = requests.post(CENSUS_URL + "/statuses/", data=json.dumps(data_to_send))
    if not response.status_code == 200:
        raise CensusUnavailable("Couldn't sent new statuses request to the census server")
