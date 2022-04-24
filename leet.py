import argparse
import os
from tkinter import Tk 
	#from: https://stackoverflow.com/questions/101128/how-do-i-read-text-from-the-clipboard
	#works for me
	#TODO(?): investigate compatibility

BASE_PATH ='./problems/leetcode/' #TODO(?): change to env var or argument later if the need arises

if (os.path.exists(BASE_PATH) != True):
	print ('Path "' + BASE_PATH + '" is not found, have a nice day')
	exit(1)


def yes_or_no(question, default = 'yes'):
	#based on: https://code.activestate.com/recipes/577058/
	"""
		Asks a yes/no "question";
		returns True/False depending on the user input;
		user input is considered to be "default" if the actual input is empty and the `default` is not None.
	"""
	valid = {"yes":True, "y":True,  "ye":True, "no":False, "n":False}
	if default == None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)
	
	while 1:
		print (question + prompt);
		choice = input().lower();
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid.keys():
			return valid[choice]
			

help_descriptions = {
	'pid':'Problem id',
	
	'add': {
		'_cmd_': 'Add problem',
		'description': 'Problem description'
	},
	'comment': {
		'_cmd_': 'Write/rewrite comment for the existing problem or the problem solution',
		'lang': 'Lang shorthand; global = comment to the task ',
		'text': 'Write/rewrite comment for the existing problem solution. Leave empty to see current.',
	},
	
	'delete': {
		'_cmd_': 'Delete problem and all its solutions',
	},
	'reindex': {
		'_cmd_': 'Update JSONs; to be used after manual file modifications',
	},
	'description':'add/rewrite description for the existing problem',
	
}

parser = argparse.ArgumentParser(description = 'something something')

subparsers = parser.add_subparsers(help='sub-command help')
parser_create = subparsers.add_parser('add', help=help_descriptions['add']['_cmd_'])
parser_create.add_argument('pid', help = help_descriptions['pid'])
parser_create.add_argument('description', help = help_descriptions['add']['description'])

parser_delete = subparsers.add_parser('delete', help=help_descriptions['delete']['_cmd_'])
parser_delete.add_argument('pid', help = help_descriptions['pid'])

parser_comment = subparsers.add_parser('comment', help=help_descriptions['comment']['_cmd_'])
parser_comment.add_argument('pid', help = help_descriptions['pid'])
parser_comment.add_argument('lang', choices=['global','js','py'],help = help_descriptions['comment']['lang'],type=ascii)
parser_comment.add_argument('text', help = help_descriptions['comment']['text'],type=ascii)

parser_description = subparsers.add_parser('description', help=help_descriptions['description'])
parser_description.add_argument('pid', help = help_descriptions['pid'])

parser_reindex = subparsers.add_parser('reindex', help=help_descriptions['reindex']['_cmd_'])



def add_problem (problem_id, description = None):
	choice = yes_or_no ('Are you sure?','no');
	return True
	
args = parser.parse_args()
print (args)