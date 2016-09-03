# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:15:38 2016

@author: gerhardj
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
#    k, text = parseFile(lines)
    text = md.convert(t)
    k = md.Meta
    if s == 'blog':
        k['section'] = [blogtitle]
    else:
        k['section'] = [s]
    print(k)
    # print(markdown.markdown(text, extensions=['smarty']))
    htm += head(**k)
    htm += '<body>\n'
    htm += header(**k)
    htm += md.convert(text)
    htm += '</body></html>'
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
    htm = '<header>\n'
    htm += '\t'
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
