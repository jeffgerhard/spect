# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 14:57:38 2016

@author: jcg
"""

#import os
#import json
#from tkinter.filedialog import askdirectory, askopenfilename
from subprocess import Popen, PIPE
from spect_config import j

class UploadFailed(Exception):
    pass


def upload_files(host, user, passwd, hkeys, local, remote):
    # cmds = ['option batch abort', 'option confirm off']
    cmds = []
    cmds.append('open sftp://{user}:{passwd}@{host}/ -hostkey="{hkeys}"'.format(
    host=host, user=user, passwd=passwd, hkeys=hkeys))
    # cmds.append('put {} ./'.format(' '.join(files)))
    cmds.append('synchronize remote -delete {} {}'.format(local, remote))
    cmds.append('exit\n')
    print(cmds)
    with Popen(WINSCP, stdin=PIPE, stdout=PIPE, stderr=PIPE,
               universal_newlines=True) as winscp:
        stdout, stderr = winscp.communicate('\n'.join(cmds))
    if winscp.returncode:
        # WinSCP returns 0 for success, so upload failed
        raise UploadFailed

#userDir = os.path.expanduser('~')
#spectDir = os.path.join(userDir, '.spect')
#config = os.path.join(spectDir, 'config.ini')
#
#if not checkConfigFile():
#    configurations = {}
#    print('going through first run setup..../n/n')
#    blogtitle = input("ok what is your blog's name? ")
#    site = input('web host site? ')
#    sitefolder = input('folder on site to use? (include the public_html) ')
#    username = input('remote host username? ')
#    password = input('remote host password? ')
#    hostkeys = input('scary hostkeys string that you barely understand? ')
#    winscp = askopenfilename('find the winscp.com file! ')
#    localdir = askdirectory(title='Choose a local directory with the file \
#                        root, like "website" with a "md" directory inside ')
#    for i in ('blogtitle', 'username', 'site', 'password', 'hostkeys',
#              'sitefolder', 'localdir'):
#        configurations[i] = locals()[i]
##    configurations['username'] = username
#    with open(config, 'w', encoding='utf-8') as fh:
#        fh.write(json.dumps(configurations, indent=4, sort_keys=True))

#with open(config, 'r', encoding='utf-8') as fh:
#    data = fh.read()
#
#j = json.loads(data)

# what about this method http://stackoverflow.com/a/33420817


localdir = j['localdir']
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
WINSCP = j['winscp']
#
upload_files(j['site'], j['username'], j['password'], j['hostkeys'],
             wdir, j['sitefolder'])
