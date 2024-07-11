from typing import Any, List

import requests, json

from config import CAMERA_CHECK_PROTOCOL
from dto.response import CameraStatusOut
from type import CameraStatus
from exception import CensusUnavailable
from config import CENSUS_URL, CAMERA_CHECK_TIMEOUT
from config.log_config import get_default_logger

logger = get_default_logger()


def __get_complexes_to_cameras_map(cameras_response):  # Это пиздец, но я устал. Мне можно. Потом переделаю
    result = {}
    for camera in cameras_response:
        if not camera["complex_uuid"] in result.keys():
            result[camera["complex_uuid"]] = []

        result[camera["complex_uuid"]].append((camera["uuid"], camera["id"]))

    return result


def __find_complex_data(complexes_response, uuid):
    for complex in complexes_response:
        if complex["uuid"] == str(uuid):
            return complex["ip"] + ":" + str(complex["port"]), complex["login"], complex["password"]


def get_statuses(cameras_response, complexes_response) -> List[CameraStatusOut]:
    result = list()

    complexes_to_cameras = __get_complexes_to_cameras_map(cameras_response)
    for complex_uuid, cameras_data_list in complexes_to_cameras.items():
        url, login, password = __find_complex_data(complexes_response, complex_uuid)
        logger.info("Trying to auth using url: " + url)
        try:
            logger.info("Sending auth request to the address: " + "http://" + url + "/api/v1/auth")
            auth_response = requests.post("http://" + url + "/api/v1/auth",
                                          timeout=3, data=json.dumps({"login": login, "password": password}),
                                          headers={"Content-Type": "application/json"})
            logger.info("Auth response: " + str(auth_response.status_code) + " : " + auth_response.text)
            access_token = auth_response.json()["access_token"]
        except Exception as err:
            logger.warning("Couldn't authorize using this url: " + "http://" + url + "/api/v1/auth")
            logger.warning("The error message: " + str(err))
            continue
        for data in cameras_data_list:
            try:
                logger.info("Sending camera checking request to the address: " + CAMERA_CHECK_PROTOCOL + url + "/stream/recognition/" + str(data[1]) + "/snapshot")
                resp = requests.get(CAMERA_CHECK_PROTOCOL + url + "/stream/recognition/" + str(data[1]) + "/snapshot",
                                    timeout=CAMERA_CHECK_TIMEOUT, headers={"access-token": access_token, "Content-Type": "application/json"})
                logger.info("Camera check response: " + str(resp.status_code) + " : " + resp.text)

                if resp.status_code != 200:
                    raise ConnectionError()

                camera_to_status: CameraStatusOut = CameraStatusOut(uuid=data[0],
                                                                    id=data[1],
                                                                    status=CameraStatus.OK.value)
                logger.info("Connected successfully to the " + url + " - " + str(data[1]))

            except Exception as err:  # Впадлу мне смотреть че там за ошибки, так что обобщим.
                logger.warning(
                    "Couldn't connect to the " + url + " - " + str(data[1]) + " due to exception: " + str(err))
                camera_to_status: CameraStatusOut = CameraStatusOut(uuid=data[0],
                                                                    id=data[1],
                                                                    status=CameraStatus.BAD.value)

            result.append(camera_to_status)

    logger.info(result)
    return result


def send_statuses(cameras_to_statuses: List[CameraStatusOut]) -> None:
    data_to_send = json.dumps([x.to_dict() for x in cameras_to_statuses])
    logger.info("Sending new statuses with the payload: " + data_to_send)
    response = requests.post(CENSUS_URL + "/statuses/", data=data_to_send)
    if not response.status_code == 200:
        raise CensusUnavailable("Couldn't sent new statuses request to the census server")

# complex_url/api/v1/cameras - get cams - [ {"id": num, "url": str, "active": bool, "description": str} ]
# complex_url/stream/recognition/cam_id/snapshot - TIMEOUT 10s
# complex_url/api/v1/traffic-zones/version - { "version": "0.3.15" }
