import os

CENSUS_URL = os.environ.get("CENSUS_URL") or "http://localhost:8000"
CAMERA_CHECK_PROTOCOL = os.environ.get("CAMERA_CHECK_PROTOCOL") or "http://"
