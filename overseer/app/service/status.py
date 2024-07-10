from typing import Any

import requests, json

from type.camera_status_codes import CameraStatus
from config import CENSUS_URL

CAMERA_CHECK_PROTOCOL = "http://"


def get_statuses(cameras: list) -> Any:
    result = []
    for camera in cameras:
        camera_to_status: dict = {"uuid": camera["uuid"]}

        try:
            resp = requests.get(CAMERA_CHECK_PROTOCOL + camera["ip"], timeout=3)
            if resp.status_code != 200:
                raise ConnectionError

            camera_to_status["status"] = CameraStatus.OK.value

        except Exception as err:
            camera_to_status["status"] = CameraStatus.BAD.value

        result.append(camera_to_status)
    return result


def send_statuses(cameras_to_statuses: list) -> bool:
    response = requests.post(CENSUS_URL + "/statuses", data=json.dumps(cameras_to_statuses))
    return response.status_code == 200
