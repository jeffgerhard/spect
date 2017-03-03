# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 20:35:20 2016

@author: J
"""
import os
from PIL import Image
from resizeimage import resizeimage
from os.path import splitext as splitext
from slugify import slugify
from subprocess import check_call
from shutil import copyfile
import json
from tkinter.filedialog import askopenfilename
import tempfile

def get_immediate_subdirectories(a_dir):
# stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python#800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def imgwidth(filename, w, output):
    with open(filename, 'rb') as f:
        img = Image.open(f)
        try:
            img = resizeimage.resize_width(img, w)
            img.save(output, img.format)
            return True
        except:
            return False


def derive_images(filename):
    derives = []
    undersize = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for w in [1280, 620, 500, 400, 250]:  # these are the tumblr sizes (minus a 75sq thumbnail)
            name = os.path.basename(filename)
            name = splitext(name)[0] + '_' + str(w) + splitext(name)[1]
            if imgwidth(filename, w, os.path.join(tmpdir, name)):
                derives.append(name)
            else:
                undersize.append(w)
            # come back to this -- i think i want to use the full-size, if big enough, in the srcset
        for d in derives:
            if splitext(d)[1] == '.png':
                fn = os.path.join(tmpdir, d)
                check_call('{} --force --strip --speed=1 --quality=50-90 --ext .png --skip-if-larger -- {}'.format(j['pngquant'], fn))
                if os.path.getsize(fn) > os.path.getsize(filename):
                    os.remove(fn)
                    copyfile(filename, fn)
                #  PyImageOptimizer.optimize_png(d, backup=False)
            elif splitext(d)[1] == '.jpg':
                pass
                #PyImageOptimizer.optimize_jpg(d, backup=False)
        for d in derives:
            copyfile(os.path.join(tmpdir, d), os.path.join(alt, d))
        if len(undersize) > 0:
            und = min(undersize)
        else:
            und = ''
        return derives, und


def generate_img_html(filename, caption=''):
    # this is really only useful for large images, certainly over 600px wide
# so it would be good to check that first
    large = False
    ogimage = ''
    derives, undersize = derive_images(filename)
    for d in derives:
        if splitext(d)[0][-5:] == '_1280':
            large = True
    mdtxt = '\n<figure>'
    if large:
        mdtxt += '\n   <a href="/images/spect/{}" title="click-through for full-size image">'.format(os.path.basename(filename))
    mdtxt += '\n   <img src="/images/spect/alt/{}"'.format(os.path.basename(derives[0]))
    if caption != '':
        mdtxt += '\n        alt="{}"'.format(caption)
    if len(derives) > 0:
        mdtxt += '\n        srcset="'
        for idx, d in enumerate(derives):
            if idx > 0:
                mdtxt += '\n                '
            elif undersize != '':
                mdtxt += '/images/spect/{} {}w,'.format(os.path.basename(filename), undersize)
                mdtxt += '\n                '
            width = splitext(d)[0][-5:].split('_')[1]
            mdtxt += '/images/spect/alt/{} {}w'.format(d, width)
            if idx < len(derives)-1:
                mdtxt += ','
            if idx == 0:
                ogimage = r'http://jeffgerhard.com/images/spect/alt/' + d
        mdtxt += '"'
        mdtxt += '\n        sizes="(max-width: 549px) 100vw, (max-width: 1250px) 620px, 620px"'
# sizes tip via https://css-tricks.com/responsive-images-youre-just-changing-resolutions-use-srcset/
    mdtxt += '>'
    if large:
        mdtxt += '\n   </a>'
    if caption != '':
        mdtxt += '\n   <figcaption>{}</figcaption>'.format(caption)
    mdtxt += '\n</figure>'
    return mdtxt, ogimage

def rename(x, assume=False):
    newname = ''
    print('Current filename is {}'.format(x))
    if not assume:
        if input('Rename this file? [Y to change, ENTER to skip] ').lower() != 'y':
            return x
    newname = input('give this image a name! ')
    print('Ok. If {} is cool just hit enter'.format(newname))
    if input('but hit [C] to edit').lower() == 'c':
        return rename(newname, assume=True)
    return newname

userDir = os.path.expanduser('~')
spectDir = os.path.join(userDir, '.spect')
config = os.path.join(spectDir, 'config.ini')
spectimages = ''
if os.path.isfile(config):
    with open(config, 'r', encoding='utf-8') as fh:
        data = fh.read()
        j = json.loads(data)
        spectimages = os.path.join(j['localdir'], 'images', 'spect')
        os.makedirs(spectimages, exist_ok=True)
        alt = os.path.join(spectimages, 'alt')
        os.makedirs(alt, exist_ok=True)
else:
    print('config file is missing!\n\nERRORS ARE LIKELY\n')


# figure out how to have switches for image, video
if __name__ == "__main__":
    image = askopenfilename(title='choose an image to derive and generate a figure set')
    newname = rename(splitext(os.path.basename(image))[0])
    if spectimages != '':
        if newname == '':
            revised = slugify(splitext(os.path.basename(image))[0], max_length=38,
                              stopwords=['the', 'a', 'an'], save_order=True)
        else:
            revised = slugify(newname, max_length=38,
                              stopwords=['the', 'a', 'an'], save_order=True)
        revised += splitext(os.path.basename(image))[1]
        copiedfile = os.path.join(spectimages, revised.lower())
        if os.path.isfile(copiedfile):
            print('\n\nALERT! A file with this name already exists!!!!')
            query = input('[O]verwrite, [R]ename, or [Q]uit? ').lower()
            # LATER -- ADD AUTORENAME OPTION
            if query == 'o':
                pass
            elif query == 'r':
                newname = rename(revised.lower(), assume=True)
                copiedfile = os.path.join(spectimages, newname.lower())
                copiedfile += splitext(os.path.basename(image))[1].lower()
            elif query == 'q':
                raise ValueError('Program halted -- check filenames!')
# THIS IS RUDIMENTARY -- NEED TO UPDATE IT LATER TO KEEP CHECKING
        copyfile(image, copiedfile)
        image = copiedfile
    caption = input('Enter a caption (optionally): ')
    md, ogimage = generate_img_html(image, caption=caption)
    print(md)
    print(ogimage)

