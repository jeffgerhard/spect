# -*- coding: utf-8 -*-
"""
all admin data:

return the data library as library class; the config data as config dictionary; 
the sitevars data as sitevars dictionary; password as string; dirs as class

these have different features

library has to be included or something is real wrong // it is a part of spect
config lives locally in user directory
sitevars live with the markdowns and other files and are backed up online

"""


import os
import json
import utils
from tkinter.filedialog import askdirectory, askopenfilename
import keyring
#try:
#    import keyring
#    kr = True
#except ImportError:
#    print('keyring not installed; password will be stored in plaintext.')
#    kr = False
from subprocess import Popen, PIPE
#import urllib
from dateutil.parser import parse
import datetime


###########################################################################
# SITEVARS FUNCTIONS
###########################################################################

def svfile(a):
    return os.path.join(a, 'sitevars.json')

def runsvchecks(d, config, password, library):
    """run through a number of checks to see if the sitevars file exists,
    if a remote copy exists, if they match, and if the sv is up to date and
    valid. if not, tries to fix all these things.      d = admindir"""
    result = False
    local = False
    remote = False
    svdir = svfile(d)
    if checksv(d):
        local = True
    remotestatus, remotesize, remotedate = checkremote(config, password)
    if remotestatus:
        remote = True
    if local and remote:
        print('both exist')
        localsize = os.path.getsize(svfile(d))
        localdate = os.path.getmtime(svfile(d))
        localdt = datetime.datetime.fromtimestamp(localdate)
        tdelta = localdt - remotedate
        if tdelta.total_seconds() < 20:
            return True
        else:
            print('there is a significant discrepancy between the local and '
                  'remote timestamps for the sitevars!')
            print('({})'.format(tdelta))
            print('local date: ', localdt)
            print('local size: ', localsize)
            print('remote date: ', remotedate)
            print('remote size: ', remotesize)
            if tdelta.total_seconds() > 0:  # local is newer
                print('\nThe local sitevars are newer than the remote ones.')
                _ = input('Do you want to upload and replace the remote file? (y/n) ')
                if _.lower() == 'y':
                    if uploadFile(config, password, svfile(d), 
                                  config['sitefolder'] + '/admin/', confirm=False):
                        print('upload succeeded. sitevars ok.')
                        return True
                elif _.lower() == 'n':
                    print('\n\n')
                    _ = input('Then do you want to download and replace the local file? (y/n) ')
                    if _.lower() == 'y':
                        x = downloadFile(config, password, 
                                         config['sitefolder'] + '/admin/sitevars.json', 
                                         dirs.admindir + '\sitevars.json',
                                         confirm=False)
                        return runsvchecks(d, config, password, library)
    elif local and not remote:
        print('no remote sitevars file found!')
        _ = input('upload the local file? (y/n)')
        if _.lower() == 'n':
            print('''Ok. Working only with a local version of sitevars. But
SPECT will keep nagging you until you upload a backup copy or else
maybe edit the source code. (try around line 90 of the admin.py file''')
            return True
        else:
            if uploadFile(config, password, svfile(d), config['sitefolder'] + '/admin/'):
                return True
            else:
                print('Upload error!')
        # figure out why and upload the local one
    elif remote and not local:
        _ = input('\nThere is a remote version of the site variables, but no '
                  'local copy.\n\nWould you like to [d]ownload the remote '
                  'version? [b]uild a new local file to sync? or [x]ancel? ')
        if _.lower() == 'b':
            svs = buildsvs(svdir)
            with open(svfile(d), 'w', encoding='utf-8') as fh:
                fh.write(json.dumps(svs, indent=4, sort_keys=True))
            print('\n\nNew sitevars saved. Hit enter to upload and overwrite the ')
            _ = input('old ones (or X to cancel)')
            if _.lower() == 'x':
                print('\n\nOk! Exiting for now... figure out the sitevars!')
                return False
            else:
                uploadFile(config, password, svfile(d), config['sitefolder'] + '/admin/', confirm=False)
            return runsvchecks(d, config, password, library)
        elif _.lower() == 'x':
            raise ValueError('sitevars halted')
        elif _.lower() == 'd':
            x = downloadFile(config, password, config['sitefolder'] + '/admin/sitevars.json', dirs.admindir + '\sitevars.json')
            return runsvchecks(d, config, password, library)
            # need to implement the download
        else:
            print('Please try that again')
            return runsvchecks(d, config, password, library)
        # figure out why and download the remote one
    elif not local and not remote:
        print('\nSPECT cannot detect any sitevars!')
        svs = buildsvs(svdir)
        with open(svfile(d), 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(svs, indent=4, sort_keys=True))
        return runsvchecks(d, config, password, library)
    else:
        print('one or both files missing')
    return result


