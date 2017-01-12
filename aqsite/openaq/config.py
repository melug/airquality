import os
import configparser

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE_NAME = os.path.join(SCRIPT_DIR, 'config.ini')


class Config(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.read(CONFIG_FILE_NAME)

    def save(self):
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            self.write(configfile)

