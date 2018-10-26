import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from collections import namedtuple
import pdb


# This is a separate class so it can be mocked to avoid network calls in unit tests
class Fetcher:
    def fetch(self, uri):
        try:
            response = requests.get(uri, timeout=10)
        except Exception as e:
            if type(e).__module__ == 'requests.exceptions':
                return (500, '')
            else:
                raise(e)
        return (response.status_code, response.text)

class Website:

    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    OBSERVATIONS = 'observations'
    FORWARD_SLASH_REGEX = re.compile('\/')
    DOWN = 'down'
    UP = 'up'

    PIPE = '|'
    SPACE = ' '

    Observation = namedtuple('Observation', ['timestamp', 'status'])

    def __init__(self, uri, expected_text):
        self.uri = uri
        self.expected_text = expected_text
        self.fetcher = Fetcher()

    @property
    def observation_file(self):
        filename = self.FORWARD_SLASH_REGEX.sub(self.PIPE, self.uri)
        return f'{self.OBSERVATIONS}/{filename}'

    def new_observation(self, status):
        now = datetime.now().strftime(self.TIMESTAMP_FORMAT)
        text = f'{now} {status}'
        with open(self.observation_file, 'w') as f:
            f.write(text)

    def last_observation(self):
        if not os.path.isfile(self.observation_file):
            return

        with open(self.observation_file, 'r') as f:
            text = f.read()
        timestamp, _, status = text.rpartition(self.SPACE)
        return self.Observation(timestamp, status)

    def clean(self):
        if os.path.isfile(self.observation_file):
            os.remove(self.observation_file)

    def current_status(self):
        status_code, response_body = self.fetcher.fetch(self.uri)

        if status_code != 200:
            return self.DOWN

        document = BeautifulSoup(response_body, 'lxml')
        text = document.get_text()
        if self.expected_text.lower() in text.lower():
            return self.UP
        else:
            return self.DOWN

    def evaluate(self):
        last_observation = self.last_observation()
        last_status    = last_observation and last_observation.status
        last_timestamp = last_observation and last_observation.timestamp

        status = self.current_status()
        print(f'\n{self.uri} is {status.upper()}')

        if status == last_status:
            print('no message required')
            self.message = None
        else:
            print('Writing a new observation')
            self.new_observation(status)
            print('Sending a message')
            self.message = f'{self.uri} is {status}.'


        if self.message and (last_status == self.DOWN):
            duration = datetime.now() - datetime.strptime(last_observation.timestamp, self.TIMESTAMP_FORMAT)

            self.message += f' Last {self.DOWN} duration: {duration.seconds} seconds.'





