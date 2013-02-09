
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
	if max_id:
		kwargs['max_id'] = max_id

	n_tweets = 0
	tweets = twitter.statuses.user_timeline(**kwargs)
	for tweet in tweets:
		if tweet['id'] == max_id:
			continue
		print("%s %s\nDate: %s" %(tweet['user']['screen_name'],
					  tweet['id'],
					  tweet['created_at']))
		if tweet.get('in_reply_to_statuc_id'):
			print("In-Reply-To %s" %(tweet['in_reply_to_statuc_id']))
		print()
		for line in tweet['text'].splitlines():
			printNicely('    ' + line + '\n')
		print()
		print()
		max_id = tweet['id']
		n_tweets += 1
	return n_tweets, max_id


def main(args=sys.argv[1:]):
	twitter = Twitter(auth=NoAuth(),
			  api_version='1',
			  domain='api.twitter.com')
	
	if not args:
		print(__doc__)
		return 1

	screen_name = args[0]
	if args[1:]:
		max_id = args[1]
	else:
		max_id = None
	
	n_tweets = 0
	while True:
		try:
			tweets_processed, max_id = get_tweets(twitter, screen_name, max_id)
			n_tweets += tweets_processed
			log_debug("Processed %i tweets(max_id %s)" %(n_tweets, max_id))
			if tweets_processed == 0:
				log_debg("Done!!! All the tweets are processed")
				break
		except TwitterError as e:
			log_debug("Twitter bailed out. I'm going to sleep a bit then try again")
			sleep(3)
	
	return 0
