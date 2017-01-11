import os
import time
import requests
import datetime
from pytz import timezone, utc


def openaq_query(country, date_from, date_to, parameters):
    '''2016-01-30T00:00:00+07:08'''
    query = {
        'country': country,
        'date_from': date_from.strftime('%Y-%m-%d'),
        'date_to': date_to.strftime('%Y-%m-%d'),
        'format': 'csv'
    }
    for i, param in enumerate(parameters):
        query['parameter[{}]'.format(i)] = param
    return query


def download_measurements(
            country='MN',
            date_from=datetime.datetime(2015, 3, 1, 0, 0, 0),
            date_to=datetime.datetime(2017, 1, 2, 0, 0, 0),
            day_intervals=10,
            openaq_data_directory='data',
            delay_between_download=5):
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
            print('Downloading data between {} and {}'.format(query['date_from'], query['date_to']))
            response = requests.get('https://api.openaq.org/v1/measurements', params=query)
            print('URL:', response.url)
            text = response.text
            if is_header_written is True:
                try:
                    text = text[text.index('\n')+1:]
                except ValueError as e:
                    print('New line did not found:', text)
            fd.write(text)
            is_header_written = True
            start_date = start_date+date_interval



if __name__ == '__main__':
    download_measurements()
