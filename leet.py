import sys
import pyperclip
import argparse
import os
import json

BASE_PATH ='./problems/leetcode/' 
PROBLEM_FILENAME = 'problem.json' #TODO(?): move constants to a separate file to be used by both this and js script


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
		'description': 'Problem description',
		'title': 'Problem title'
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



def problem_add (pid = None, title = None):
	"""
		Creates a problem folder & .json file, containing problem data in it by using either arguments or JSON from clipboard
	"""
	clipboard = pyperclip.paste()
	
	data = None
	description = ''
	difficulty = ''
	
	try:
		data = json.loads(clipboard)
	except:
		pass
	
	if (data != None and yes_or_no('Clipboard seems to contain a valid JSON, use it for problem creation?','yes')):
		if (pid == None or (pid != data['id'] and yes_or_no('JSON contains an id different from the provided one, use id from JSON?','yes'))):
			pid = data['id']

		title = data['title']
		description = data['description']
		difficulty = data['difficulty']
	else:
		if (pid == None):
			sys.exit('No id given')
		if (title == None):
			sys.exit('No title given')
	
	output_dict = {
		'id': pid,
		'title':title,
		'description':description,
		'difficulty':difficulty
	};
	
	path_to_problem = BASE_PATH + pid + '/'
	path_to_file = path_to_problem + PROBLEM_FILENAME
	
	if (os.path.exists(path_to_problem)):
		if (yes_or_no('The problem folder is already in place, rewrite problem data?','no')):
			pass
		else:
			sys.exit('You chose to not rewrite the problem data')
	else:
		try:
			os.makedirs(path_to_problem)
		except:
			sys.exit('Unable to create folder')


	try:
		file = open(path_to_file,'w');
		json.dump(output_dict,file);
		file.close();
	except:
		sys.exit('Unable to create/write file')
		
	print('Problem created');
	

def problem_delete ():
	pass

def problem_comment ():
	pass
	
command_mapping = { #TODO(?):find a prettier way to do it
	'add':problem_add,
	'delete':problem_delete,
	'comment':problem_comment,
}

def main():
	if (not os.path.exists(BASE_PATH)):
		print ('Path "' + BASE_PATH + '" is not found, have a nice day')
		exit(1)
		
	parser = argparse.ArgumentParser(description = 'A script for managing problems from leetcode')
	command = None

	subparsers = parser.add_subparsers(help='sub-command help',dest='command')
	parser_create = subparsers.add_parser('add', help=help_descriptions['add']['_cmd_'])
	parser_create.add_argument('pid', help = help_descriptions['pid'],nargs='?')
	parser_create.add_argument('title', help = help_descriptions['add']['title'],nargs='?')

	parser_delete = subparsers.add_parser('delete', help=help_descriptions['delete']['_cmd_'])
	parser_delete.add_argument('pid', help = help_descriptions['pid'])

	parser_comment = subparsers.add_parser('comment', help=help_descriptions['comment']['_cmd_'])
	parser_comment.add_argument('pid', help = help_descriptions['pid'])
	parser_comment.add_argument('lang', choices=['global','js','py'],help = help_descriptions['comment']['lang'],type=ascii)
	parser_comment.add_argument('text', help = help_descriptions['comment']['text'],type=ascii)

	parser_description = subparsers.add_parser('description', help=help_descriptions['description'])
	parser_description.add_argument('pid', help = help_descriptions['pid'])

	parser_reindex = subparsers.add_parser('reindex', help=help_descriptions['reindex']['_cmd_'])
	
	
	args = vars(parser.parse_args())
	command = args.pop('command');
	
	#print (args)
	command_mapping[command](**args)
	
	#try:
	#	command_mapping[command](args)
	#except:
	#	print ('Something went wrong')
	#	exit(1);
	
	#print (command)
	

#try:
#	command_mapping[args[0]]()
#	break;

if __name__ == "__main__":
	main()
