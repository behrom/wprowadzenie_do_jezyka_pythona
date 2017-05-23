#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json

PYTHON_HISTORY = "http://python-history.blogspot.com/feeds/posts/default?alt=json"
PYTHON_NEWS = "http://pyfound.blogspot.com/feeds/posts/default?alt=json"
GOOGLE = "http://googlepolska.blogspot.com/feeds/posts/default?alt=json"

response = urllib2.urlopen(PYTHON_HISTORY)
data = json.load(response)

