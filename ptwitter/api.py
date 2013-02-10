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

DEFAULT = '1'

class TwitterError(object):
	pass

class TwitterCall(object):
	def __init__(
		self, auth, format, domain, callable_cls, uri="",
		uriparts=None, secure=True):
		self.auth = auth
		self.format = format
		self.domain = domain
		self.callable_cls = callable_cls
		self.uriparts = uriparts
		self.secure = secure

	def __getattr__(self, k):
		print("inside __getattr__")
		try:
			return object.__getattr__(self, k)
		except AttributeError:
			def extend_call(arg):
				return self.callable_cls(auth=self.auth,
						format=self.format,
						domain=self.domain,
						callable_cls=self.callable_cls,
						uriparts=self.uriparts + (arg,),
						secure=self.secure)

			if k == "_":
				return extend_call
			else:
				return extend_call(k)

	def __call__(self, **kwargs):
		print("inside call")
		uriparts = []
		for uriparts in self.uriparts:
			uriparts.append(str(kwargs.pop(uripart, uripart)))
		uri = '/'.join(uriparts)

		method = kwargs.pop('_method', None)
		if not method:
			method = "GET"
			for action in POST_ACTIONS:
				if re.search("%s(/\d+)?$" % action, uri):
					method = "POST"
					break

		id = kwargs.pop('id', None)
		if id:
			uri += "/%s" %(id)

		_id = kwargs.pop('_id', None)
		if _id:
			kwargs['id'] = _id

		_timeout = kwargs.pop('_timeout', None)

		secure_str = ''

class Twitter(TwitterCall):
	def __init__(self, format="json",domain="api.twitter.com", secure=True, auth=None, api_version=DEFAULT):
		if not auth:
			auth = NoAuth()

	# there is an issue with the format
		if(format not in ("json", "xml", "")):
			raise ValueError("Unknown data format '%s'" %(format))

		if api_version is DEFAULT:
			if domain == 'api.twitter.com':
				api_version = '1.1'
			else:
				api_version = None
		uriparts = ()
		if api_version:
			uriparts += (str(api_version),)

		TwitterCall.__init__(self, auth=auth, format=format, domain=domain, callable_cls=TwitterCall, secure=secure, uriparts=uriparts)

__all__ = ["Twitter", "TwitterError", "TwitterHTTPError", "TwitterResponse"]
