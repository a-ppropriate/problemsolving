# problemsolving
### Intro
A small experimental project.
The primary goal is for me to get familiar with the Python basics, the secondary one is to put up a site that showcases some leetcode problem solutions.

All in all the goal is to create a website, that:
- Works without hosting (github pages).
- Showcases my leetcode problem solutions + comments.

### Current key feature decisions (a subject to change):
- Use vue for client side, use JSON for storing data.
- Create a python CLI script to automate the work with files & constructing JSONs.

### Draft
#### Structure

##### Site

/problems/ - a place to store solutions 

/problems/leetcode/ - leetcode solutions

/problems/leetcode/{id}/ - a place to store solution files, {id} being problem id

/assets/ - a place to store css/js needed for site functioning

##### Misc

/leet.py - a CLI script to automatise work with jsons

/bookmarklets/ - a place to store bookmarklets for scraping

##### Issues
- Looks like there is no easy way to scrap leetcode task descriptions without piling up the dependencies. I'll use js bookmarklets to scrap the needed ones + insert from clipboard.
- The bookmarklet "convert-images-to-data-uri" feature took too much time to implement since simple canvas solution didn't work due to canvas tainting.
- Python does not seem to have a convenient/pretty way to store a dict of functions, the workarounds seem to be not pretty enouh too, so the simplest way it is (for now at least).
- Tkinter has proven to be useless, switched to pyperclip