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
	pass
