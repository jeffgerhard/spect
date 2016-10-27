# -*- coding: utf-8 -*-
"""
Working with the config file, which is located in the user folder
If keyring is installed, that will hold the server password
If not, I can add a functionality to include the pw in the config

If run separately, will offer options to reset configuration / may add more
admin features here later

note that there is some site-level metadata that would be good to put into
an admin folder and also upload to the server. things like site description,
category descriptions, cat types (i want to implement a tumblr-style category)

"""

from spect_utils import get_immediate_subdirectories
import os
import json
from tkinter.filedialog import askdirectory, askopenfilename
try:
    import keyring
    kr = True
except ImportError:
    print('keyring not installed; password will be stored in plaintext.')
    kr = False
    # COME BACK TO THIS L8ER


def checkConfigFile():
    '''returns True/False on whether .spect directory has configfile'''
    if not os.path.exists(spectDir):
        os.makedirs(spectDir)
    if os.path.isfile(config):
        return True
    else:
        return False


def checkAdminFile(j):
    '''returns True/False on local admin file exists'''
    admindir = os.path.join(j['localdir'], 'www', 'admin')
    os.makedirs(admindir, exist_ok=True)
    if os.path.isfile(os.path.join(admindir, 'admin.json')):
        # need to check the categories!
        return True
    else:
        return False


def buildAdminFile(j):
    print('''The admin info is descriptive stuff about the blog, like its title,
category names, etc. It is stored in the local folder and we need to keep it in
sync across all instances.''')
    admin = dict()
    admin['blogtitle'] = input(varlib['blogtitle'])
    secs = get_immediate_subdirectories(j['mddir'])
    if 'categories' in admin:
        pass  # come back to this
    else:
        admin['categories'] = list()
        for cat in secs:
            c = dict()
            c['category'] = cat
            c['description'] = input('Add a description for category {}: '.format(cat))
            # later add type
            admin['categories'].append(c)
# need to build the category names based on existing cats in local folder. hmm.
    with open(os.path.join(admindir, 'admin.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(admin, indent=4, sort_keys=True))


def rebuildConfig(j):
    for cfg in ['site', 'sitefolder']:
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
    mddir = os.path.join(j['localdir'], 'md')
    wdir = os.path.join(j['localdir'], 'www')
    admindir = os.path.join(wdir, 'admin')
    tagdir = os.path.join(admindir, 'tags')
    tagwebdir = os.path.join(wdir, 'tags')
    for i in site_vars:
        j[i] = locals()[i]
    return j            

userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')
version = '0.3.0' # 10/26/2016
varlib = {'blogtitle': "ok so what is your blog's name? ",
           'site': 'web host site (e.g., example.com)? ',
           'sitefolder': 'folder on server to use (e.g., "public_html/site") ?',
           'username': 'remote host username? ',
           'password': 'remote host password? ',
            'hostkeys': 'insert the scary hostkeys string from winscp ',
            'blogdescription': 'give a description for this blog '}
folderlib = {'localdir': '''Choose a local directory, like "website", that has
the "md" directory inside it:'''}
filelib = {'winscp': 'find the winscp.com file! ' }
site_vars = ['mddir', 'wdir', 'admindir', 'tagdir', 'tagwebdir']

if not checkConfigFile():
    configurations = {}
    print('''going through first run setup....
first we'll set up some variables, then we need to locate some specific files and directories.

''')
#    site = input('web host site? (like example.com) ')
#    sitefolder = input('folder on site to use? (e.g. "public_html/site") ')
#    username = input('remote host username? ')
#    password = input('remote host password? ')
#    hostkeys = input('scary hostkeys string that you barely understand? ')
#    winscp = askopenfilename(title='find the winscp.com file! ')
#    localdir = askdirectory(title=
#    'Choose a local directory, like "website", that has the "md" directory inside '
#    )
    j = rebuildConfig(configurations)

#    for i in ('site', 'hostkeys', 'username',
#              'sitefolder', 'localdir', 'winscp', 'version'):
#        configurations[i] = locals()[i]

    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(j, indent=4, sort_keys=True))
#    keyring.set_password('spect', username, password)
with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()
j = json.loads(data)
password = keyring.get_password('spect', j['username'])
admindir = os.path.join(j['localdir'], 'www', 'admin')
if __name__ == "__main__":
    if input('set up configuration? (y/n) ').lower() == 'y':
            #redo configuration stuff
        j = rebuildConfig(j)
        j['version'] = version
        with open(config, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(j, indent=2, sort_keys=True))
        keyring.set_password('spect', j['username'], password)
else:
    if not checkAdminFile(j):
        print('No admin info found!')
        dl = input('Do you want to try to download it from the server? (y/n) ')
        #  implement that if yes
        buildAdminFile(j)
    with open(os.path.join(admindir, 'admin.json'), 'r', encoding='utf-8') as fh:
        data = fh.read()
    admin = json.loads(data)
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

