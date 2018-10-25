import yaml
import pdb
import re
from collections import namedtuple
from website import Website
from courier import Courier
from concurrent import futures


class SocialWorker:
    CONFIG_FILE = '../config/sites.yml'
    WHITESPACE_REGEX = re.compile('\s+')
    PIPE = '|'

    EXECUTOR = futures.ThreadPoolExecutor(max_workers=100)

    def __init__(self):
        # Set self.courier and self.sites
        self.load_config()

    def load_config(self, data=None):
        if not data:
            with open(self.CONFIG_FILE, 'r') as f:
                text = f.read()
            data = yaml.load(text)

        self.courier = Courier(data['webhook_url'])
        sites = []
        for entry in data['sites']:
            pieces = re.split(self.WHITESPACE_REGEX, entry, maxsplit=1)
            uri = pieces[0]

            if len(pieces) > 1:
                expected_text = pieces[1]
            else:
                expected_text = ''

            site = Website(uri, expected_text)
            sites.append(site)
        self.sites = sites

    def check_sites(self):
        for site in self.sites:
            self.__check_one_site(site)

    def check_sites_async(self):
        self.EXECUTOR.map(self.__check_one_site, self.sites)

    def __check_one_site(self, site):
        site.evaluate()
        if site.message:
            self.courier.deliver(site.message)

