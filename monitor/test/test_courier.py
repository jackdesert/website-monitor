from monitor.models.courier import Courier
import unittest
import pdb

class TestSocialWorker(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        cc = Courier('hi')
        self.assertEqual(cc.webhook_url, 'hi')

    # This test makes a network call to Slack
    def test_deliver(self):
        cc = Courier(Courier.SLACK_TEST_URI)
        cc.deliver('Unit testing Courier.deliver()')

    def test_deliver_when_uri_is_malformed(self):
        cc = Courier('h://slack')

        # Make this call just to make sure the exception is handled
        cc.deliver('Unit testing Courier.deliver()')


if __name__ == '__main__':
    unittest.main()
