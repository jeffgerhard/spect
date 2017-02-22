# Development roadmap
## PHASE ONE

development phase 1: just generate some html files in a directory structure of index.html files 
### somewhat complete steps:
- generate html pages, tag pages, category pages
- basic uploading functionality with winscp
- sitevars and config files [cleanup in progress]
- flesh out config/admin a little more. need to name the folder structures here
- clean up text content like footer text
- category (and overall blog) descriptions [moved into admin/sitevars]
- list categories and tags and show frequency (also have tags/ and categories/ pages to list all)
- basic sitemap generation

### last steps left to complete in phase 1:
- remove my personal site-specific stuff (mostly done but not 100%)
- short-term hook to call external tag libraries
- look into making snippets expand into full text / keep this accessible tho
- split out stylesheets (external to spect, really), make diff. categories diff. colors?
- __clean up code__ for redundancy / pythonicness / modularity / theoretically usable by other people
- clean up variable names; look at python best practices
- generate blank index.html files for any exposed folders (admin, scripts, styles)
- reassess deleting outdated directories!
- use tempfile for .spect files (i'm running on a dropbox folder and dbx is occasionally interfering)

## PHASE 2
- start tracking versions and start figuring out git amend commands :)
- add a markdown hook for images, videos, and other stuff
- add 'series' features to link together part 1, part 2, etc.
- add 'published' status so that if i ever change the title, the URL will not change
- begin to think through workflow like 'hey this seems to be a new post! publish?' and then auto-upload
- also, work on 'date modified' type of metadata in case of revisions
- and using full datestamps when applicable [imported data already has it]
- begin to figure out how to modularize external sections of the site, e.g., archives
- work on "front page" of website
- reassess google web fonts (though ultimately this design level stuff will not be part of spect)
- registry of all pages and sections that are not in blog so that i can update them en masse
- more head metadata / opengraph stuff maybe __[partly complete]__
- schema.org stuff like 'blogposting' -- possibly in json-ld __[partly complete]__
- http://humanstxt.org/
- https://indieweb.org/IndieAuth
- more complicated templates like for my "harmonies" category
- related posts, recent posts, prev/next links if desired
- enumerate results pages; do more results (eg date/month)
- more tumblr-type features (incl. youtubes and whatnot; embedding my own vids / gif-ify vids)
- shrinkify most images and make them click-thru to full size __[partly complete]__
- generate rss feed(s)
- auto-post to twitter and then link to or embed in the pages (probably i'll add a 'twitter' tag to the markdowns)
- more robust BACKUP features [stash it all on server?] --- requires a bit of thinking because i don't want duplicate copies of image files all over the place
- better separation of content, presentation, and program
- maybe slip in images for tag main pages (like, if in the folder)
- tag synonyms
- html validation?
- rsync for windows?
- sass integration, css minification
- sitemap pings

## PHASE 3
- a separate script to easily generate new .md files including dates, sections, etc. NB this part can resolve publication date issues
- incorporate some kind of spellcheck and can stash a user dictionary on the server. see https://pythonhosted.org/pyenchant/tutorial.html
- look into other upload solutions for mac/linux (they should be pretty straightforward)
- look at other social media apis --- facebook, diaspora*, google+, mastodon
- link checking and analysis
- link archiving??
- tag suggestions????
- markdown plugin to simplify code?
- API for use of my data?

## PHASE 4
think about .htaccess and redirects; also 404s and all that
- search functionality? [seems dumb / can use google / but maybe worth learning]
- maybe do webmentions? https://webmention.net/implementations/
- consider implementing comments. see https://github.com/jimpick/lambda-comments
- look into replacing some of the dependencies with more appropriate code?
- consider python2 compliance
- error checking / debugging
- tag hierarchies / RDF style? VIAF? subject headings? --- this is kinda silly but an interesting idea and would be good for highlighting related posts
- python standards for file arrangement, etc.
	
## PHASE 5
- look into moving this joint onto the web? django/flask?
- plugin/hook system?