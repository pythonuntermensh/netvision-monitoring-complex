import logging
from service import get_camera_list, get_statuses, send_statuses, get_complex_list


logger = logging.getLogger('overseer_default')


def update_statuses():
    cameras = get_camera_list()
    complexes = get_complex_list()

    statuses = get_statuses(cameras, complexes)
    if len(statuses) < 1:
        return

    send_statuses(statuses)
