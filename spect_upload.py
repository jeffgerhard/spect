# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 14:57:38 2016

@author: jcg
"""

import os
#import json
#from tkinter.filedialog import askdirectory, askopenfilename
from subprocess import Popen, PIPE
from spect_config import j
from spect_config import password as pw
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

# basically stealing this method http://stackoverflow.com/a/33420817


localdir = j['localdir']
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
WINSCP = j['winscp']
upload_files(j['site'], j['username'], pw, j['hostkeys'],
             wdir, j['sitefolder'])
