# -*- coding: utf-8 -*-
"""
Created August-October 2016
@author: github.com/jeffgerhard or @jeffgerhard

spect is a static site generator customized to my own needs, in active development.

"""

import markdown as m
import os
from slugify import slugify
from dateutil.parser import parse
from spect_config import j, admin
import shutil
import filecmp
import json
from smartypants import smartypants as smp
from spect_utils import get_immediate_subdirectories


def cleanDate2(x):
    ''' return text date and then a yyyy-mm-dd date '''
    d = parse(x)
    cleandate = '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())
    return cleandate, str(d.date())


def get_files(ext, path, directory):
    a_dir = os.path.join(path, directory)
    y = -(len(ext))
    return [name for name in os.listdir(a_dir)
            if name[y:] == ext]


def keywords(f, s):
    h = os.path.join(mddir, s, f)
    with open(h, mode='r', encoding='utf-8') as z:
        t = z.read()
    text = md.convert(t)
    k = md.Meta
    k['snipped'], k['snippet'] = snipp(t)
    k['section'] = [s]
    k['slug'] = [cleanDate2(k['date'][0])[1] + '--']
    if 'title' in k:
        k['slug'] += slugify(
            k['title'][0], max_length=28,
            stopwords=['the', 'a', 'an'], word_boundary=True, save_order=True
            )
    return text, k


def buildHTML(k, depth=('../', '../')):
    htm = head(k)
    htm += '<body>'
    htm += header()
    htm += '''
    <main class="container">
        <article>
            <header class="row">
'''
    if 'date' in k:
        htm += '                <p class="date">{} | '.format(k['text_date'])
    htm += '<a href="{}{}" class="category-name">{}</a></p>'.format(depth[0],k['section'], str(k['section']).upper())
    if 'title' in k:
        htm += '''
                <h1>{}</h1>
'''.format(k['title_md'])
    if 'summary' in k:
        htm += '''                <p class="summary">{}</p>
'''.format(str(k['summary_md']))
    htm += '''            </header>
            <div class="row">
            <div class="article-content eight columns">

'''
    gist = md.convert(k['text'])
    g = gist.splitlines(keepends=True)
    for a in g:
        if not a == '\n':
            htm += '\t\t\t' + a
    htm += '''


            </div>
            <footer class="four columns" id="post_details">
'''
    if 'date' in k:
        htm += '''                <p>Published <time datetime="{}">{}</time> in
                                  category <a class="category-name"
                                  href="{}{}">{}</a>.</p>
'''.format(k['yyyy-mm-dd'], k['text_date'], depth[0], k['section'],
           k['section'])
    htm += '''                <p>If you would like to comment, please do so
                over on Twitter, where this post was simulposted
                <a href="//twitter.com/something">here</a>.</p>
'''
    if 'tags' in k:
        htm += '''                <p class="taglist"><em>Tagged as:</em> '''
        for tag in k['tags']:
            taglink = '{}tags/'.format(depth[0]) + slugify(tag)
            htm += '<a href="{}" class="taglink" rel="tag">{}</a> '.format(taglink, tag)
        htm += '</p>'
    htm += '''
            </footer></div>
        </article>
    </main>
'''
    htm += sidebar(**k)
    htm += footer(**k)
    htm += '''</body>
</html>'''
    return htm


