from __future__ import print_function

import sys
import time
import os.path

try:
	from ConfigParser import SafeConfigParser
except ImportError:
	from configparser import ConfigParser as SafeConfigParser

import ansi	

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
	print(config_options)
	
	options = dict(OPTIONS)
	for d in config_options, arg_options:
		for k, v in list(d.items()):
			if v: options[k] = v

	print(options)
	
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

	print("twitter called inside main")
