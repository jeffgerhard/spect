# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 18:02:44 2016

@author: jcg
"""

import os
import json
from tkinter.filedialog import askdirectory, askopenfilename
import keyring

def checkConfigFile():
    if not os.path.exists(spectDir):
        os.makedirs(spectDir)
    if os.path.isfile(config):
        return True
    else:
        return False

def addMapSecs():
    t = input('Add a section title (or X to cancel): ')
    if t.lower() == 'x':
        return titlemap
    else:
        j['titlemap'][t] = input('What name should the folder have for "{}"? '.format(t))
        print(j['titlemap'])
        addMapSecs()

def rebuildConfig(j):
    for cfg in ['blogtitle','site','sitefolder']:
        if cfg in j:
            if input('Change {} from "{}" (y/n)? '.format(cfg, j[cfg])).lower() == "y":
                j[cfg] = input(varlib[cfg])
        else:
            j[cfg] = input(varlib[cfg])
    if 'titlemap' in j:
        print("Section titles are currently mapped like this:", json.dumps(j['titlemap'], indent=2))
        if input('Would you like to change them (y/n) ?').lower() == "y":
            addMapSecs()
    else:
        if input(varlib['titlemap']).lower() == "y":
            j['titlemap'] = dict()
            addMapSecs()
    for cfg in ['username', 'password', 'hostkeys']:
        if cfg in j:
            if input('Change {} from "{}" (y/n)? '.format(cfg, j[cfg])).lower() == "y":
                j[cfg] = input(varlib[cfg])
        else:
            j[cfg] = input(varlib[cfg])
    if 'localdir' in j:
        if input('Change local directory from {} (y/n)? '.format(j['localdir'])).lower() == "y":
            j['localdir'] = askdirectory(title=folderlib['localdir'])
    else:
        j['localdir'] = askdirectory(title=folderlib['localdir'])
    if 'winscp' in j:
        if input('Change location of winscp.com from {} (y/n)'.format(j['winscp'])).lower() == "y":
            j['winscp'] = askopenfilename(title=filelib['winscp'])
    else:
        j['winscp'] = askopenfilename(title=filelib['winscp'])
    return j            


userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')
version = '0.1'
varlib = {'blogtitle': "ok so what is your blog's name? ",
           'site': 'web host site (e.g., example.com)? ',
           'sitefolder': 'folder on server to use (e.g., "public_html/site") ?',
           'username': 'remote host username? ',
           'password': 'remote host password? ',
           'titlemap': '''spect can optionally map "section" to "foldernames",
so that, for example, the section called "personal" shows up
with a folder structure like example.com/blog
Do you want to do that? (y/n) ''',
            'hostkeys': 'insert the scary hostkeys string from winscp '}
folderlib = {'localdir': '''Choose a local directory, like "website", that has
the "md" directory inside it:'''}
filelib = {'winscp': 'find the winscp.com file! ' }


if not checkConfigFile():
    configurations = {}
    print('''going through first run setup....
first we'll set up some variables, then we need to locate some specific files and directories.

''')
    blogtitle = input("ok so what is your blog's name? ")
    site = input('web host site? (like example.com) ')
    sitefolder = input('folder on site to use? (e.g. "public_html/site") ')
    username = input('remote host username? ')
    password = input('remote host password? ')
    if input('''
spect can optionally map "section" to "foldernames",
so that, for example, the section called "personal" shows up
with a folder structure like {}/blog
Do you want to do that? (y/n)'''.format(sitefolder)) == "y":
        titlemap = addMapSecs()
    hostkeys = input('scary hostkeys string that you barely understand? ')
    winscp = askopenfilename(title='find the winscp.com file! ')
    localdir = askdirectory(title=
    'Choose a local directory, like "website", that has the "md" directory inside '
    )
    for i in ('blogtitle', 'site', 'hostkeys', 'username',
              'sitefolder', 'localdir', 'winscp', 'titlemap', 'version'):
        configurations[i] = locals()[i]
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(configurations, indent=4, sort_keys=True))
    keyring.set_password('spect', username, password)

with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()

j = json.loads(data)
j['password'] = keyring.get_password('spect', j['username'])
if not 'version' in j:
    print('No version found! Rebuilding config...\n\n')
    j = rebuildConfig(j)
    j['version'] = version
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(j, indent=2, sort_keys=True))
    keyring.set_password('spect', j['username'], j['password'])
if not j['version'] == version:
    print("\n\nConfiguration version is out of date. Let's rebuild.\n\n")
    j = rebuildConfig(j)
    j['version'] = version
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(j, indent=2, sort_keys=True))
    keyring.set_password('spect', j['username'], j['password'])