def head(k, depth=('../','../../')):
    htm = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>'''
    # NEED TO FIX ALL THE BELOW WITH A TITLE STRING WHEN CALLED
    if 'title' in k:
        htm += str(k['title'])
    if 'section' in k:
        htm += ' :: ' + k['section']
    htm += ' :: ' + blogtitle + ' :: &mdash; jeffgerhard.com &mdash;'
    htm += '</title>'
    scz = ['scripts']
    if 'scripts' in k:
        for s in k['scripts']:
            scz.append(s)
    for sc in scz:
        htm += '''
    <script src="{}scripts/{}.js"></script>'''.format(depth[0], sc)
    htm += '''
    <link rel="stylesheet" href=
    "//fonts.googleapis.com/css?family=Bitter%7CIceland%7CSource+Sans+Pro">'''
    stz = ['normalize', 'skeleton', 'style']
    if 'styles' in k:
        for s in k['styles']:
            stz.append(s)
    for st in stz:
        htm += '''
    <link rel="stylesheet" href="{}styles/{}.css">'''.format(depth[0], st)
    htm += '''
    <link rel="icon" type="image/x-icon" href="{}favicon.ico">
    <meta name="generator" content="https://github.com/jeffgerhard/spect">
</head>
'''.format(depth[0])
    return htm


def header(depth=('../', '../../'), **k):
    htm = '''
    <header id="topbar" class="container">
        <div id="navigator">
            <nav><a href="/">jeffgerhard.com</a></nav>
            <nav><a href="{}">{} (blog)</a></nav>
        </div>'''.format(depth[0], blogtitle)
    htm += '''
        <h1>'''
    htm += blogtitle  # give this some thought
    htm += '''</h1>
    </header>
'''
    return htm


def footer(**kwargs):
    htm = '''
    <footer id="bottombar">
        <div class="container">
            <p>Except as noted, all content here is by <a
            href="/" rel="author">Jeff Gerhard</a>. @jeffgerhard. introspect 
            [at] jeffgerhard.com</p>
            <p>More info about this website <a href="/about">here</a>.</p>
        </div>
    </footer>
'''
    return htm


def sidebar(**kwargs):
    htm = '''
<!--    <aside>
        consider a sidebar (on widescreen only) with links to social media postings, etc. listening now. that kinda jazz. can easily cut this though.
    </aside> -->
'''
    return htm


def snipp(f, limit=1000):
    ''' return T/F of whether snipped, and markdown-style snippet of the text content; adapted from
    http://rabexc.org/posts/html-snippets-in-python '''
    snippet = []
    txt = []
    count = 0
    blank = 0
    lines = f.splitlines()
    # let's break out the meta at top
    for line in lines:
        if blank > 0:
            txt.append(line)
        if line == '':
            blank += 1
    if len(''.join(txt)) < limit:
        return False, '\n'.join(txt)
    for line in txt:
        snippet.append(line)
        count += len(line)
        if count >= limit:
            snippet.append('')
            snippet.append('**[ ... ]**')     
            break
    return True, '\n'.join(snippet)


def buildResultsPage(f, l, result_type, depth=('../','../../')):
    ''' f functions as a title, l is the list of results, result_type
    is a string to use to explain the results (for example, 'in category'),
    default depth is for the category pages'''
    k['title'] = '[' + f.upper() + ']'  # sometime i will fix this awkward bit
    tagcount = str(len(l)) + ' post'
    if len(l) > 1:
        tagcount += 's'
    htm = head(k, depth=depth)
    htm += '''<body>
'''
    htm += header(depth=depth)
    # I WOULD LIKE TO ADD CATEGORY DESCRIPTIONS TO THE SITE METADATA
    htm += '''    <main class="container">
        <p class="headertext">{} {}:</p>
        <h1>[{}]</h1>'''.format(tagcount, result_type, f.upper())
    # LATER WILL ADD PAGING FUNCTIONALITY (LIKE, DISPLAY RESULTS 1-20, 21-40?)
    for line in sorted(l, key=lambda k: k['yyyy-mm-dd'], reverse=True):
        if result_type == 'in category':
            insec = ''
        else:
            insec = ' in category <a class="category-name" href="{}{}">{}</a>'.format(depth[0], line['section'], line['section'])
        htm += '''
        <article class="post_link">
            '''
        if 'title' in line:
            htm += '''<p class="date"><time datetime="{}">{}</time>{}</p>
            <h2><a href="{}{}">{}</a></h2>
'''.format(line['yyyy-mm-dd'], line['text_date'], insec, depth[0],
           line['slug'], line['title_md'])
        else:
            htm += '''
                <p class="date"><a href="{}{}" title="permalink">{}</a>{}</p>
'''.format(depth[0], line['slug'], line['text_date'], insec)
        if 'summary' in line:
            htm += '''
            <p class="summary">{}</p>'''.format(line['summary_md'])
        htm += '''
            <div class="snippet">
'''
        snippet = m.markdown(line['snippet'], extensions=['smarty'])
        g = snippet.splitlines(keepends=True)
        repls = [['h4>', 'h6>'], ['h3>', 'h5>'], ['h2>', 'h4>'],
                 ['h1>', 'h3>']]
        # fix urls in the snippets and adjust headings (h1 --> h3 etc.)
        for a in g:
            for x, y in (repls):
                a = a.replace(x, y)
            if not a == '\n':
                htm += '\t\t\t\t' + a.replace('../', depth[0])
        htm += '''
            </div>
        </article>
'''
    htm += '        </main>'
    htm += footer(**k)
    htm += '''
</body>
</html>'''
    return htm


