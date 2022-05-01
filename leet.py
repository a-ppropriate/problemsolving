import sys
import shutil
import pyperclip
import argparse
import os
import json

#TODO: replace all the sys.exits with appropriate returns / error raises

BASE_PATH ='./problems/leetcode/' #TODO(?): move constants to a separate file to be used by both this and js script
PROBLEM_FILENAME = 'problem.json' 
COMMENT_FILENAME = 'comment'
SOLUTION_FILENAME = 'solution'
INDEX_FILENAME = 'index.json'
SUPPORTED_LANGS = ['js','py3']


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
	'solution': {
		'_cmd_': 'Add solution',
		'lang': 'Lang shorthand'
	},
	'comment': {
		'_cmd_': 'Write/rewrite comment for the existing problem or the problem solution',
		'lang': 'Lang shorthand; global = comment on problem',
		'text': 'Comment text',
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
		if (pid == None or (pid != data.get('id') and yes_or_no('JSON contains an id different from the provided one, use id from JSON?','yes'))):
			pid = data.get('id')

		title = data.get('title')
		description = data.get('description')
		difficulty = data.get('difficulty')
	
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
		with open(path_to_file,'w') as f:
			json.dump(output_dict,f)
	except:
		sys.exit('Unable to create/write file')
	
	reindex()
	sys.exit('Problem created, id:' + pid)

def solution_add (pid = None, lang = None):
	"""
		Adds solution of `lang` to an existing problem with id = `pid` using text from clipboard
	"""
	data = pyperclip.paste().replace("\r", "") # win has some issues with writing "\r\n" to file
	data = data.strip("\r\n\t")
	
	if (pid == None):
		sys.exit('No id given')
	if (lang == None):
		sys.exit('No lang given')
	
	path_to_problem = BASE_PATH + pid + '/'
	path_to_file = path_to_problem + SOLUTION_FILENAME + '.' + lang
	
	if (not os.path.exists(path_to_problem)):
		sys.exit('The chosen problem does not exist')
	
	if (os.path.exists(path_to_file)):
		if(not yes_or_no('There already is a solution for selected lang, rewrite it?','yes')):
			sys.exit('You chose to not rewrite the solution data')
		
	try:
		with open(path_to_file,'w') as f:
			f.write(data)
	except:
		sys.exit('Unable to create/write file')
	
	reindex()
	sys.exit('Solution created')

def problem_delete (pid = None):
	"""
		Deletes problem folder
	"""
	if (pid == None):
		sys.exit('No id given')
	
	path_to_problem = BASE_PATH + pid
	if (yes_or_no('Do you really want to remove problem with id ' + pid + ' and all its solutions?','no')):
		try:
			shutil.rmtree(path_to_problem,ignore_errors=True)
		except:
			sys.exit('Unable to delete problem')
		
		reindex()
		sys.exit('Problem deleted')
	else:
		sys.exit('You chose to leave the problem be')
	
def problem_comment (pid = None, text = None, lang = 'global'):
	"""
		Adds a `global` comment to problem or specific solution for `lang` 
	"""
	filename = COMMENT_FILENAME;
	if (pid == None):
		sys.exit('No id given')
	
	if (text == None):
		sys.exit('No text given')
	
	if (lang != 'global'):
		filename = lang + '_' + filename
	
	path_to_problem = BASE_PATH + pid + '/'
	path_to_file = path_to_problem + filename
	
	if (not os.path.exists(path_to_problem)):
		sys.exit('Problem folder not found')
	elif (os.path.exists(path_to_file)):
		if (not yes_or_no('The comment you are trying to set already exists, overwrite?','no')):
			sys.exit('You chose to keep the old comment')
	
	with open(path_to_file,'w') as f:
		f.write(text)
	
	reindex()
	sys.exit('Comment created')
	
def reindex ():
	"""
		Write/rewrite an index file that contains the data on problems and solutions within BASE_PATH
		Currently "index file" is more of a full data rather than index (probably a subject to change in the future)
	"""
	index_path = BASE_PATH + INDEX_FILENAME
	index = {}
	
	for dir in os.listdir(BASE_PATH):
		dir_path = BASE_PATH + dir + '/'
		problem_file = dir_path + PROBLEM_FILENAME
		problem_comment_file = dir_path + COMMENT_FILENAME
		problem_comment = None
		
		if (not os.path.exists(problem_file)):
			continue
			
		try:
			with open(problem_file,'r') as f:
				problem_data = json.load(f)
		except:
			continue
		
		if os.path.exists(problem_comment_file):
			try:
				with open(problem_comment_file,'r') as f:
					problem_comment = f.read()
			except:
				pass
				
		solutions = {}
		for lang in SUPPORTED_LANGS:
			solution_text = None
			solution_comment = None
			solution_path = dir_path + SOLUTION_FILENAME + '.' + lang
			solution_comment_path = dir_path + lang + '_' + COMMENT_FILENAME
			
			if os.path.exists(solution_path):
				try:
					with open(solution_path,'r') as f:
						solution_text = f.read()
				except:
					pass
			
			if (solution_text == None):
				continue
			
			if os.path.exists(solution_comment_path):
				try:
					with open(solution_comment_path,'r') as f:
						solution_comment = f.read()
				except:
					pass
			
			solutions[lang] = {'solution':solution_text, 'comment':solution_comment}
		
		index[dir] = {'problem': problem_data, 'comment':problem_comment,'solutions': solutions}
	
	try:
		with open(index_path,'w') as f:
			json.dump(index,f,indent=4, sort_keys=True)
			
			return True
	except:
		return False

command_mapping = { #TODO(?):find a prettier way to do it
	'add':problem_add,
	'delete':problem_delete,
	'comment':problem_comment,
	'solution':solution_add,
	'reindex':reindex
}

def main():
	if (not os.path.exists(BASE_PATH)):
		print ('Path "' + BASE_PATH + '" is not found, have a nice day')
		exit(1)
		
	parser = argparse.ArgumentParser(description = 'A script for managing problems from leetcode')
	command = None

	subparsers = parser.add_subparsers(help='sub-command help',dest='command') # TODO(?): organise it better
	parser_create = subparsers.add_parser('add', help=help_descriptions['add']['_cmd_'])
	parser_create.add_argument('pid', help = help_descriptions['pid'],nargs='?')
	parser_create.add_argument('title', help = help_descriptions['add']['title'],nargs='?')
	
	parser_solution = subparsers.add_parser('solution', help=help_descriptions['solution']['_cmd_'])
	parser_solution.add_argument('pid', help = help_descriptions['pid'],nargs='?')
	parser_solution.add_argument('lang', choices=SUPPORTED_LANGS,help = help_descriptions['solution']['lang'])

	parser_delete = subparsers.add_parser('delete', help=help_descriptions['delete']['_cmd_'])
	parser_delete.add_argument('pid', help = help_descriptions['pid'])

	parser_comment = subparsers.add_parser('comment', help=help_descriptions['comment']['_cmd_'])
	parser_comment.add_argument('pid', help = help_descriptions['pid'])
	parser_comment.add_argument('lang', choices=SUPPORTED_LANGS + ['global'],help = help_descriptions['comment']['lang'])
	parser_comment.add_argument('text', help = help_descriptions['comment']['text'])

	parser_reindex = subparsers.add_parser('reindex', help=help_descriptions['reindex']['_cmd_'])
	
	args = vars(parser.parse_args())
	command = args.pop('command');
	
	command_mapping[command](**args)

if __name__ == "__main__":
	main()
