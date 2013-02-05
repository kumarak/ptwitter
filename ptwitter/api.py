try:
	import urllib.request as urllib_request
	import urllib.error as urllib_error
except ImportError:
	import urllib2 as urllib_request
	import urllib2 as urllib_error

try:
	from cStringIO import StringIO
except ImportError:
	from io import BytesIO as StringIO

#from ptwitter.twitter_globals import POST_ACTIONS
from ptwitter.auth import NoAuth

class TwitterCall(object):
	pass

class Twitter(TwitterCall):
	pass

__all__ = ["Twitter", "TwitterError", "TwitterHTTPError", "TwitterResponse"]
