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
/index.html ; /assets/ - site files

/problems/`{provider}`/ - directory for storing problems & solutions from "problem providers". Currently leetcode is the only one.

/problems/`{provider}`/index.json - currently is a DB, containing all the info on problems from `provider`; was supposed to be an "index" - a file, containing some data on problem + paths to solution,comment,etc. files.

/problems/`{provider}`/`{id}`/ - directory for storing problem data; currently excluded from the repo.

##### Misc

/leet.py - a CLI script to automatise work with jsons

/bookmarklets/ - a place to store bookmarklets for scraping

##### Issues
- Looks like there is no easy way to scrap leetcode task descriptions without piling up the dependencies. I'll use js bookmarklets to scrap the needed ones + insert from clipboard.
- The bookmarklet "convert-images-to-data-uri" feature took too much time to implement since simple canvas solution didn't work due to canvas tainting.
- Python does not seem to have a convenient/pretty way to store a dict of functions, the workarounds seem to be not pretty enouh too, so the simplest way it is (for now at least).
- Tkinter has proven to be not quite fitting for the task, switched to pyperclip.
- Should've just used bootstrap to save time.