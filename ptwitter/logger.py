
from __future__ import print_function

import sys
import os
from time import sleep

from api import Twitter, TwitterError
from auth import NoAuth
from util import printNicely

def log_debug(msg):
	print(msg, file=sys.stderr)

def get_tweets(twitter, screen_name, max_id=None):
	kwargs = dict(count=3200, screen_name=screen_name)
	pass
