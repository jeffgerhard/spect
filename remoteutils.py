# -*- coding: utf-8 -*-
"""
i need regular use of utilities to upload and download things from the server

for the time being, these are windows utilities using winscp to handle 
server connections and security. 

later i will the option to work purely offline and allow a user full control 
of all uploading

later still i will add linux and osx capabilities (should be easier, they
have better built-in tools like rsync)

this needs to work as follows:
 - assume config exists locally and the relevant variables are
   passed thru to these functions as variables
 - check to see if certain files/folders exist on server or not
 - check to see if there are any files/folders on server that are not expected
 - upload specified files and folders
 - download specified files and folders (eg administrative data)
 - overwrite remote files with or without warning
 - overwrite local files with or without warning
 
later -- some more robust backup features, esp for images // as this thing
grows i will have lots of images i don't want sitting on dbx

"""



import os
##import json
##from tkinter.filedialog import askdirectory, askopenfilename
from subprocess import Popen, PIPE
#from spect_config import j
#from spect_config import password as pw
class UploadFailed(Exception):
    print('upload failed?')
    pass
#
#
def upload_files(host, user, passwd, hkeys, local, remote):
    # cmds = ['option batch abort', 'option confirm off']
    cmds = []
    cmds.append('open sftp://{user}:{passwd}@{host}/ -hostkey="{hkeys}"'.format(
    host=host, user=user, passwd=passwd, hkeys=hkeys))
    # cmds.append('put {} ./'.format(' '.join(files)))
    cmds.append('synchronize remote -delete {} {}'.format(local, remote))
    cmds.append('exit\n')
#    print(cmds)
    with Popen(WINSCP, stdin=PIPE, stdout=PIPE, stderr=PIPE,
               universal_newlines=True) as winscp:
        stdout, stderr = winscp.communicate('\n'.join(cmds))
    if winscp.returncode:
        # WinSCP returns 0 for success, so upload failed
        print('upload problem!')
        raise UploadFailed

def remotecommit(cmds, WINSCP, exit=True):
    with Popen(WINSCP, stdin=PIPE, stdout=PIPE, stderr=PIPE,
               universal_newlines=True) as winscp:
        stdout, stderr = winscp.communicate('\n'.join(cmds))
    print(stdout)
    return winscp.returncode

def remotestring(config, pwd):
    cmds = []
    cmds.append('open sftp://{user}:{passwd}@{host}/ -hostkey="{hkeys}"'.format(
    host=config['site'],
    user=config['username'],
    passwd=pwd,
    hkeys=config['hostkeys']))
    return cmds

def checkRemoteFile(config, pwd, file):
    cmds = remotestring(config, pwd)
    cmds.append('stat {}'.format(file))
    return remotecommit(cmds, config['winscp'])
    
    # cf https://winscp.net/eng/docs/script_checking_file_existence
#
## basically stealing this method http://stackoverflow.com/a/33420817
#
#def download_admin(host, user, passwd, hkeys, remote, local):
#    # cmds = ['option batch abort', 'option confirm off']
#    cmds = []
#    cmds.append('open sftp://{user}:{passwd}@{host}/ -hostkey="{hkeys}"'.format(
#    host=host, user=user, passwd=passwd, hkeys=hkeys))
#    # cmds.append('put {} ./'.format(' '.join(files)))
#    cmds.append('get {}/admin/admin.json {}\\ -neweronly'.format(remote, local))
#    cmds.append('exit\n')
#    # print(cmds)
#    with Popen(WINSCP, stdin=PIPE, stdout=PIPE, stderr=PIPE,
#               universal_newlines=True) as winscp:
#        stdout, stderr = winscp.communicate('\n'.join(cmds))
#    if winscp.returncode:
#        # WinSCP returns 0 for success, so upload failed
#        print('download problem!')
#        print(winscp.returncode)
#        return False
#    else:
#        return True
#
#
#localdir = j['localdir']
#mddir = j['mddir']
#wdir = j['wdir']
#tagwdir = os.path.join(j['localdir'], 'tags')
#WINSCP = j['winscp']
#tagremote = j['sitefolder'][:-5] + '/tags' # this is deleting 'blog' but need to rethink!
if __name__ == "__main__":
    import admin
    print(checkRemoteFile(admin.config, admin.password,
                          admin.config['sitefolder'] + '/admin/admin.json'))
#    upload_files(j['site'], j['username'], pw, j['hostkeys'],
#                 j['wdir'], j['sitefolder'])
#    # now let's do tags somewhat differently... more to work on later
##    upload_files(j['site'], j['username'], pw, j['hostkeys'],
##                 tagwdir, tagremote)
