# Development roadmap
## PHASE ONE

development phase 1: just generate some html files in a directory structure of index.html files 
### somewhat complete steps:
- generate html pages, tag pages, category pages
- basic uploading functionality with winscp
- admin and config files [REALLLLLLY MESSY FOR NOW]

### last steps left to complete in phase 1:
- clean up text content like footer text
- category (and overall blog) descriptions // keep this in an admin folder?
- list categories and tags and show frequency (also have tags/ and categories/ pages to list all)
- look into making snippets expand into full text / keep this accessible tho
- split out stylesheets (external to spect, really), make diff. categories diff. colors?
- clean up code for redundancy / pythonicness / modularity / theoretically usable by other people
- clean up variable names; look at python best practices
- generate blank index.html files for any exposed folders (admin, scripts, styles)

## PHASE 2
- more head metadata / opengraph stuff maybe
- http://humanstxt.org/
- https://indieweb.org/IndieAuth
- more complicated templates like for my "harmonies" category
- related posts, recent posts, prev/next links if desired
- enumerate results pages; do more results (eg date/month)
- more tumblr-type features (incl. youtubes and whatnot; embedding my own vids / gif-ify vids)
- shrinkify all images and make them click-thru to full size
- generate rss feed and sitemap
- auto-post to twitter and then link to or embed in the pages (probably i'll add a 'twitter' tag to the markdowns)
- more robust backup features [stash it all on server?]
- better separation of content, presentation, and program
- maybe slip in images for tag main pages (like, if in the folder

## PHASE 3
- a separate script to easily generate new .md files including dates, sections, etc. NB this part can resolve publication date issues
- incorporate some kind of spellcheck and can stash a user dictionary on the server. see https://pythonhosted.org/pyenchant/tutorial.html
- look into other upload solutions for mac/linux (they should be pretty straightforward)
- look at other social media apis like the ole f book and maybe g+

## PHASE 4
think about .htaccess and redirects; also 404s and all that
- search functionality? [seems dumb / can use google / but maybe worth learning]
- maybe do webmentions? https://webmention.net/implementations/
- consider implementing comments. see https://github.com/jimpick/lambda-comments
	
## PHASE 5
- look into moving this joint onto the web? django/flask?