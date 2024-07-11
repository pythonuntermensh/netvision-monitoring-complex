import os

CRON_INTERVAL = int(os.environ.get("CRON_INTERVAL") or 5)
MAX_JOBS_INSTANCES = int(os.environ.get("MAX_JOBS_INSTANCES") or 3)
