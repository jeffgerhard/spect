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
from spect_config import j, admin  # may move this around a bit soon
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
    k['source'] = 'Introspect'
#    k['slug'] = [cleanDate2(k['date'][0])[1] + '--']
#    if 'title' in k:
#        k['slug'] += slugify(
#            k['title'][0], max_length=28,
#            stopwords=['the', 'a', 'an'], word_boundary=True, save_order=True
#            )
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
    htm += '<a href="{}{}/" class="category-name">{}</a></p>'.format(depth[0],k['section'], str(k['section']).upper())
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
                category <a class="category-name" href="{}{}/">{}</a>.
'''.format(k['yyyy-mm-dd'], k['text_date'], depth[0], k['section'],
           k['section'])
    if 'tags' in k:
        htm += '''                <em>Tagged as:</em> <span class="lynx">'''
        for tag in k['tags']:
            taglink = '/tags/' + slugify(tag)
            htm += '''
                  <a href="{}/" class="taglink" rel="tag">{}</a> '''.format(taglink, tag)
        htm += '</span>'
    htm += '''
                </p>'''
    if 'twitter' in k:
        htm += '''
                <p>If you would like to comment, please do so
                over on Twitter, where this post was simulposted
                <a href="{}">here</a>.</p>
'''.format(k['twitter'][0])
    if len(catpages[k['section']])>1:
        htm += '''
                <p>Latest posts in <a class="category-name" href="{}{}/">{}</a>:</p> 
                    <ul>
'''.format(depth[0], k['section'], k['section'].upper())
        for x in sorted(catpages[k['section']], 
                        key=lambda y: y['yyyy-mm-dd'], reverse=True)[0:2]:
            htm += '''                      <li><span class="list_date"><em>{}</em></span>
                      <br><a'''.format(x['text_date'])
            if 'summary' in x:
                htm += ''' title="{}"
                      '''.format(x['summary'])
            htm += ''' href="{}{}/">'''.format(depth[0],x['slug'])
            if 'title' in x:
                htm += x['title_md']
            else:
                htm += '[untitled post]'
            htm += '''</a></li>
'''
        htm += '                    </ul>'
    htm += '''
                <p><em>Most frequent tags:</em> <span class="lynx">                         
'''
    for x in dictSort(tagdict)[0:3]:  # LATER I WILL UP THIS NUMBER WHEN I HAVE CONTENT!
        htm += '''                <a href="/tags/{}/" rel="tag">{}</a>
'''.format(slugify(x[0]), x[0])
    htm += '''                <a href="/tags/">[see all tags&hellip;]</a></span></p>
'''.format(depth[0])
    htm += '''            </footer>
            </div>
        </article>
    </main>
'''
    htm += sidebar(**k)
    htm += footer(**k)
    htm += '''</body>
</html>'''
    return htm


def head(k, depth=('../','../'), **kw):
    htm = '''<!DOCTYPE html>
<html lang="en">
'''
    if 'introspect' in k:
        htm += '<head prefix="og: http://ogp.me/ns# article: http://ogp.me/ns/article#">'
    else:
        htm += '<head>'
    htm+='''
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>'''
    # NEED TO FIX ALL THE BELOW WITH A TITLE STRING WHEN CALLED
    if 'htmltitle' in k:
        htm += k['htmltitle']
    htm += '</title>'
    if 'introspect' in k:
        kanonical = r'http://jeffgerhard.com/blog/' + k['slug'] + r'/'
        htm += '''
    <link rel="canonical" href="{}">'''.format(kanonical)
        if 'summary' in k:
            htm += '''
    <meta property="og:description" content="{}">'''.format(k['summary_md'])
        htm += '''
    <meta property="og:title" content="{}">
    <meta property="og:url" content="{}">
    <meta property="og:site_name" content="Introspect">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:creator" content="@JeffGerhard">
    <meta property="article:author" content="http://jeffgerhard.com/">
    <meta property="article:published_time" content="{}">
