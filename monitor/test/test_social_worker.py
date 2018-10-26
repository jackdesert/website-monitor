from monitor.models.social_worker import SocialWorker
from monitor.models.courier import Courier

import unittest
from unittest.mock import patch
import requests

class TestSocialWorker(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_config(self):
        soc = SocialWorker()
        soc.load_config()
        self.assertTrue(isinstance(soc.sites, list))
        self.assertTrue(soc.sites, 'Expected one or more sites to be present')

        self.assertTrue(isinstance(soc.courier, Courier))

    def test_yaml_parsing(self):
        data = {'webhook_url': '',
                'sites': ['https://example.com   everyone loves a great example',
                          'https://no-expected-text.com']
               }
        soc = SocialWorker()
        soc.load_config(data)
        site_0 = soc.sites[0]
        self.assertEqual(site_0.expected_text, 'everyone loves a great example')

        site_1 = soc.sites[1]
        self.assertEqual(site_1.expected_text, '')

    @patch('monitor.models.courier.Courier')
    def test_check_sites(self, MockCourier):
        data = {'webhook_url': Courier.SLACK_TEST_URI,
                'sites': ['https://example.com   example']
               }
        soc = SocialWorker()
        soc.load_config(data)

        # Override the default courier with our mock
        soc.courier = MockCourier()


        print('Calling network from test_social_worker.py')
        soc.check_sites()

    @patch('monitor.models.courier.Courier')
    def test_check_sites_async(self, MockCourier):
        data = {'webhook_url': Courier.SLACK_TEST_URI,
                'sites': ['https://example.com   example']
               }
        soc = SocialWorker()
        soc.load_config(data)

        # Override the default courier with our mock
        soc.courier = MockCourier()


        print('Calling network from test_social_worker.py')
        soc.check_sites_async()


if __name__ == '__main__':
    unittest.main()
