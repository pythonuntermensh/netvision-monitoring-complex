from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import update_statuses
from config import CRON_INTERVAL

scheduler = BackgroundScheduler(job_defaults={'max_instances': 4})

scheduler.add_job(update_statuses, 'interval', seconds=CRON_INTERVAL)
