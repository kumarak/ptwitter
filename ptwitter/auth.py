try:
	import urllib.parse as urllib_parse
except ImportError:
	import urllib as urllib_parse

class Auth(object):
	def encode_params(self, base_url, method, params):
		raise NotImplementedError()

	def generate_headers(self):
		raise NotImplementedError()

# basic authentication using email/username and password
class UserPassAuth(Auth):
	def __init__(self, uname, password):
		self.username = uname
		self.password = password

	def encode_params(self, base_url, method, params):
		return urllib_parse.urlencode(params)

	def generate_headers(self):
		return {b"Authorization": b"Basic " + encodebytes(
			("%s:%s" %(self.username, self.password))
			.encode('utf8')).strip(b'\n')
			}

class NoAuth(Auth):
	def __init__(self):
		pass

	def encode_params(self, base_url, method, params):
		return urllib_parse.urlencode(params)

	def generate_headers(self):
		return {}
