# -*- coding: utf-8 -*-
"""
Created August-September 2016
@author: github.com/jeffgerhard or @jeffgerhard

spect is a static site generator customized to my own needs, in active development.

development phase 1: just generate some html files in a directory structure
of index.html files 

NEED TO DELETE OBSOLETE LOCAL FILES!
And maybe backup last saved files before screwing around

phase 2: generate tags pages and similar (like related content);
    generate rss feed and sitemap; allow local persistent settings for
    multiple instances. note that i need to do the tags, etc first!

phase 3: configure an auto-upload to server [coming along nicely]

phase 4: a separate script to easily generate the .md files including
    dates, sections, etc. NB this part can include publication date issues

phase 5: think about .htaccess and redirects; also 404s and all that

uses markdown and python-slugify https://github.com/un33k/python-slugify

"""

import markdown as m
import os
from slugify import slugify
from dateutil.parser import parse
from spect_config import j


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

def cleanDate(**k):
    if 'date' in k:
        d = parse(k['date'][0])
        return '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())

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
        k['slug'][0] += slugify(
            k['title'][0], max_length=28,
            stopwords=['the', 'a', 'an']
            )
    else:
        k['slug'][0] += 'untitled'
        k['title'][0] = 'untitled'  # later, grab file name as title
    return text, k


def buildHTML(text, **k):
    htm = head(**k)
    htm += '<body>'
    htm += header(**k)
    htm += '''
    <main class="container"> <!-- would be good to also split out this <main>
                    stuff so could have like blog() or other variations -->
        <article>
            <header>
                <h1>{}</h1>
'''.format(k['title'][0])
    if 'summary' in k:
        htm += '\t\t\t<p class="summary">' + str(k['summary'][0]) + '</p>\n'
    if 'date' in k:
        htm += cleanDate(**k)
    htm += '\t\t</header>\n'
    htm += '\t\t<div class="eight columns">\n'
    htm += '\n\n'
    gist = md.convert(text)
    g = gist.splitlines(keepends=True)
    for a in g:
        if not a == '\n':
            htm += '\t' + a
    htm += '\t\t</div>\n'
    htm += '\n\n\n\t\t<footer class="three columns">\n'
    htm += '\t\t\t<p>This could be where i add date posted and tags, prev/next links, etc</p>\n'
    htm += '\t\t</footer>\n'
    htm += '\t\t</article>\n'
    htm += '\t</main>\n'
    htm += sidebar(**k)
    htm += footer(**k)
    htm += '</body>\n'
    htm += '</html>'
    return htm


def head(**kwargs):
    htm = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>'''
    if 'title' in kwargs:
        htm += str(kwargs['title'][0])
    if 'section' in kwargs:
        htm += ' :: ' + kwargs['section'][0]
    else:
        htm += '&mdash; jeffgerhard.com'
    htm += '</title>'
    htm += '''
    <link rel="stylesheet" type="text/css"
    href="//fonts.googleapis.com/css?family=Alegreya+Sans|Raleway">'''
    stz = ['normalize', 'skeleton']
    if 'styles' in kwargs:
        for s in kwargs['styles']:
            stz.append(s)
    for st in stz:
        htm += '''
    <link rel="stylesheet" href="../../styles/{}.css">'''.format(st)
    htm += '''
    <link rel="icon" type="image/png" href="../../favicon.png">
    <meta name="generator" content="https://github.com/jeffgerhard/spect">
</head>
'''
    return htm


def header(**kwargs):
    htm = '''
    <header id="topbar">
        <p>Name of website I guess! A 'home' link can be at the left
        and be persistent/sticky, then most of the rest can scroll up
        and offscreen</p>
        <div class="container">
            <nav>
                <a href="//">PROJECTS</a>
            </nav>
            <nav>
                <a href="//">BLOG</a>
            </nav>
            <nav>
                <a href="//">MUSIC</a>
            </nav>
        </div>
    </header>
'''
    return htm


def footer(**kwargs):
    htm = '''
    <footer>
        <p>Some misc about links can go down here i guess.</p>
    </footer>
'''
    return htm


def sidebar(**kwargs):
    htm = '''
    <aside>
        [here i can put my sidebar]
    </aside>
'''
    return htm

md = m.Markdown(extensions=['meta', 'smarty'])
# think about how to make the local md files add to the extension list
localdir = j['localdir']
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
blogtitle = j['blogtitle']
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
