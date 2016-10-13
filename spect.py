# -*- coding: utf-8 -*-
"""
swithing over to json for data storage version!
Created August-September 2016
@author: github.com/jeffgerhard or @jeffgerhard

spect is a static site generator customized to my own needs, in active development.

development phase 1: just generate some html files in a directory structure
of index.html files 

also i need to clean up the configuration of the styles and sections;
    also i need to think about generated pages like front of blog,
    and what wordpress considers 'pages'
    
    md files can be like type: page with default to be blog-type
    
also also i need to consider the organization of the .md files. i think 
    including 'section' should override folder structure. so could just have
    a single .md folder if a user wanted that

phase 2: generate tags pages and similar (like related content);
    generate rss feed and sitemap; note that i need to generate tags 
    pages before the .html pages

phase 3: configure an auto-upload to server [coming along nicely]
    incorporate some kind of spellcheck and can stash a user dictionary
    on the server. see https://pythonhosted.org/pyenchant/tutorial.html
    make it easy to edit the config file or reset it

phase 4: a separate script to easily generate new .md files including
    dates, sections, etc. NB this part can include publication date issues

phase 5: think about .htaccess and redirects; also 404s and all that

consider implementing comments. see https://github.com/jimpick/lambda-comments

"""

import markdown as m
import os
from slugify import slugify
from dateutil.parser import parse
from spect_config import j
import shutil
import filecmp
import json
from smartypants import smartypants as smp


def get_immediate_subdirectories(a_dir):
# stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python#800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def yyyy_mm_dd(**k):
    if 'date' in k:
        d = parse(k['date'][0])
        return str(d.date())
    else:
        return ''


def cleanDate(**k):
    if 'date' in k:
        d = parse(k['date'][0])
        return '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())

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
#    if s == 'blog':
#        k['section'] = [blogtitle]
#    else:
    k['section'] = [s]
    k['slug'] = [yyyy_mm_dd(**k) + '--']
    if 'title' in k:
        k['slug'][0] += slugify(
            k['title'][0], max_length=28,
            stopwords=['the', 'a', 'an'], word_boundary=True, save_order=True
            )
    else:
        k['slug'][0] += 'untitled'
        k['title'][0] = 'untitled'  # later, grab file name as title
    return text, k

def keywords2(f, s):
    h = os.path.join(mddir, s, f)
    with open(h, mode='r', encoding='utf-8') as z:
        t = z.read()
    return md.convert(t) # just return the md text


def buildHTML(text, **k):
    htm = head(**k)
    htm += '<body>'
    htm += header(**k)
    htm += '''
    <main class="container">
        <article>
            <header class="row">
'''
    if 'date' in k:
        htm += '                <p class="date">{} | '.format(cleanDate(**k))
    htm += '<a href="../../{}" class="category-name">{}</a></p>'.format(k['section'][0], k['section'][0].upper())
    htm += '''
                <h1>{}</h1>
'''.format(k['title'][0])
    if 'summary' in k:
        htm += '''                <p class="summary">{}</p>
'''.format(str(k['summary'][0]))
    htm += '''            </header>
            <div class="row">
            <div class="article-content eight columns">

'''
    gist = md.convert(text)
    g = gist.splitlines(keepends=True)
    for a in g:
        if not a == '\n':
            htm += '\t\t\t' + a
    htm += '''


            </div>
            <footer class="four columns" id="post_details">
'''
    if 'date' in k:
        htm += '''                <p>Published {} in category 
                <a class="category-name" href="../../{}">{}</a>.</p>
'''.format(cleanDate(**k), k['section'][0], k['section'][0])
    htm +='''                <p>If you would like to comment, please do so over on
                Twitter, where this post was simulposted
                <a href="//">here</a>.</p>
'''
    if 'tags' in k:
        htm += '''                <p class="taglist"><em>Tagged as:</em> '''
        for tag in k['tags']:
            taglink = '../../tags/' + slugify(tag)
            htm += '<a href="{}" class="taglink">{}</a> '.format(taglink, tag)
        htm += '</p>'
    htm +='''
            </footer></div>
        </article>
    </main>
'''
    htm += sidebar(**k)
    htm += footer(**k)
    htm += '''</body>
</html>'''
    return htm


