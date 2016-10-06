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
    if s == 'blog':
        k['section'] = [blogtitle]
    else:
        k['section'] = [s]
    k['slug'] = [yyyy_mm_dd(**k) + '_']
    if 'title' in k:
        k['slug'][0] += slugify(
            k['title'][0], max_length=28,
            stopwords=['the', 'a', 'an'], word_boundary=True, save_order=True
            )
    else:
        k['slug'][0] += 'untitled'
        k['title'][0] = 'untitled'  # later, grab file name as title
    return text, k


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
        htm += '''                <p class="date">{}</p>
'''.format(cleanDate(**k))
    htm += '''                <h1>{}</h1>
'''.format(k['title'][0])
    if 'summary' in k:
        htm += '''                <p class="summary">{}</p>
'''.format(str(k['summary'][0]))
    htm += '''            </header>
            <div class="row">
            <div class="eight columns">

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
                <a href="../../{}">{}</a>.</p>
'''.format(cleanDate(**k), k['section'][0], k['section'][0])
    htm +='''                <p>In lieu of comments, please respond over on
                Twitter, where this post was highlighted
                <a href="//">here</a>.</p>
'''
    if 'tags' in k:
        htm += '''                <p><em>Tagged as:</em></p>
                <ul class="taglist">'''
        for tag in k['tags']:
            taglink = '../../tags/' + slugify(tag)
            htm += '''
                    <li><a href="{}" class="taglink">{}</a></li>'''.format(taglink, tag)
        htm += '''
                </ul>'''
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
    stz = ['normalize', 'skeleton']
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
    <header id="topbar">
        <h1 class="container">'''
    htm += k['section'][0]  # give this some thought
    htm +='''</h1>        
        <div class="container">
            <nav class="one-third column">
                <a href="../../projects">PROFESSIONAL</a>
            </nav>
            <nav class="one-third column">
                <a href="../../blog">PERSONAL</a>
            </nav>
            <nav class="one-third column">
                <a href="../../etc">EPHEMERAL</a>
            </nav>
        </div>
    </header>
'''
    return htm


def footer(**kwargs):
    htm = '''
    <footer id="bottombar">
        <div class="container">
            <p class="one-third column">All content by <a
            href="//jeffgerhard.com">Jeff Gerhard</a>.</p>
            <p class="one-third column">@jeffgerhard</p>
            <p class="one-third column">introspect [at] jeffgerhard.com</p>
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
            insec = 'in ' + line['section']
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
<!-- i guess i should add a footer 'n' sidebar too -->
</body>
</html>    
    '''
    return htm
    # ok this is getting somewhere and is basically the same way i can
    # build the front blog pages, etc.

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
        text, k = keywords(f, s)
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
                new['date'] = yyyy_mm_dd(**k)
                new['title'] = k['title'][0]
                new['path'] = s + '/' + k['slug'][0]
                if 'section' in k:
                    new['section'] = k['section'][0]
                if 'summary' in k:
                    new['summary'] = k['summary'][0]
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
        with open(internalsitemap, 'a') as fh:
            # fh.write('../../' + s + '/' + k['slug'][0] + '/\n')
            fh.write(yyyy_mm_dd(**k) + ',')
            fh.write(k['title'][0] + ',')
            fh.write(s + '/' + k['slug'][0] + '\n')
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