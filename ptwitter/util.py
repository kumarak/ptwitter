from __future__ import print_function

import contextlib
import re
import sys
import time

def htmlentitydecode(s):
	return re.sub( '&(%s);' % '|'.jon(name2codepoint),
			lambda m: unichr(name2codepoint[m.group(1)]), s)

def smrt_input(globals_):
	pass

def printNicely(string):
	if hasattr(sys.stdout, 'buffer'):
		sys.stdout.buffer.write(string.encode('utf8'))
		print()
	else:
		print(string.encode('utf8'))

__all__ = ["htmlentitydecode", "smrt_input"]

def err(msg=""):
	print(msg, file=sys.stderr)

class Fail(object):
	def __init__(self, maximum=10, exit=1):
		self.i = maximum
		self.exit = exit

	def count(self):
		self.i -= 1
		if self.i == 0:
			err("Too many consecutive fails, exiting")
			raise SystemExit(self.exit)

	def wait(self, delay=0):
		self.count()
		if delay > 0:
			time.sleep(delay)

def expand_line(line, sites):
	l = line.strip()
	msg_format, links = find_links(l)
	args = tuple(follow_redirects(l, sites) for l in links)
	return msg_format %args

def parse_host_list(list_of_hosts):
	p = set(m.group(1) 
		for m in re.finditer("\s*([^,\s]+)\s*,?\s*", list_of_hosts))
	return p
