# -*- coding: utf-8 -*-
"""
Created August-September 2016
@author: github.com/jeffgerhard or @jeffgerhard

spect is a static site generator customized to my own needs, in active development.

development phase 1: just generate some html files in a directory structure
of index.html files

phase 2: generate tags pages and similar (like related content);
    generate rss feed and sitemap; allow local persistent settings for
    multiple instances

phase 3: configure an auto-upload to server

phase 4: a separate script to easily generate the .md files including
    dates, sections, etc.

phase 5: think about .htaccess and redirects

"""

import markdown as m
import os


def get_immediate_subdirectories(a_dir):
# stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python#800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_mdfiles(x):
    a_dir = os.path.join(mddir, x)
    return [name for name in os.listdir(a_dir)
            if name[-2:] == 'md']


def buildHTML(f, s):
    h = os.path.join(mddir, s, f)
    htm = ''
    with open(h, mode='r', encoding='utf-8') as z:
        t = z.read()
    text = md.convert(t)
    k = md.Meta
    if s == 'blog':
        k['section'] = [blogtitle]
    else:
        k['section'] = [s]
    # print(k)
    htm += head(**k)
    htm += '<body>\n'
    htm += header(**k)
    htm += sidebar(**k)
    htm += '\t<main>\n'
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
        htm += '\t' + a
    htm += '\n\n\t</main>\n'
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
        htm += ' : ' + kwargs['section'][0]
    else:
        htm += '&mdash; jeffgerhard.com'
    htm += '</title>\n'
    stz = ['styles']
    if 'styles' in kwargs:
        for s in kwargs['styles']:
            stz.append(s)
    for st in stz:
        htm += '\t<link rel="stylesheet" href="../styles/'
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

for s in secs:
    files = get_mdfiles(s)
    for f in files:
        x = buildHTML(f, s)
        print(x)