def checksv(a):
    os.makedirs(a, exist_ok=True)
    result = False
    if os.path.isfile(svfile(a)):
        return True
    return result


def checkremote(config, password):
    status, filesize, filedate = checkRemoteFile(config, password,
                                                 config['sitefolder'] + '/admin/sitevars.json')
#    print('status', status)
    return status, filesize, filedate


def buildsvs(svdir):
    print('Hello. I notice that you haven\'t set up the site variables\n'
          'Generating them at {}. This is a text file that you '
          'can edit by hand later.'.format(svdir))
    sitevars = dict()
    sitevars['version'] = library.sitevars_version
    for sv in library.sitevars_build:
        if sv['required']:
            if sv['type'] in ['string', 'boolean']:
                sitevars[sv['name']] = askforvar(sv['description'], sv['name'], sv['type'])
            elif sv['type'] == 'list':
                pass
            elif 'depends_on' in sv:
                print(sv)
                if sitevars[sv['depends_on']]:
                    sitevars[sv['name']] = askforvar(sv['description'], sv['name'], sv['type'])
        else:
            if 'depends_on' in sv:
                if sitevars[sv['depends_on']]:
                    if 'based_on' in sv:
                        sitevars[sv['name']] = dict()
                        for _ in sitevars[sv['based_on']]:
                            _desc = '[' + _ + '] - ' + sv['description']
                            sitevars[sv['name']][_] = askforvar(_desc, sv['name'])
                    else:
                        sitevars[sv['name']] = askforvar(sv['description'], sv['name'], sv['type'])
    return sitevars


def askforvar(x, y, vtype='string'):
    def var_query(x, y):
        res = input(x + ' ')
        _ = ('you entered "{}" for {}. If that\'s cool, hit enter,'
             ' or hit X to retry '.format(res, y))
        confirm = input(_)
        if confirm.lower() == 'x':
            res = askforvar(x, y)
        return res
    print('\n\n{:-^30}'.format(' ' + y + ' '))
    if vtype == 'string':
        return var_query(x, y)
    elif vtype == 'boolean':
        res = var_query(x, y)
        if res.lower() in ['yes', 'true', '1', 'y', 't']:
            resb = True
        elif res.lower() in ['no', 'false', '0', 'n', 'f']:
            resb = False
        else:
            print('The value for {} has to be in a yes/no or true/false '
                  'format! Re-enter it, bitte sehr!'.format(y))
            resb = askforvar(x, y, vtype)
        return resb
    elif vtype == 'list':
        print('\nEnter some {}. Just hit enter to finish adding.'.format(y))
        z = 'category name'
        c = 1
        resl = list()
        while z != '':
            z = var_query('(' + str(c) + ') ' + x, y)
            if z != '':
                resl.append(z)
            c += 1
        return resl


def returnsitevars(d):
    with open(svfile(d), 'r', encoding='utf-8') as fh:
        _ = fh.read()
        return json.loads(_)


def checkConfigFile():
    '''s for spectdir, c for configfile location. returns True/False'''
    exists = False
    _ = os.path.expanduser('~')
    configdir = os.path.join(_, '.spect')
    configfileloc = os.path.join(configdir, 'config.ini')
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    if os.path.isfile(configfileloc):
        exists = True
    return exists, configfileloc


def rebuildConfig(config, phrase, library):
    print(phrase)
    for _ in library.config_build:
        if _['name'] in config:
            config[_['name']] = config_entry(_, config[_['name']], _['name'] in config)
    pw = keyring.get_password('spect', config['username'])
    if input('Change password from {}? (y/n) '.format(pw)).lower() == "y":
        newpw = input('New password: ')
        keyring.set_password('spect', config['username'], newpw)
    extracfgs = []
    for c in config:
        here = False
        for x in library.config_build:
            if x['name'] == c:
                here = True
        if not here:
            extracfgs.append(c)
    print('deleted some extra configuration entries:', extracfgs)
    for c in extracfgs:
        del config[c]
    config['version'] = library.config_version
    print(config)
    return config


