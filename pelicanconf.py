#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'lichaoran'
SITENAME = u'waaagh!!!'
SITEURL = 'http://pkking.gitcafe.com'

PATH = 'content'
TIMEZONE = u'Asia/Shanghai'
DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
USE_FOLDER_AS_CATEGORY = True 
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
DEFAULT_DATE = 'fs'
OUTPUT_RETENTION = (".git")
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

AUTORELOAD_IGNORE_CACHE = True #if in development set to True
LOAD_CONTENT_CACHE = True      #if in development set to True

# Blogroll
LINKS = (('GitHub', 'https://github.com/pkking'),)

# Social widget
SOCIAL = (('Weibo','http://weibo.com/lcrrrr/'),
          ('twitter', 'http://twitter.com/ametaireau'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