def head(**kwargs):
    htm = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>'''
    if 'title' in kwargs:
        htm += str(kwargs['title'][0])
    if 'section' in kwargs:
        htm += ' :: ' + kwargs['section'][0]
    else:
        htm += '&mdash; jeffgerhard.com'
    htm += '</title>'
    scz = ['scripts']
    if 'scripts' in kwargs:
        for s in kwargs['scripts']:
            scz.append(s)
    for sc in scz:
        htm += '''
    <script source="../../scripts/{}.js"></script>'''.format(sc)
    htm += '''
    <link rel="stylesheet" href=
    "//fonts.googleapis.com/css?family=Bitter|Iceland|Source+Sans+Pro">'''
    stz = ['normalize', 'skeleton', 'style']
    if 'styles' in kwargs:
        for s in kwargs['styles']:
            stz.append(s)
    for st in stz:
        htm += '''
    <link rel="stylesheet" href="../../styles/{}.css">'''.format(st)
    htm += '''
    <link rel="icon" type="image/x-icon" href="../../favicon.ico">
    <meta name="generator" content="https://github.com/jeffgerhard/spect">
</head>
'''
    return htm


def header(**kwargs):
    htm = '''
    <header id="topbar" class="container">
        <div id ="navigator">
            <nav><a href="//">jeffgerhard.com</a></nav>
            <nav><a href="//">{} (blog)</a></nav>
        </div>'''.format(blogtitle)
    htm += '''
        <h1>'''
    htm += blogtitle  # give this some thought
    htm +='''</h1>        
        <!-- <div>
           <nav class="one-third column">
                <a href="../../projects">PROFESSIONAL</a>
            </nav>
            <nav class="one-third column">
                <a href="../../blog">PERSONAL</a>
            </nav>
            <nav class="one-third column">
                <a href="../../etc">EPHEMERAL</a>
            </nav>
            <nav>
                <a href="../../projects">PROFESSIONAL</a>
            </nav>
            <nav>
                <a href="../../blog">PERSONAL</a>
            </nav>
            <nav>
                <a href="../../etc">EPHEMERAL</a>
            </nav>
        </div> -->
    </header>
'''
    return htm


def footer(**kwargs):
    htm = '''
    <footer id="bottombar">
        <div class="container">
            <p>Except as noted, all content here is by <a
            href="//jeffgerhard.com">Jeff Gerhard</a>. @jeffgerhard. introspect 
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


def buildTagPage(f, l):
    k['title'] = ['[' + f.upper() + ']']
    k['section'] = ['site tags']
    tagcount = str(len(l)) + ' post'
    if len(l)>1:
        tagcount += 's'
    htm = head(**k)
    htm += '''<body>
'''
    htm += header(**k)
    htm +='''    <main class="container">
    <p class="headertext">{} tagged with:</p>
    <h1>[{}]</h1>'''.format(tagcount, f.upper())
    # LATER WILL ADD PAGING FUNCTIONALITY (LIKE, DISPLAY RESULTS 1-20, 21-40?)
    for line in sorted(l, key=lambda k: k['date'], reverse=True):
        d = parse(line['date'])
        cleand = '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())
        if 'section' in line:
            insec = 'in category <a class="category-name" href="../{}">{}</a>'.format(line['section'], line['section'])
        htm +='''
        <section class="post_link">
            <p class="date">{} {}</p>
            <h2><a href="../../{}">{}</a></h2>'''.format(cleand, insec, line['path'], line['title'])
        if 'summary' in line:
            htm += '''
            <p class="summary">{}</p>'''.format(line['summary'])
    htm +='''
        </section>
    </main>
'''
    htm +=footer(**k)
    htm +='''
</body>
</html>    
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
        return False, txt
    for line in txt:
        snippet.append(line)
        count += len(line)
        if count >= limit:
            snippet.append('')
            snippet.append('**[ ... ]**')     
            break
#    for line in txt:
#        if not line.strip() and snippet[-1] and snippet[-1][-1] == ".":
#            break
#        snippet.append(line)
    return True, '\n'.join(snippet)
       

def buildCatPage(f, l):
    k['title'] = ['[' + f.upper() + ']']
    htm = head(**k)
    htm += '''<body>
