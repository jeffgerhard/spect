# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 22:09:15 2017

@author: J
"""

import requests

r = requests.get('http://www.bing.com/webmaster/ping.aspx?siteMap=http://jeffgerhard.com/sitemap.xml')
print('for bing, response', r)
r = requests.get('http://www.google.com/webmasters/sitemaps/ping?sitemap=http://jeffgerhard.com/sitemap.xml')
print('for google, response', r)
