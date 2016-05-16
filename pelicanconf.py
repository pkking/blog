#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'lichaoran'
SITENAME = u'WAAAGH!'
SITEURL = 'http://pkking.gitcafe.io'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
PATH = 'content'
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'cn'
OUTPUT_PATH = 'pkking/'
ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'
#enable search
USE_FOLDER_AS_CATEGORY = True 
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
DEFAULT_DATE = 'fs'
PAGE_PATHS = ['pages']
DISPLAY_PAGES_ON_MENU = True
DISPLAY_SEARCH_FORM = True
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme
THEME = 'waaagh'

# DUOSHUO comment plugin
DUOSHUO_SITENAME = u'waaagh'

# Cache
AUTORELOAD_IGNORE_CACHE = True #if in development set to True
LOAD_CONTENT_CACHE =  False    #if in development set to True

#  Links
GITHUB_URL = u'https://github.com/pkking'
LINKS = (('GitHub', 'https://github.com/pkking'),)

# Social widget
TWITTER_URL = u'https://twitter.com/li_chaoran'
WEIBO_URL = u'http://weibo.com/lcrrrr'
SOCIAL = (('weibo','http://weibo.com/lcrrrr/'),
        ('twitter', 'https://twitter.com/li_chaoran'),)

DEFAULT_PAGINATION = 5

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 200

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
