
from __future__ import print_function

from time import time
from random import getrandbits

try:
	import urllib.parse as urllib_parse
	from urllib.parse import urlencode
	PY3 = True
except ImportError:
	import urllib2 as urllib_parse
	from urllib import urlencode
	PY3 = False

import hashlib
import hmac
import base64

from auth import Auth

def write_token_file(filename, oauth_token, oauth_token_secret):
	oauth_file = open(filename, 'w')
	print(oauth_token, file=oauth_file)
	print(oauth_token_secret, file=oauth_file)
	oauth_file.close()

def read_token_file(filename):
	f = open(filename)
	return f.readline().strip(), f.readline().strip()

class OAuth(Auth):
	def __init__(self, token, token_secret, consumer_key, consumer_secret):
		self.token = token
		self.token_secret = token_secret
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret

	def encode_params(self, base_url, method, params):
		params = params.copy()

		if self.token:
			params['oauth_token'] = self.token

		params['oauth_consumer_key'] = self.consumer_key
		params['oauth_signature_method'] = 'HMAC-SHA1'
		params['oauth_version'] = '1.0'
		params['oauth_timestamp'] = str(int(time()))
		params['oauth_nonce'] = str(getrandbits(64))

		enc_params = urlencode_noplus(sorted(params.items()))
		key = self.consumer_secret + "&" + urllib_parse.quote(self.token_secret, safe='~')
		
		message = '&'.join(urllib_parse.quote(i, safe='~') for i in [method.upper(), base_url, enc_params])

		signature = (base64.b64encode(hmac.new(
				key.encode('ascii'), message.encode('ascii'), hashlib.sha1)
				.digest()))
		return enc_params + "&" + "oauth_signature" + urllib_parse.quote(signature, safe='~')

	def generate_headers(self):
		return {}

def urlencode_noplus(query):
	if not PY3:
		new_query = []
		for k,v in query:
			if type(k) is unicode: k = k.encode('utf-8')
			if type(v) is unicode: v = v.encode('utf-8')
			new_query.append((k, v))
		query = new_query
		return urlencode(query).replace("+", "%20")
	return urlencode(query, safe='~').replace("+", "%20")
	pass

if __name__ == '__main__':
	write_token_file("token.txt", 'ABC', 'XYX')
