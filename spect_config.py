# -*- coding: utf-8 -*-
"""
Working with the config file, which is located in the user folder
If keyring is installed, that will hold the server password
If not, I can add a functionality to include the pw in the config

If run separately, will offer options to reset configuration / may add more
admin features here later

hmm running into difficulties with site upload/download / hitting the limits
here of a config util that can serve up site variables and check config vs
calling other files that rely on the site metadata.

i almost have to map this stuff out. this will also tie into doing backups 
and other server work in the future.

think about a generalized workflow like:
 - check site config data exists
     - if not (or outdated version) -- add it!
     - if yes:
 - check admin data exists online
 - check admin data exists locally
     - if both: compare and ask for help if no match
     - if online only: copy locally
     - if local only: ask about uploading it
     - if neither -- create it!


so the problem is, i need a way to call CONFIG data from the upload/download tool
in order to modify the ADMIN data

could either split it out into multiple script files (not ideal)...
or... reorganize a bit? 
note that the uploader doesn't even need any of the admin data, just config

i think probably the best thing to do is have a metadata script that checks and 
returns both files IF NECESSARY but can just do one or t'other. but is that even
possible?

"""

from spect_utils import get_immediate_subdirectories
# from spect_upload import download_admin
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
    admindir = os.path.join(j['localdir'], 'blog', 'admin')
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
    admin['blogdescription'] = input('Enter the blog description (this can include markdown and you can edit it in a text editor later)')
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
    if 'pngquant' in j:
        if input('Change location of pngquant.exe from {} (y/n)'.format(j['pngquant'])).lower() == "y":
            j['pngquant'] = askopenfilename(title=filelib['pngquant'])
    else:
        j['pngquant'] = askopenfilename(title=filelib['pngquant'])
    if kr:
        pw = keyring.get_password('spect', j['username'])
        if input('Change password from {}? (y/n) '.format(pw)).lower() == "y":
            newpw = input('New password: ')
            keyring.set_password('spect', j['username'], newpw)
    mddir = os.path.join(j['localdir'], 'md')
    wdir = os.path.join(j['localdir'], 'blog')
    admindir = os.path.join(wdir, 'admin')
#    tagdir = os.path.join(admindir, 'tags')
#    tagwebdir = os.path.join(wdir, 'tags')
    tagwebdir = os.path.join(j['localdir'], 'tags')
    for i in site_vars:
        j[i] = locals()[i]
    return j            

userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')
version = '0.5' # 1/26/2017 -- adding path to pngquant
varlib = {'blogtitle': "ok so what is your blog's name? ",
           'site': 'web host site (e.g., example.com)? ',
           'sitefolder': 'folder on server to use (e.g., "public_html/site") ?',
           'username': 'remote host username? ',
           'password': 'remote host password? ',
            'hostkeys': 'insert the scary hostkeys string from winscp ',
            'blogdescription': 'give a description for this blog '}
folderlib = {'localdir': '''Choose a local directory, like "website", that has
the "md" directory inside it:'''}
filelib = {'winscp': 'find the winscp.com file! ',
           'pngquant': 'find the path to the pngquant.exe file '}
site_vars = ['mddir', 'wdir', 'admindir', 'tagwebdir']

if not checkConfigFile():
    configurations = {}
    print('''going through first run setup....
first we'll set up some variables, then we need to locate some specific files and directories.

''')
    j = rebuildConfig(configurations)

    with open(config, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(j, indent=4, sort_keys=True))
#    keyring.set_password('spect', username, password)
with open(config, 'r', encoding='utf-8') as fh:
    data = fh.read()
j = json.loads(data)
password = keyring.get_password('spect', j['username'])
admindir = os.path.join(j['localdir'], 'blog', 'admin')
if __name__ == "__main__":
    if input('set up configuration? (y/n) ').lower() == 'y':
        j = rebuildConfig(j)
        j['version'] = version
        with open(config, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(j, indent=2, sort_keys=True))
        keyring.set_password('spect', j['username'], password)
else:
    if not checkAdminFile(j):
        print('No admin info found!')
        dl = input('Do you want to try to download it from the server? (y/n) ')
#        if dl.lower() == 'y':
#            download_admin()
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

