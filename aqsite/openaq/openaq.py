import os
import time
import requests
import datetime
from pytz import timezone, utc
from .config import Config

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def openaq_query(country, date_from, date_to, parameters):
    '''2016-01-30T00:00:00+07:08'''
    query = {
        'country': country,
        'date_from': date_from.strftime(DATE_FORMAT),
        'date_to': date_to.strftime(DATE_FORMAT),
        'format': 'csv'
    }
    for i, param in enumerate(parameters):
        query['parameter[{}]'.format(i)] = param
    return query


def download_measurements(
            country='MN',
            date_from=None,
            date_to=None,
            day_intervals=10,
            openaq_data_directory='data',
            delay_between_download=5,
            logger=None):
    '''
    Download measurements between date_from to date_to
    '''
    if not os.path.exists(openaq_data_directory):
        os.mkdir(openaq_data_directory)
    start_date = date_from
    date_interval = datetime.timedelta(day_intervals)
    output_file_name = os.path.join(openaq_data_directory, 'openaq.csv')
    is_header_written = False
    with open(output_file_name, 'w') as fd:
        while start_date <= date_to:
            if start_date+date_interval<date_to:
                end_date = start_date+date_interval
            else:
                end_date = date_to
            query = openaq_query(country, start_date, end_date, ['so2', 'no2', 'pm10', 'pm25', 'co'])
            # firewall?
            time.sleep(delay_between_download)
            logger.info('Downloading data between {} and {}'.format(query['date_from'], query['date_to']))
            response = requests.get('https://api.openaq.org/v1/measurements', params=query)
            text = response.text
            if is_header_written is True:
                try:
                    text = text[text.index('\n')+1:]
                except ValueError as e:
                    logger.warning('Data is empty')
            fd.write(text)
            is_header_written = True
            start_date = start_date+date_interval


def update_measurements(logger=None):
    config = Config()
    config_header = __file__
    if config_header not in config:
        config[config_header] = {}
    if logger is None:
        import logging
        logger = logging.getLogger(__file__)
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
    now = datetime.datetime.now()
    start = datetime.datetime.strptime(config[config_header]['START DATE'], DATE_FORMAT)
    download_measurements(date_from=start, date_to=now, logger=logger)
    config[config_header]['START DATE'] = now.strftime(DATE_FORMAT)
    config.save()


if __name__ == '__main__':
    update_measurements()