#######################################################
#
# DEFINE SOME SYSTEM VARIABLES
#
#
md = m.Markdown(extensions=['meta', 'smarty'])
# think about how to make the local md files add to the extension list
localdir = j['localdir']
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
admindir = os.path.join(wdir, 'admin')
tagdir = os.path.join(admindir, 'tags')
tagwebdir = os.path.join(wdir, 'tags')
# tag_trackers = ['date', 'title', 'path', 'summary']
blogtitle = admin['blogtitle']
secs = get_immediate_subdirectories(mddir)
for s in secs:
    os.makedirs(os.path.join(wdir, s), exist_ok=True)
os.makedirs(admindir, exist_ok=True)
########################################################
#
# HERE ARE TAG DIRECTORIES. WE'LL DELETE THE OLD ONES AND
# JUST DO THESE FROM SCRATCH
#
# - wait why again? not that big a deal but this list will grow big over time
#if os.path.exists(tagdir):
#    shutil.rmtree(tagdir)
if os.path.exists(tagwebdir):
    shutil.rmtree(tagwebdir)
# os.makedirs(tagdir)
os.makedirs(tagwebdir)
#######################################################
# OK IT'S TIME TO DO THIS
#
# let's assemble the whole dang site into a dictionary
#
all_site_meta = []
for s in secs:
    files = get_files('md', mddir, s)
    for f in files:
        text, k = keywords(f, s)
        k['text'] = text
        k['file'] = f
        k['path'] = s
        k['slug'] = ''
        if 'date' in k:
            k['date'] = k['date'][0]
            k['text_date'], k['yyyy-mm-dd'] = cleanDate2(k['date'])
            k['slug'] += k['yyyy-mm-dd'] + '--'
        else:
            pass  # later, apply some from file metadata?
        if 'section' not in s:
            k['section'] = s
        if 'title' in k:
            k['slug'] += slugify(
                k['title'][0], max_length=28,
                stopwords=['the', 'a', 'an'], word_boundary=True,
                save_order=True)
            k['title_md'] = smp(k['title'][0])
        elif 'spumblr_key' in k:
            k['slug'] = k['spumblr_key'][0]
        else:
            k['slug'] += 'untitled'
            k['title'] = 'untitled'  # later, grab file name as title
        if 'summary' in k:
            k['summary_md'] = smp(k['summary'][0])
        for mk in ['section', 'summary', 'date', 'title']:
            if mk in k:
                if len(k[mk]) == 1:
                    k[mk] = k[mk][0]
        all_site_meta.append(k)
# print(json.dumps(all_site_meta, indent=2, sort_keys=True))
# LATER I MIGHT WANT TO SAVE THIS IN AN ADMIN FOLDER, BACK IT
# UP TO SERVER, AND COMPARE ON REBUILD
#############################################################
# COOL! NOW WE'LL COMPILE TAG INFO TO BUILD TAG PAGES

