#! /usr/bin/env python3

import pdb
import time
from social_worker import SocialWorker

while True:
    # Reinitialize the social worker each loop
    # to pick up any changes to config file
    soc = SocialWorker()

    # Check sites asynchronously
    soc.check_sites_async()
    time.sleep(15)
