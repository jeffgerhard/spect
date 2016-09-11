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

userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')

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
    hostkeys = input('scary hostkeys string that you barely understand? ')
    winscp = askopenfilename(title='find the winscp.com file! ')
    localdir = askdirectory(title=
    'Choose a local directory, like "website", that has the "md" directory inside '
    )
    for i in ('blogtitle', 'site', 'hostkeys', 'username',
              'sitefolder', 'localdir', 'winscp'):
        configurations[i] = locals()[i]
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(configurations, indent=4, sort_keys=True))
    keyring.set_password('spect', username, password)

with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()

j = json.loads(data)
j['password'] = keyring.get_password('spect', j['username'])