'''.format(k['title_md'], kanonical, k['yyyy-mm-dd'])
    scz = ['scripts']
    if 'scripts' in k:
        for s in k['scripts']:
            scz.append(s)
    for sc in scz:
        htm += '''
    <script src="{}scripts/{}.js"></script>'''.format(depth[1], sc)
    htm += '''
    <link rel="stylesheet" href=
    "//fonts.googleapis.com/css?family=Bitter%7CIceland%7CSource+Sans+Pro">'''
    stz = ['normalize', 'skeleton', 'style']
    if 'section' in k:
        stz.append(k['section'])
    if 'styles' in k:
        for s in k['styles']:
            stz.append(s)
    for st in stz:
        htm += '''
    <link rel="stylesheet" href="{}styles/{}.css">'''.format(depth[1], st)
    htm += '''
    <link rel="icon" type="image/x-icon" href="{}favicon.ico">
    <meta name="generator" content="https://github.com/jeffgerhard/spect">
</head>
'''.format(depth[1])
    return htm


def header(depth=('../', '../../'), **k):
    if 'headtitle' not in k:
        k['headtitle'] = blogtitle
    htm = '''
    <header id="topbar" class="container">
        <div id="navigator">
            <nav><a href="/">jeffgerhard.com</a></nav>
            <nav><a href="{}">{} (blog)</a></nav>
        </div>'''.format(depth[0], k['headtitle'])
    htm += '''
        <h1>'''
    htm += k['headtitle']  # give this some thought
    htm += '''</h1>
    </header>
'''
    return htm


def footer(**kwargs):
    htm = '''
    <footer id="bottombar">
        <div class="container">
            <p>Except as noted, all content here is by <a
            href="/" rel="author">Jeff Gerhard</a>. @jeffgerhard. jeff 
            [at] jeffgerhard.com</p>
            <p>More info about this website <a href="/about/">here</a>.</p>
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


def buildResultsPage(f, l, result_type, desc, depth=('../','../')):
    ''' f functions as a title, l is the list of results, result_type
    is a string to use to explain the results (for example, 'in category'),
    default depth is for the category pages'''
    zzz = dict()
    kw = dict()
    zzz['htmltitle'] = f.upper()
    if result_type == 'tagged with':
        zzz['htmltitle'] += ' tag results'
        zzz['styles'] = ['tags']
    zzz['htmltitle'] += ' &mdash; jeffgerhard.com'  # sometime i will fix this awkward bit
    tagcount = str(len(l)) + ' post'
    if len(l) > 1:
        tagcount += 's'
    if result_type == 'in category':
        zzz['section'] = f
    htm = head(zzz, depth=depth)
    htm += '''<body>
'''
    if result_type == 'tagged with':
        kw['headtitle'] = 'site tags'
        htm += '''
    <header id="topbar" class="container">
        <div id="navigator">
            <nav><a href="/">jeffgerhard.com</a></nav>
            <nav><a href="../">site tags</a></nav>
        </div>
        <h1>site tags</h1>
    </header>
'''
    else:
        htm += header()
    htm += '''    <main class="container">
        <p class="headertext">{} {}:</p>
        <h1>[{}]</h1>'''.format(tagcount, result_type, f.upper())
    if desc != '':
        htm += '        <p class="description">{}</p>'.format(smp(desc))
    # LATER WILL ADD PAGING FUNCTIONALITY (LIKE, DISPLAY RESULTS 1-20, 21-40?)
    for line in sorted(l, key=lambda k: k['yyyy-mm-dd'], reverse=True):
        if result_type == 'in category':
            insec = ''
        elif result_type == 'tagged with':
            if 'categorylink' in line:
                insec = ''' from <strong>{}</strong> in category <a class="category-name" href="{}">{}</a>
            '''.format(line['source'], line['categorylink'], line['section'])
            else:
                insec = ''' from <strong>{}</strong> in category <a class="category-name" href="{}{}/">{}</a>
            '''.format(line['source'], depth[0], slugify(line['section']), line['section'])
        else:
            insec = ' in category <a class="category-name" href="{}{}/">{}</a>'.format(depth[0], slugify(line['section']), line['section'])
        htm += '''
        <article class="post_link">
            '''
        if 'canonical' in line:
            htm += '''<p class="date"><time datetime="{}">{}</time>{}</p>
            <h2><a href="{}">{}</a></h2>
'''.format(line['yyyy-mm-dd'], line['text_date'], insec,
           line['canonical'], line['title'])
        elif 'title' in line:
            htm += '''<p class="date"><time datetime="{}">{}</time>{}</p>
            <h2><a href="{}{}/">{}</a></h2>
'''.format(line['yyyy-mm-dd'], line['text_date'], insec, depth[0],
           line['slug'], line['title_md'])
        else:
            htm += '''
                <p class="date"><a href="{}{}/" title="permalink">{}</a>{}</p>
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

def buildPagePage(k):
    k['htmltitle'] = k['title'] + ' &mdash; jeffgerhard.com'  # sometime i will fix this awkward bit
    htm = head(k, depth=k['depth'])
    htm += '''<body>
    <header id="topbar" class="container">
        <div id="navigator">
            <nav><a href="/">jeffgerhard.com</a></nav>
            <nav><a href="{}{}">{}</a></nav>
        </div>
        <h1>{}</h1>
    </header>
    <main class="container">
