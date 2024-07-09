from service import get_camera_list, get_statuses, send_statuses


def update_statuses():
    cameras = get_camera_list()
    if cameras is None:
        return
        # log smth

    statuses = get_statuses(cameras)
    print(statuses)
    if statuses is None:
        return
        # log smth

    if not send_statuses(statuses):
        pass
        # log smth
