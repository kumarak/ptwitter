from __future__ import print_function

CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'

import sys
import time
import os.path

try:
	from ConfigParser import SafeConfigParser
except ImportError:
	from configparser import ConfigParser as SafeConfigParser


import ansi
from api import Twitter, TwitterError
from oauth import OAuth, write_token_file, read_token_file	

OPTIONS = {
	'action': 'friends',
	'refresh': False,
	'refresh_rate': 600,
	'format': 'default',
	'prompt': '[cyan]twitter[R]>',
	'config_filename': os.environ.get('HOME', os.environ.get('USERPROFILE', '')) + os.sep + '.twitter',
	'oauth_filename': os.environ.get('HOME', os.environ.get('USERPROFILE', '')) + os.sep + '.twitter_oauth',
	'length': 20,
	'timestamp': False,
	'datestamp': False,
	'extra_args': [],
	'secure': True,
	'invert_split': False,
	'force-ansi': False,
}




def parse_args(args, options):
	pass

class Action(object):
	def ask(self, subject='perform this action', careful=False):
		pass
	def __call__(self, twitter, options):
		action = actions.get(options['action'], NoSuchAction)()
		try:
			doAction = lambda : action(twitter, options)
			if(options['refresh'] and isinstance(action, StatusAction)):
				while True:
					doAction()
					sys.stdout.flush()
					time.sleep(options['refresh_rate'])
			else:
				doAction()
			print(doAction)
		except KeyboardInterrupt:
			print('\n[Keyboard Interrupt]', file=sys.stderr)
			pass		
		print("inside action call")
		pass


class NoSuchActionError(Exception):
    pass

class NoSuchAction(Action):
    def __call__(self, twitter, options):
        raise NoSuchActionError("No such action: %s" % (options['action']))


class StatusAction(Action):
	def __call__(self, twitter, options):
		pass

class AdminAction(Action):
	def __call__(self, twitter, options):
		pass

class ListsAction(StatusAction):
	def getStatuses(self, twitter, options):
		if not options['extra_args']:
			raise TwitterError("Please Provide a user to query for lists")

class FriendsAction(StatusAction):
	def getStatuses(self, twitter, options):
		return reversed(twitter.statuses.friends_timeline(count=options["length"]))

class FollowAction(AdminAction):
	def getUser(self, twitter, user):
		return twitter.friendships.create(id=user)

class DoNothingAction(Action):
	def __call__(self, twitter, options):
		print("inside DoNothingAction")
		pass
actions = {
	'authorize' : DoNothingAction,
	'follow'    : FollowAction,
	'friends'   : FriendsAction,
	'list'      : ListsAction,
}

def loadConfig(filename):
	options = dict(OPTIONS)
	if os.path.exists(filename):
		print("option file exist")
		cp = SafeConfigParser()
		cp.read([filename])
		for option in ('format', 'prompt'):	
			if cp.has_option('twitter', option):
				options[option] = cp.get("twitter", option)
		
		for option in ('invert_split'):
			if cp.has_option('twitter', option):
				options[option] = cp.getboolean('twitter', option)
	return options

def main(args=sys.argv[1:]):
	arg_options = {}
	try:
		parse_args(args, arg_options)
	except GetoptError as e:
		print("Can't parse argument")
		print(file=sys.stderr)
		raise SystemExit(1)
	
	#config_path = OPTIONS.get('config_filename')
	config_path = os.path.expanduser(arg_options.get('config_filename') or
			OPTIONS.get('config_filename'))

	# check why config path is None
	print(config_path)
	config_options = loadConfig(config_path)
	#print(config_options)
	
	options = dict(OPTIONS)
	for d in config_options, arg_options:
		for k, v in list(d.items()):
			if v: options[k] = v

	#print(options)
	
	if options['refresh'] and options['action'] not in ('friends', 'public', 'replies'):
		print("You can only refresh the friends, public, or replies action.", file=sys.stderr)
		print("Use 'twitter -h' for help", file=sys.stderr)
		return 1
	
	oauth_filename = os.path.expanduser(options['oauth_filename'])

	if (options['action'] == 'authorize'
		or not os.path.exists(oauth_filename)):
		oauth_dance("the Command-Line-Tool", CONSUMER_KEY,
			CONSUMER_SECRET, options['oauth_filename'])

	global ansiFormatter
	ansiFormatter = ansi.AnsiCmd(options['force-ansi'])
	
	oauth_token, oauth_token_secret = read_token_file(oauth_filename)

	twitter = Twitter(
			auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET), secure=options['secure'], api_version='1', domain='api.twitter.com')

	try:
		Action()(twitter, options)
#	except NoSuchActionError as e:
#		print(e, file=sys.stderr)
#		raise SystemExit(1)
	except TwitterError as e:
		print(str(e), file=sys.stderr)
		print("Use 'twitter -h' for help", file=sys.stderr)
		raise SystemExit(1)

	print("twitter called inside main")