'''
    htm += header(**k)
    htm +='''    <main class="container">
    <h1>[{}]</h1>'''.format(f.upper())
    # LATER WILL ADD PAGING FUNCTIONALITY (LIKE, DISPLAY RESULTS 1-20, 21-40?)
    for line in sorted(l, key=lambda k: k['yyyy-mm-dd'], reverse=True):
#        d = parse(line['date'])
#        cleand = '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())
#        if 'section' in line:
#            insec = 'in category <a class="category-name" href="../{}">{}</a>'.format(line['section'], line['section'])
        htm +='''
        <section class="post_link">
            <p class="date">{}</p>
            <h2><a href="../{}/{}">{}</a></h2>'''.format(line['text_date'], f, line['slug'], line['title_md'])
        if 'summary' in line:
            htm += '''
            <p class="summary">{}</p>'''.format(line['summary_md'])
    htm +='''
        </section>
    </main>
'''
    htm +=footer(**k)
    htm +='''
</body>
</html>'''
    return htm
    
md = m.Markdown(extensions=['meta', 'smarty'])
# think about how to make the local md files add to the extension list
localdir = j['localdir']
mddir = os.path.join(localdir, 'md')
wdir = os.path.join(localdir, 'www')
admindir = os.path.join(localdir, 'admin')
tagdir = os.path.join(admindir, 'tags')
tagwebdir = os.path.join(wdir, 'tags')
tag_trackers = ['date','title','path','summary']
blogtitle = j['blogtitle']
sitemap_in_mem = []
# first i will do backups of all the wdir files
# update - jk don't really need to do that!
#secs = get_immediate_subdirectories(wdir)
#for s in secs:
#    subsecs = get_immediate_subdirectories(os.path.join(wdir, s))
#    for sub in subsecs:
#        ind = os.path.join(wdir, s, sub, 'index.html')
#        bup = os.path.join(wdir, s, sub, 'index.bak')
#        shutil.copy2(ind, bup)
# then will create spect files
secs = get_immediate_subdirectories(mddir)
internalsitemap = os.path.join(admindir, 'site.txt')
######################################################
# clean up some directories and files before starting;
# should really make sure to build basic directories too!
######################################################
with open(internalsitemap, 'w') as fh:
    fh.write('')  # clear contents of sitemap file
#### honestly probs don't need that anymore
#
#
# in here i need to insert some parsing of the .md files and prepend
# more meta fields (if absent) like:
#   - text_date
#   - yyyy-mm-dd
#   - twitter (eventually)
#   - slug (why not)
# 'twould be nice to just do it in json or another better format
# then i could ditch all these dumb [0] things
#
# for realz what i need to do is parse .md files into memory all in one go
# i am pretty sure it can handle whatever i throw at it including the md.text
#
# and then manipulate the metadata and write it to the .md if needed
# NB if i edit the .md's i should add a modified date to the meta!
#
#
# cool.... let's do it
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
#            k['text_date'] = cleanDate(k['date'])
#            k['yyyy-mm-dd'] = yyyy_mm_dd(**k)
            k['slug'] += k['yyyy-mm-dd'] + '--'
        else:
            pass
            # need to apply some from file metadata
        if not 'section' in s:
            k['section'] = s
        if 'title' in k:
            k['slug'] += slugify(
                k['title'][0], max_length=28,
                stopwords=['the', 'a', 'an'], word_boundary=True, save_order=True
                )
        else:
            k['slug'] += 'untitled'
            k['title'][0] = 'untitled'  # later, grab file name as title
        if 'summary' in k:
            k['summary_md'] = smp(k['summary'][0])
        for mk in ['section','summary','date','title']:
            if mk in k:
                if len(k[mk]) == 1:
                    k[mk] = k[mk][0]
        k['title_md'] = smp(k['title'])
        all_site_meta.append(k)
print(json.dumps(all_site_meta, indent=2, sort_keys=True))
if os.path.exists(tagdir):
    shutil.rmtree(tagdir)
if os.path.exists(tagwebdir):
    shutil.rmtree(tagwebdir)
os.makedirs(tagdir)
os.makedirs(tagwebdir)
# let's try to grab tags for now; later dates? etc?

tagdict = {}
for s in secs:
    files = get_files('md', mddir, s)
    for f in files:
        k = [x for x in all_site_meta if x['section'] == s and x['file'] == f][0]
#        text, k = keywords(f, s)
        if 'tags' in k:
            tags = k['tags']
            for t in tags:
                tagfile = os.path.join(admindir, 'tags', t + '.tmp')
                new = {}
#                with open(tagfile, 'a', encoding='utf-8', newline='') as fh:
#                    writer = csv.DictWriter(fh, fieldnames=tag_trackers, dialect='excel')
#                with open(tagfile, 'w', encoding='utf-8') as fh:
#                    json.dump([], fh)
#                with open(tagfile, 'a', encoding='utf-8') as fh:
                if not t in tagdict:
                    tagdict[t] = []
                new['date'] = k['yyyy-mm-dd']
                new['title'] = k['title']
                new['path'] = s + '/' + k['slug']
                if 'section' in k:
                    new['section'] = k['section']
                if 'summary' in k:
                    new['summary'] = k['summary']
                tagdict[t].append(new)
#                    fh.write(json.dumps(newline, indent=4))
#                    writer.writerow(newline)
# then let's build tag pages for each tag
#files = get_files('tmp', admindir, 'tags')
#taghtmls = {}
#for f in files:
#    fn = os.path.join(tagdir, f)
#    with open(fn, 'r', newline='') as fh:
#        taghtmls = json.loads(fh.read())
#        reader = csv.DictReader(fh, fieldnames=tag_trackers)
        
#        lines = fh.read()
#        l = lines.splitlines()
#        l.sort()
#        taghtmls[f[:-4]] = buildTagPage(f, reader)
# print(json.dumps(tagdict, indent=2))
for t in tagdict:
    thtmlpath = os.path.join(tagwebdir,slugify(t))
    os.makedirs(thtmlpath, exist_ok=True)
#    print(t)
#    print(tagdict[t])
    taghtmls = buildTagPage(t, tagdict[t])
    tagfile = os.path.join(thtmlpath,'index.spect')
    with open(tagfile, 'w') as fh:
        fh.write(taghtmls)
#################################################################
# here is the main routine to build html files
#################################################################
for s in secs:
    files = get_files('md', mddir, s)
    for f in files:
        text, k = keywords(f, s)
        htm = buildHTML(text, **k)
        pagedir = os.path.join(wdir, s, k['slug'][0])
        if not os.path.exists(pagedir):
            os.makedirs(pagedir)
        htmlfile = os.path.join(pagedir, 'index.spect')
        with open(htmlfile, 'w') as fh:
            fh.write(htm)
       # with open(internalsitemap, 'a') as fh:
            # fh.write('../../' + s + '/' + k['slug'][0] + '/\n')
         #   fh.write(json.dumps(k, indent=2, sort_keys=True))

        sitemap_in_mem.append(k)
# let's start making the main category pages
catpages = dict()
for s in secs:
    catpages[s] = []
    catpages[s] += [l for l in all_site_meta if l['section'] == s]
#print(json.dumps(catpages, indent=2))
for s in secs:
    chtmls = buildCatPage(s, catpages[s])
    #print(chtmls)
##########################################################
# then i want to run thru and compare 'n' delete files
secs = get_immediate_subdirectories(wdir)
for s in secs:
    subsecs = get_immediate_subdirectories(os.path.join(wdir, s))
    for sub in subsecs:
        ind = os.path.join(wdir, s, sub, 'index.html')
        # bup = os.path.join(wdir, s, sub, 'index.bak')
        spct = os.path.join(wdir, s, sub, 'index.spect')
        if os.path.exists(ind):
            # compare files and delete one
            if os.path.exists(spct):
                if filecmp.cmp(ind, spct):
                    os.remove(spct)
                else:
                    os.remove(ind)
                    os.rename(spct, ind)
            else:  # no .spect file so delete this whole dir
                shutil.rmtree(os.path.join(wdir, s, sub))
        else:  # no index file so just use the spct
            os.rename(spct, ind)