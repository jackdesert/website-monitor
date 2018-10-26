from monitor.models.website import Website
from monitor.models.website import Fetcher

import unittest
from unittest.mock import patch
from collections import namedtuple
import pdb

class TestWebsite(unittest.TestCase):

    def setUp(self):
        pass

    def test_initialize(self):
        uri = 'https://example.com'
        expected_text = 'example'

        site = Website(uri, expected_text)
        self.assertEqual(uri, site.uri)
        self.assertEqual(expected_text, site.expected_text)

    def test_observation_file(self):
        site = Website('https://example.com', 'example')
        self.assertEqual(site.observation_file, 'observations/https:||example.com')

    def test_last_observation_happy_path(self):
        site = Website('https://example.com', 'example')
        site.new_observation('up')

        last = site.last_observation()
        self.assertEqual(last.status, 'up')

    def test_last_observation_when_no_observation_exists(self):
        site = Website('https://example.com', 'example')

        site.clean()
        observation = site.last_observation()

        self.assertEqual(observation, None)

    def test_current_status(self):
        site = Website('https://example.com', 'example')
        status = site.current_status()

    def test_current_status_with_malformed_uri(self):
        site = Website('h://malformed.com', 'example')
        status = site.current_status()
        self.assertEqual(status, 'down')

    @patch('monitor.models.website.Fetcher')
    def test_message_status_same_as_last_time(self, MockFetcher):
        site = Website('https://example.com', 'example')
        site.new_observation('up')

        site.fetcher = MockFetcher()
        site.fetcher.fetch.return_value = (200, 'This is an example')

        # This line would make a network call, but uses our mock instead
        site.evaluate()
        self.assertFalse(site.message, 'No Message expected')

    @patch('monitor.models.website.Fetcher')
    def test_message_status_was_up_now_down(self, MockFetcher):
        site = Website('https://example.com', 'this phrase not found')

        site.fetcher = MockFetcher()
        site.fetcher.fetch.return_value = (502, 'Nginx Error')

        site.new_observation('up')
        site.evaluate()
        self.assertEqual(site.message, 'https://example.com is down.')

    @patch('monitor.models.website.Fetcher')
    def test_message_status_was_down_now_up(self, MockFetcher):
        site = Website('https://example.com', 'example')

        site.fetcher = MockFetcher()
        site.fetcher.fetch.return_value = (200, 'An example')

        site.new_observation('down')
        site.evaluate()
        variations = ['https://example.com is up. Last down duration: 0 seconds.',
                      'https://example.com is up. Last down duration: 1 seconds.']
        self.assertTrue(site.message in variations, 'Expected duration is either 0 or 1 second')

    @patch('monitor.models.website.Fetcher')
    def test_message_when_no_observation_exists(self, MockFetcher):
        site = Website('https://example.com', 'example')

        site.fetcher = MockFetcher()
        site.fetcher.fetch.return_value = (200, 'An example')

        site.clean()
        site.evaluate()
        self.assertEqual(site.message, 'https://example.com is up.')




if __name__ == '__main__':
    unittest.main()
