# -*- coding: utf-8 -*-
"""
Working with the config file, which is located in the user folder
If keyring is installed, that will hold the server password
If not, I can add a functionality to include the pw in the config

If run separately, will offer options to reset configuration / may add more
admin features here later
"""

import os
import json
from tkinter.filedialog import askdirectory, askopenfilename
try:
    import keyring
    kr = True
except ImportError:
    print('keyring not installed; password will be stored in plaintext.')
    kr = False

def checkConfigFile():
    '''returns True/False on whether .spect directory has configfile'''
    if not os.path.exists(spectDir):
        os.makedirs(spectDir)
    if os.path.isfile(config):
        return True
    else:
        return False

def rebuildConfig(j):
    for cfg in ['blogtitle','site','sitefolder']:
        if cfg in j:
            if input('Change {} from "{}" (y/n)? '.format(cfg, j[cfg])).lower() == "y":
                j[cfg] = input(varlib[cfg])
        else:
            j[cfg] = input(varlib[cfg])
    for cfg in ['username', 'hostkeys']:
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
    if kr:
        pw = keyring.get_password('spect', j['username'])
        if input('Change password from {}? (y/n) '.format(pw)).lower() == "y":
            newpw = input('New password: ')
            keyring.set_password('spect', j['username'], newpw)
    return j            

userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')
version = '0.2.1' # 10/12/2016
varlib = {'blogtitle': "ok so what is your blog's name? ",
           'site': 'web host site (e.g., example.com)? ',
           'sitefolder': 'folder on server to use (e.g., "public_html/site") ?',
           'username': 'remote host username? ',
           'password': 'remote host password? ',
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
    hostkeys = input('scary hostkeys string that you barely understand? ')
    winscp = askopenfilename(title='find the winscp.com file! ')
    localdir = askdirectory(title=
    'Choose a local directory, like "website", that has the "md" directory inside '
    )
    for i in ('blogtitle', 'site', 'hostkeys', 'username',
              'sitefolder', 'localdir', 'winscp', 'version'):
        configurations[i] = locals()[i]
    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(configurations, indent=4, sort_keys=True))
    keyring.set_password('spect', username, password)

with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()
j = json.loads(data)
password = keyring.get_password('spect', j['username'])
if __name__ == "__main__":
    if input('set up configuration? (y/n) ').lower() == 'y':
            #redo configuration stuff
        j['version'] = version
        rebuildConfig(j)
else:
    if not 'version' in j:
        print('No version found! Rebuilding config...\n\n')
        j = rebuildConfig(j)
        j['version'] = version
        with open(config, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(j, indent=2, sort_keys=True))
        keyring.set_password('spect', j['username'], password)
    if not j['version'] == version:
        print("\n\nConfiguration version is out of date. Let's rebuild.\n\n")
        j = rebuildConfig(j)
        j['version'] = version
        with open(config, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(j, indent=2, sort_keys=True))
        keyring.set_password('spect', j['username'], password)
    
