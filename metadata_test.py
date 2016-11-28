# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 21:11:33 2016

@author: J

 - ok check site config data exists [via calling j from config]
     - if not (or outdated version) -- add it!
     - when yes:
         - check admin data exists online
         - check admin data exists locally
             - if both: compare and ask for help if mismatch
             - if online only: copy locally
             - if local only: ask about uploading it
             - if neither -- create it!
"""

from spect_upload import download_admin
from spect_config import j
from spect_config import password as pw
from spect_config import checkAdminFile
import os
import filecmp

adminbackup = os.path.join(j['localdir'], 'admin.json')
adminfile = os.path.join(j['admindir'], 'admin.json')

if __name__ == "__main__":
#    if input('set up configuration? (y/n) ').lower() == 'y':
#        pass

#    print(j)
#    print(pw)
    if download_admin(j['site'], j['username'], pw, j['hostkeys'], j['sitefolder'], j['localdir']):
        print('whoa it worked; we have an admin file online')
        backup = True
    localadmin = checkAdminFile(j)
    
    if backup and localadmin:
        print('we have both files so lets compare them')
        if filecmp.cmp(adminbackup, adminfile):
            print('cool both admin copies are identical. you may proceed.')
            os.remove(adminbackup)
        else:
            print('backup admin file does not match the local file! Overwriting backup is not yet implemented so do it manually if necessary.')
    elif backup:
        print('we have a backup, or retrieved it from online, so see if that will suffice')
        print('the backup is located at {}'.format(adminbackup))
    elif localadmin:
        print('there is no backup of the admin online! do it now!')
    else:
        print('hokay have to generate an admin file')

# then i want to allow for updating admin data; 
# also when uploading i want to compare categories and offer to add descriptions
# for any new ones!