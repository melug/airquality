from aqsite import celery_app

@celery_app.task()
def download_data():
    print('Downloading new data')