tagdict = {}  # there is probably a better way to do this, but i'm just
#               reconstructing the site data to group by tag
for s in secs:
    files = get_files('md', mddir, s)
    for f in files:
        k = [x for x in all_site_meta if x['section'] == s and x['file'] == f][0]
        if 'tags' in k:
            for tag in k['tags']:
                tag = tag.lower()
                if tag not in tagdict:
                    tagdict[tag] = []
                tagdict[tag].append(k)
# then making .spect files for them [will transform these later to html]
for t in tagdict:
    thtmlpath = os.path.join(tagwebdir, slugify(t))
    os.makedirs(thtmlpath, exist_ok=True)
    taghtmls = buildResultsPage(t, tagdict[t], 'tagged with',
                                depth=('../../', '../'))
#    taghtmls = buildTagPage(t, tagdict[t])
    tagfile = os.path.join(thtmlpath, 'index.spect')
    with open(tagfile, 'w') as fh:
        fh.write(taghtmls)

#################################################################
# here is the main routine to build html files
#################################################################

for f in all_site_meta:
    htm = buildHTML(f)
    pagedir = os.path.join(wdir, f['slug'])
    if not os.path.exists(pagedir):
        os.makedirs(pagedir)
    htmlfile = os.path.join(pagedir, 'index.spect')
    with open(htmlfile, 'w') as fh:
        fh.write(htm)

# let's also make the main category pages
catpages = dict()  # basically the same technique as the tag pages...
for s in secs:
    catpages[s] = []
    catpages[s] += [l for l in all_site_meta if l['section'] == s]
for s in secs:
    chtmls = buildResultsPage(s, catpages[s], 'in category')
#    chtmls = buildCatPage(s, catpages[s])
    catpage = os.path.join(wdir, s, 'index.html')  # is there a reason not to make them as spect?
    with open(catpage, 'w') as fh:
        fh.write(chtmls)
##########################################################
# now the actual main page should be relatively easy (?)
#
frontpage = buildResultsPage(blogtitle, all_site_meta, 'in this blog',
                             depth=('', '../../'))
with open(os.path.join(wdir, 'index.html'), 'w') as fh:
    fh.write(frontpage)
# gotta look at the depth next!


##########################################################
# then i want to run thru and compare 'n' delete files
def compare_spect(folders, path):
    for f in folders:
        ind = os.path.join(path, f, 'index.html')
        spct = os.path.join(path, f, 'index.spect')
        if os.path.exists(ind):
            # compare files and delete one
            if os.path.exists(spct):
                if filecmp.cmp(ind, spct):
                    os.remove(spct)
                else:
                    os.remove(ind)
                    os.rename(spct, ind)
#            else:  # no .spect file so delete this whole dir
#                shutil.rmtree(os.path.join(wdir, s, sub))
# **** ALERT: NEED TO COME BACK TO THIS!!!!! ****
        elif os.path.exists(spct):
                os.rename(spct, ind)
wsecs = get_immediate_subdirectories(wdir)
compare_spect(wsecs, wdir)
for s in wsecs:
    subsecs = get_immediate_subdirectories(os.path.join(wdir, s))
    compare_spect(subsecs, os.path.join(wdir, s))
#    for sub in subsecs:
#        ind = os.path.join(wdir, s, sub, 'index.html')
#        spct = os.path.join(wdir, s, sub, 'index.spect')
#        if os.path.exists(ind):
#            # compare files and delete one
#            if os.path.exists(spct):
#                if filecmp.cmp(ind, spct):
#                    os.remove(spct)
#                else:
#                    os.remove(ind)
#                    os.rename(spct, ind)
#            else:  # no .spect file so delete this whole dir
#                shutil.rmtree(os.path.join(wdir, s, sub))
#        else:  # no index file so just use the spct
#            os.rename(spct, ind)