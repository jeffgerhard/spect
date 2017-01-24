# -*- coding: utf-8 -*-
"""
sitemap generator version 0.0.1
when i change around the upload functions to be more of a 'publish' feature
i will go ahead and implement pinging google, bing, and others

"""

#from spect_config import j, admin  

def buildurls(k, priority='0.5', changefreq='monthly'):
    ''' where k is the dictionary of site content. 
    note that i should break up html building the same way sometime
    when i clean up the overall code
    '''
    sitemap = ''
    for url in k:
        if 'date_modified' in url:
            lastmod = url['date_modified']
        else:
            lastmod = url['yyyy-mm-dd']
        sitemap += '''
   <url>
      <loc>{}</loc>
      <lastmod>{}</lastmod>
      <changefreq>{}</changefreq>
      <priority>{}</priority>
   </url>'''.format(url['canonical'], lastmod, changefreq, priority)
    return sitemap


def addpage(loc, lastmod, priority='0.5', changefreq='monthly'):
    sitemap = '''
   <url>
      <loc>{}</loc>
      <lastmod>{}</lastmod>
      <changefreq>{}</changefreq>
      <priority>{}</priority>
   </url>'''.format(loc, lastmod, changefreq, priority)
    return sitemap


def finish(k):
    ''' where k is the compiled list of sitemap url chunks, i.e., from different
    sections of my website '''
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    for line in k:
        sitemap += line
    sitemap += '''
</urlset>'''
    return sitemap