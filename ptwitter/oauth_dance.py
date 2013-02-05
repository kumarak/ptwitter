from __future__ import print_function

import webbrowser
import time

from api import Twitter
from oauth import OAuth, write_token_file

def oauth_dance(app_name, consumer_key, consumer_secret, token_filename=None):
	print("Hi there! We're gonna get you all the setup to use %s." %(app_name))
	twitter = Twitter(
		auth=OAuth('', '', consumer_key, consumer_secret),
		format='',
		api_version=None)
	oauth_token, oauth_token_secret = parse_oauth_tokens(twitter.oauth.request_token())
