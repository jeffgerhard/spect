# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:15:38 2016

@author: gerhardj
"""

import markdown
import os


def get_immediate_subdirectories(a_dir):
# stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python#800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_jfiles(x):
    a_dir = os.path.join(mddir, x)
    return [name for name in os.listdir(a_dir)
            if name[-1:] == 'j']


def parseFile(lines):
    kwargs = {}
    text = []
    for l in lines:
        if l[0:2] == '$$':
            y, z = l.split(":")
            v = y[2:]
            kwargs[v] = z
        else:
            text.append(l)
    md = '\n'.join(text)
    return kwargs, md


def buildHTML(f, s):
    h = os.path.join(mddir, s, f)
    htm = ''
    with open(h, mode='r', encoding='utf-8') as z:
        text = z.read()
        lines = text.splitlines()
    k, text = parseFile(lines)
    if s == 'blog':
        k['section'] = blogtitle
    # print(k)
    # print(markdown.markdown(text, extensions=['smarty']))
    htm += header(**k)
    htm += '<body>\n'
    htm += markdown.markdown(text, extensions=['smarty'])
    htm += '</body></html>
    return htm


def header(**kwargs):
    htm = '<!DOCTYPE html>\n'
    htm += '<html>\n'
    htm += '<head>\n'
    htm += '\t<meta charset="utf-8">\n'
    htm += '\t<meta http-equiv="x-ua-compatible" content="ie=edge">\n'
    htm += '\t<meta name="viewport" content="width=device-width,'
    htm += 'initial-scale=1">\n'
    htm += '\t<title>'
    if kwargs['title']:
        htm += kwargs['title'] + ' : '
    if kwargs['section']:
        htm += kwargs[section']
    else:
        htm += 'jeffgerhard.com'
    htm += '</title>\n
    htm += '\t<link rel="stylesheet" href="..\styles\styles.css">\n'
    htm += '\t<meta name="generator" content="spect https://github.com/jeffgerhard/spect">\n'
    htm += '</head>\n'
    return htm

localdir = r'C:\Users\gerhardj\Dropbox\__websites\python\testsite'
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
blogtitle = 'introspect'
secs = get_immediate_subdirectories(mddir)

for s in secs:
    files = get_jfiles(s)
    for f in files:
        x = buildHTML(f, s)
        print(x)
