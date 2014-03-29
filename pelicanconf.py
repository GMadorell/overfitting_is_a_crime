#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gerard Madorell'
SITENAME = u'MLBlog'
SITEURL = ''

PATH = './content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

#Plugins
PLUGIN_PATH = './plugins'
PLUGINS = ['ipythonnb']
MARKUP = ('md', 'ipynb')  # Enable ipython articles.

# Social widget
SOCIAL = (('Twitter', 'http://www.twitter.com/gmadorell'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
