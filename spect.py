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


def parseFile(l):
    if l[0:2] == '$$':
        v, z = l.split(":")
        return v[2:], z


def buildHTML(f, s):
    h = os.path.join(mddir, s, f)
    with open(h, mode='r', encoding='utf-8') as z:
        text = z.read()
        lines = text.splitlines()
        for l in lines:
            if not l == '':
                print(parseFile(l))
      

localdir = r'C:\Users\gerhardj\Dropbox\__websites\python\testsite'
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')

secs = get_immediate_subdirectories(mddir)

for s in secs:
    files = get_jfiles(s)
    for f in files:
        buildHTML(f, s)
    