'''.format(k['depth'][0], k['slug'], k['title'], k['title'].upper())
    # LATER WILL ADD PAGING FUNCTIONALITY (LIKE, DISPLAY RESULTS 1-20, 21-40?)
    if 'summary' in k:
        htm += '    <div class="summary">{}</div>'.format(k['summary'])
    htm += k['text']
    htm += '        </main>'
    htm += footer(**k)
    htm += '''
</body>
</html>'''
    return htm


def dictSort(y):
    results = []
    for x in sorted(y.keys(), key=lambda x: len(y[x]), 
                    reverse=True):
        results.append([x, len(y[x])])
    return results

#######################################################
# 
# FOR RN I AM HARD CODING SOME ADDED STUFF TO INTEGRATE
# THIS WITH MY SITE;
# STARTING WITH EXTERNAL TAG JSON FILES!
with open(r'C:\Users\J\Dropbox\__websites\jeffgerhard.com\archives\monodrone.org\monodrone_tagdict.json', 'r', encoding='utf-8') as fh:
    monodrone_tagdict = json.loads(fh.read())

    
#######################################################
#
# DEFINE SOME SYSTEM VARIABLES
#
#
md = m.Markdown(extensions=['meta', 'smarty'])
# think about how to make the local md files add to the extension list
admindir, localdir, mddir, tagwebdir, wdir = [j.get(k) for k in ['admindir', 'localdir', 'mddir', 'tagwebdir', 'wdir']]
#localdir = j['localdir']
#mddir = os.path.join(localdir, 'md')
#wdir = os.path.join(localdir, 'www')
#admindir = os.path.join(wdir, 'admin')
#tagdir = os.path.join(admindir, 'tags')
#tagwebdir = os.path.join(wdir, 'tags')
# tag_trackers = ['date', 'title', 'path', 'summary']
blogtitle = admin['blogtitle']
secs = get_immediate_subdirectories(mddir)
#secs = admin['secs']
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
        k['introspect'] = 'post'
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
            k['htmltitle'] = k['title'][0] + ' (' + k['text_date'] + ')'
        elif 'spumblr_key' in k:
            k['slug'] = k['spumblr_key'][0]
            k['htmltitle'] = '[untitled post, ' + k['text_date'] + ']'
            k['title_md'] = k['htmltitle']
        else:
            k['slug'] += 'untitled'
            k['htmltitle'] = '[untitled post]'
            k['title'] = 'untitled'  # later, grab file name as title
        k['htmltitle'] += ' &mdash; ' + blogtitle + ' (' + k['section'] +')' 
        if 'summary' in k:
            k['summary_md'] = smp(k['summary'][0])
        for mk in ['section', 'summary', 'date', 'title']:
            if mk in k:
                if len(k[mk]) == 1:
                    k[mk] = k[mk][0]
        all_site_meta.append(k)
#print(json.dumps(all_site_meta, indent=2, sort_keys=True))
# LATER I MIGHT WANT TO SAVE THIS IN AN ADMIN FOLDER, BACK IT
# UP TO SERVER, AND COMPARE ON REBUILD
#############################################################
# COOL! NOW WE'LL COMPILE TAG INFO

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

# let's also make the main category pages
catpages = dict()  # basically the same technique as the tag pages...
for s in secs:
    catpages[s] = []
    desc = ''
    catpages[s] += [l for l in all_site_meta if l['section'] == s]
for s in secs:
    if 'categories' in admin:
        for c in admin['categories']:
            if c['category'] == s:
                desc = c['description']
    chtmls = buildResultsPage(s, catpages[s], 'in category', desc)
#    chtmls = buildCatPage(s, catpages[s])
    catpage = os.path.join(wdir, s, 'index.html')  # is there a reason not to make them as spect?
    with open(catpage, 'w') as fh:
        fh.write(chtmls)

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

##########################################################
# now the actual main page should be relatively easy (?)
#
desc = ''
if 'blogdescription' in admin:
    desc = admin['blogdescription']
frontpage = buildResultsPage(blogtitle, all_site_meta, 'in this blog', desc,
                             depth=('', '/blog/'))
with open(os.path.join(wdir, 'index.html'), 'w') as fh:
    fh.write(frontpage)

##########################################################
# DO TAGS PAGES LAST

# now lemme try to merge dictionaries.. ugh......
for t in tagdict:
    if t in monodrone_tagdict:
        tagdict[t] += monodrone_tagdict[t]
mergedtags = {**monodrone_tagdict, **tagdict}
# then making .spect files for them [will transform these later to html]
for t in mergedtags:
    thtmlpath = os.path.join(tagwebdir, slugify(t))
    os.makedirs(thtmlpath, exist_ok=True)
    taghtmls = buildResultsPage(t, mergedtags[t], 'tagged with', '',
                                depth=('../../blog/', '../../blog/')) # TROUBLE BUT EHHH
#    taghtmls = buildTagPage(t, tagdict[t])
    tagfile = os.path.join(thtmlpath, 'index.spect')
    with open(tagfile, 'w', encoding='utf-8') as fh:
        fh.write(taghtmls)
##########################################################
# howzabout doing a tag table for the tag main page?
tagtable = '''

    <table class="sortable">
        <tr>
            <th>Tag</th>
            <th>Count</th>
        </tr>
'''
# come back the below and think about secondary sort on title or something
for t in sorted(mergedtags, key=lambda t: len(mergedtags[t]), reverse=True):
    tagtable += '''        <tr>
            <td><a href="{}/">{}</a></td>
            <td>{}</td>
        </tr>
'''.format(slugify(t), t, len(mergedtags[t]))

tagtable += '''    </table>
'''

# then use that table as the content to build a page???

tablepage = dict()
tablepage['title'] = 'all site tags'
tablepage['scripts'] = ['sorttable']
tablepage['summary'] = '''
        <p>Here is a list of all site tags. Note that this includes a ton of 
        <span style="text-decoration: line-through">useless junk</span> vintage
        content pulled from personal websites and various internet accounts
        dating back over a decade. In the future I will work on adding some filters 
        here.</p>
'''
tablepage['text'] = tagtable
tablepage['styles'] = ['meta', 'tags']
tablepage['depth'] = ('/', '/blog/')
tablepage['slug'] = 'tags'
thetags = buildPagePage(tablepage)
with open(os.path.join(j['tagwebdir'], 'index.html'), 'w') as fh:
    fh.write(thetags)

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
    
wsecs = get_immediate_subdirectories(tagwebdir)
compare_spect(wsecs, tagwebdir)

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
