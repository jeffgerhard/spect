# -*- coding: utf-8 -*-
"""
Created August-September 2016
@author: github.com/jeffgerhard or @jeffgerhard

spect is a static site generator customized to my own needs, in active development.

development phase 1: just generate some html files in a directory structure
of index.html files // mostly done but i want to add date functionality

phase 2: generate tags pages and similar (like related content);
    generate rss feed and sitemap; allow local persistent settings for
    multiple instances

phase 3: configure an auto-upload to server

phase 4: a separate script to easily generate the .md files including
    dates, sections, etc. NB this part can include publication date issues

phase 5: think about .htaccess and redirects

uses markdown and python-slugify https://github.com/un33k/python-slugify

"""

import markdown as m
import os
from slugify import slugify
from dateutil.parser import parse


def get_immediate_subdirectories(a_dir):
# stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python#800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def yyyy_mm_dd(**k):
    if 'date' in k:
        d = parse(k['date'][0])
        return str(d.date())
    else:
        return ''


def get_mdfiles(x):
    a_dir = os.path.join(mddir, x)
    return [name for name in os.listdir(a_dir)
            if name[-2:] == 'md']


def keywords(f, s):
    h = os.path.join(mddir, s, f)
    with open(h, mode='r', encoding='utf-8') as z:
        t = z.read()
    text = md.convert(t)
    k = md.Meta
    if s == 'blog':
        k['section'] = [blogtitle]
    else:
        k['section'] = [s]
    k['slug'] = [yyyy_mm_dd(**k) + '_']
    if 'title' in k:
        k['slug'][0] += slugify(k['title'][0], max_length=20,
              word_boundary=True, stopwords=['the', 'a', 'an'])
    else:
        k['slug'][0] += 'untitled'
    return text, k


def buildHTML(text, **k):
    htm = head(**k)
    htm += '<body>\n'
    htm += header(**k)
    htm += sidebar(**k)
    htm += '\t<main>\n'  #  would be good to also split out this main stuff
    #                       so could have like blog() or other variations
    htm += '\t\t<header>\n'
    htm += '\t\t\t<h1>'
    if 'title' in k:
        htm += str(k['title'][0])
    htm += '</h1>\n'
    if 'summary' in k:
        htm += '\t\t\t<p class ="summary">' + str(k['summary'][0]) + '</p>\n'
    htm += '\t\t</header>\n'
    htm += '\n\n'
    gist = md.convert(text)
    g = gist.splitlines(keepends=True)
    for a in g:
        if not a == '\n':
            htm += '\t' + a
    htm += '\n\n\n\t\t<footer>\n'
    htm += '\t\t\t<p>This could be where i add date posted and tags, prev/next links, etc</p>\n'
    htm += '\t\t</footer>\n'
    htm += '\t</main>\n'
    htm += footer(**k)
    htm += '</body>\n'
    htm += '</html>'
    return htm


def head(**kwargs):
    htm = '<!DOCTYPE html>\n'
    htm += '<html>\n'
    htm += '<head>\n'
    htm += '\t<meta charset="utf-8">\n'
    htm += '\t<meta http-equiv="x-ua-compatible" content="ie=edge">\n'
    htm += '\t<meta name="viewport" content="width=device-width,'
    htm += 'initial-scale=1">\n'
    htm += '\t<title>'
    if 'title' in kwargs:
        htm += str(kwargs['title'][0])
    if 'section' in kwargs:
        htm += ' :: ' + kwargs['section'][0]
    else:
        htm += '&mdash; jeffgerhard.com'
    htm += '</title>\n'
    stz = ['styles']
    if 'styles' in kwargs:
        for s in kwargs['styles']:
            stz.append(s)
    for st in stz:
        htm += '\t<link rel="stylesheet" href="../../styles/'
        htm += st
        htm += '.css">\n'
    htm += '\t<meta name="generator" content="https://github.com/jeffgerhard/spect">\n'
    htm += '</head>\n'
    return htm


def header(**kwargs):
    htm = '\t<header>\n'
    htm += '\t\t[ok so think about including a header nav bar that scrolls mostly offscreen like i did for that finding aid project?]\n'
    htm += '\t\t[also can customize per section?]\n'
    htm += '\t</header>\n'
    return htm


def footer(**kwargs):
    htm = '\t<footer>\n'
    htm += '\t\t<p>Some misc about links can go down here i guess.</p>\n'
    htm += '\t</footer>\n'
    return htm


def sidebar(**kwargs):
    htm = '\t<aside>\n'
    htm += '\t\t[here i can put my sidebar]\n'
    htm += '\t</aside>\n'
    return htm


md = m.Markdown(extensions=['meta', 'smarty'])
# think about how to make the local md files add to the extension list

# localdir = r'C:\Users\gerhardj\Dropbox\__websites\python\testsite'
localdir = r'C:\Users\J\Dropbox\__websites\python\testsite'
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
blogtitle = 'introspect'
secs = get_immediate_subdirectories(mddir)
internalsitemap = os.path.join(localdir, 'site.txt')
with open(internalsitemap, 'w') as fh:
    fh.write('')  # will this delete contents?
for s in secs:
    files = get_mdfiles(s)
    for f in files:
        text, k = keywords(f, s)
        htm = buildHTML(text, **k)
        pagedir = os.path.join(wdir, s, k['slug'][0])
        if not os.path.exists(pagedir):
            os.makedirs(pagedir)
        htmlfile = os.path.join(pagedir, 'index.html')
        with open(htmlfile, 'w') as fh:
            fh.write(htm)
        with open(internalsitemap, 'a') as fh:
            # fh.write('../../' + s + '/' + k['slug'][0] + '/\n')
            fh.write(yyyy_mm_dd(**k) + ',')
            fh.write(k['title'][0] + ',')
            fh.write(s + '/' + k['slug'][0] + '\n')