def config_entry(_, name, exists):
    print('\n\n{:-^30}\n'.format(' ' + _['name'] + ' '))
    if exists:
        question = input('Change {} from "{}" (y/n)? '.format(_['name'], name))
    if exists is False or question == "y":
        if _['type'] == 'string':
            return input(_['description'] + ' ')
        elif _['type'] == 'folder':
            input('Ok hit ENTER then select a directory.')
            return askdirectory(title=_['description'])
        elif _['type'] == 'file':
            input('Ok hit ENTER to choose the proper file.')
            return askopenfilename(title=_['description'])
    else:
        return name

###########################################################################
# REMOTE UPLOAD/DOWNLOAD/CHECK THE SERVER TOOLS
###########################################################################

def remotecommit(cmds, WINSCP, exit=True):
    if exit:
        cmds.append('exit\n')
    with Popen(WINSCP, stdin=PIPE, stdout=PIPE, stderr=PIPE,
               universal_newlines=True) as winscp:
        stdout, stderr = winscp.communicate('\n'.join(cmds))
#        print(stdout)
    return winscp.returncode, stdout


def remotestring(config, pwd):
    cmds = []
    cmds.append('open sftp://{user}:{passwd}@{host}/ -hostkey="{hkeys}"'.format(
                host=config['site'],
                user=config['username'],
                passwd=pwd,
                hkeys=config['hostkeys']
                ))
    return cmds


def checkRemoteFile(config, pwd, file):
    cmds = remotestring(config, pwd)
    cmds.append('stat {}'.format(file))
    returncode, output = remotecommit(cmds, config['winscp'])
    if returncode == 0:
        lines = output.splitlines()
        stat = lines[-2].split('  ')[-1].strip()
        props = stat.split()
        filedate = (' ').join(props[1:5])
        filesize = props[0]
#        print('filedate', filedate)
#        print('filesize', filesize)
#        print(parse(filedate).date())
        return True, filesize, parse(filedate)
    else:
        return False, None, None


def uploadFile(config, pwd, file, remotedir, confirm=True):
    #  print(file, remotedir)
    cmds = remotestring(config, pwd)
    if confirm == False:
        cmds.append('option confirm off')
    cmds.append('put ' + file + ' ' + remotedir)
    returncode, output = remotecommit(cmds, config['winscp'])
    if returncode == '0':
        return True
    else:
        return False


def downloadFile(config, pwd, remotefile, localdir, confirm=True):
    cmds = remotestring(config, pwd)
    if confirm is False:
        cmds.append('option confirm off')
    cmds.append('get ' + remotefile + ' ' + localdir)
    returncode, output = remotecommit(cmds, config['winscp'])
    if returncode == '0':
        print('file downloaded successfully.')
        return True
    else:
        return False

# LIBRARY

_ = os.path.dirname(__file__)
with open(os.path.join(_, 'data/library.json'), 'r', encoding='utf-8') as fh:
    library = utils.Dict2Obj(json.loads(fh.read()))

# CONFIG FILE

def configure():
    _, configfileloc = checkConfigFile()
    if _:
        with open(configfileloc, 'r', encoding='utf-8') as fh:
            data = fh.read()
        config = json.loads(data)
        password = keyring.get_password('spect', config['username'])
    else:
        print("Can't find the basic configuration for this computer!")
        _ = input('\nWould you like to build them from scratch? (y/n)')
        if _.lower() == 'y':
            pass
        else:
            print('Ending this charade, then.')
            return
    if 'version' not in config:
        config = rebuildConfig(config,
                               'No version found! Rebuilding config...\n\n',
                               library)
        utils.savejson(config, configfileloc)
    elif not config['version'] == library.config_version:
        config = rebuildConfig(config,
                               "\n\nConfiguration version is out of date. Let's rebuild.\n\n",
                               library)
        utils.savejson(config, configfileloc)
    return config, password

# DIRS

def build_dirs(x):
    class Dirs(object):
        def __init__(self):
            self.data = []
    y = Dirs()
    y.localdir = x
    y.mddir = os.path.join(x, 'md')
    y.wdir = os.path.join(x, 'blog')
    y.admindir = os.path.join(x, 'admin')
    y.tagwebdir = os.path.join(x, 'tags')
    return y

config, password = configure()
dirs = build_dirs(config['localdir'])

# SITEVARS

if runsvchecks(dirs.admindir, config, password, library):
    print('config is good')
    sitevars = returnsitevars(dirs.admindir)
else:
    print('there is some problem with the sitevars configuration '
          '(or more likely the code)')

# STILL TO DO: Enable editing of all of these if name = main
