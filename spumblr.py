# -*- coding: utf-8 -*-
"""
spect function to create tumblr-style post from an image
STILL TO DO: look into image processing functionality to
potentially reduce img size

for example, consider using one of these: 
http://docs.wand-py.org/en/0.4.3/
https://tinypng.com/developers
https://pyimageoptimizer.readthedocs.io/en/latest/readme.html

"""

from spect_config import j
from tkinter.filedialog import askopenfilename
import string
import random
import time
import os
import shutil


def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # http://stackoverflow.com/a/2257449


def askForTags():
    if len(tags) > 0:
        print('Current tags: {}'.format(tags))
    t = input('Add a tag (or "X" to end; re-enter a tag to delete it): ')
    if not t.lower() == 'x' or t == '':
        if t in tags:
            tags.remove(t)
        else:
            tags.append(t)
        askForTags()
    else:
        return tags

rn = time.strftime('%Y-%m-%d')
img_dir = os.path.join(j['wdir'], 'images')
image = askopenfilename(title='Select an image for tumblr-style page post',
                        initialdir=j['localdir'])
c = input('Enter a caption: (or "X" for no caption): ')
if not c.lower() == 'x' or c == '':
    caption = c
    capt = True
else:
    capt = False
tags = []
tags.append(askForTags())
identifier = rn + '--' + id_generator()
imgname = identifier + '.' + image[-3:].lower()
newimg = os.path.join(img_dir, imgname)
mdfilename = identifier + '.md'
mdfile = os.path.join(j['localdir'], 'md', 'ephemeral', mdfilename)
mdtxt = 'Type: tumblr\n'
mdtxt += 'Spumblr_key: {}\n'.format(identifier)
mdtxt += 'Date: {}\n'.format(rn)
if len(tags) > 0:
    mdtxt += 'Tags: {}\n'.format(tags[0])
if len(tags) > 1:
    for t in range(1, len(tags)-1):
        mdtxt += '\t{}\n'.format(tags[t])

mdtxt += '\n<figure><img src="../images/{}"'.format(imgname)
if capt:
    mdtxt += ' alt="{}"'.format(caption)
# can figure out width/heigh sometime in python?
mdtxt += '>'
if capt:
    mdtxt += '<figcaption>{}</figcaption>'.format(caption)
mdtxt += '</figure>'
# shutil.copy(my_copy, os.path.join(backup_dir, backupname))
with open(mdfile, 'w') as fh:
    fh.write(mdtxt)
shutil.copy(image, newimg)
