from celery.utils.log import get_task_logger
from celery.schedules import crontab

from aqsite.celery import app
from openaq import openaq

logger = get_task_logger(__name__)

@app.task()
def update_openaq_data():
    openaq.update_measurements(logger=logger)

app.conf.beat_schedule = {
    'update-openaq-date-every-15-minutes': {
        'task': 'aqapp.tasks.update_openaq_data',
        'schedule': crontab(hour='*', minute='*')
    },
}
