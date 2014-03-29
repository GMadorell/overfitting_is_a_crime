#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gerard Madorell'
SITENAME = u'MLBlog'
SITEURL = ''

PATH = './content'
OUTPUT_PATH = './output'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'



# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

# Blogroll
LINKS = None

#Plugins
PLUGIN_PATH = './plugins'
PLUGINS = ['ipythonnb']
MARKUP = ('md', 'ipynb')  # Enable ipython articles.

# Themes
THEME = 'pelican-elegant-1.3'

# Social widget
SOCIAL = (('Twitter', 'http://www.twitter.com/gmadorell'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
