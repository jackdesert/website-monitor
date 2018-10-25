import requests
import pdb
import json

class Courier:
    SLACK_TEST_URI = 'https://hooks.slack.com/services/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'

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def deliver(self, msg):
        payload = dict(text=msg,
                       icon_emoji='ghost')

        try:
            response = requests.post(self.webhook_url, data=json.dumps(payload), timeout=5)
        except Exception as e:
            if type(e).__module__ == 'requests.exceptions':
                exception_class = type(e).__name__
                error_message = f'{exception_class}: {str(e)}'
                self._print_error(error_message)
                return
            else:
                raise(e)

        if response.status_code != 200:
            self._print_error(f'{msg} (status_code was {response.status_code}')

    def _print_error(self, error_message):
        print(f'ERROR Posting to Slack: "{error_message}"')

