# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 18:02:44 2016

@author: jcg
"""

import os
import json
from tkinter.filedialog import askdirectory, askopenfilename


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
    print('going through first run setup..../n/n')
    blogtitle = input("ok what is your blog's name? ")
    site = input('web host site? ')
    sitefolder = input('folder on site to use? (include the public_html) ')
    username = input('remote host username? ')
    password = input('remote host password? ')
    hostkeys = input('scary hostkeys string that you barely understand? ')
    winscp = askopenfilename('find the winscp.com file! ')
    localdir = askdirectory(title='Choose a local directory with the file \
                        root, like "website" with a "md" directory inside ')
    for i in ('blogtitle', 'username', 'site', 'password', 'hostkeys',
              'sitefolder', 'localdir'):
        configurations[i] = locals()[i]
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(configurations, indent=4, sort_keys=True))

with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()

j = json.loads(data)
