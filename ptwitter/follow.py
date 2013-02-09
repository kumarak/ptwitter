
from __future__ import print_function

import os, sys, time, calendar
from getopt import gnu_getopt as getopt, GetoptError

try:
	import urllib.request as urllib2
	import http.client as httplib
except ImportError:
	import urllib2
	import httplib

CONSUMER_KEY='USRZQfvFFjB6UvZIN2Edww'
CONSUMER_SECRET='AwGAaSzZa5r0TDL8RKCDtffnI9H9mooZUdOa95nw8'

from api import Twitter, TwitterError
from oauth import OAuth, read_token_file
from oauth_dance import oauth_dance
from auth import NoAuth
from util import Fail, err 

def parse_args(args, options):
	pass

def lookup_portion(twitter, user_ids):
	pass

def lookup(twitter, user_ids):
	pass

def follow_portion(twitter, screen_name, cursor=-1, followers=True):
	pass

def follow(twitter, screen_name, followers=True):
	pass

def rate_limit_status(twitter):
	pass

def main(args=sys.argv[1:]):
	pass
