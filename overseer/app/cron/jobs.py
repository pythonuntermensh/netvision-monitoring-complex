from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import update_statuses
from config import CRON_INTERVAL, MAX_JOBS_INSTANCES

scheduler = BackgroundScheduler(job_defaults={'max_instances': MAX_JOBS_INSTANCES})

scheduler.add_job(update_statuses, 'interval', seconds=CRON_INTERVAL)
