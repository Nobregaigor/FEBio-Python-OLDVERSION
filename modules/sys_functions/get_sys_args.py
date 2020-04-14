import sys, getopt
import os
from os.path import isfile, isdir, isabs, join
from pathlib import Path

from .. enums import COMMAND_INPUT, POSSIBLE_INPUTS, INPUT_FLAG, INPUT_DEFAULTS, PATH_TO_STORAGE

def get_input_arguments():
	print("\nAsserting inputs...")
	argv = sys.argv[1:]

	#####################
	# Check inputs
	#####################

	# Get input command. Should be the first argument after file declaration
	user_command = argv[0].upper()
	user_inputs = argv[1:]
	user_inputs_upper_case = [a.upper() for a in user_inputs]

	# Check if command is valid. If it is not, return False
	command = next((command for command in COMMAND_INPUT.keys() if command.name == user_command), False)
	# In is valid, proceed. Otherwise, raise error
	if not command:
		raise(AssertionError("Input command not valid. Commands should be the first argument. Please, check the system arguments and try again."))

	# Give a feedback of the command found
	print("Command found:", command.name)

	# Get needed inputs
	needed_inputs = COMMAND_INPUT[command]
	
	# Check inputs. Inputs should be declared as INPUT_NAME INPUT_VALUE ...
	inputs = {}
	for inp in needed_inputs:
		_type = inp[0]
		_name = inp[1].name

		# Check required inputs
		if _name not in user_inputs_upper_case:
			if _type == INPUT_FLAG.R:
				raise(AssertionError("Input needed not found:", _name))
			elif _type == INPUT_FLAG.O:
				default_value = INPUT_DEFAULTS[command][inp[1]]
				_user_input = inputs[POSSIBLE_INPUTS[_name]] = INPUT_DEFAULTS[command][inp[1]]
				print("*** Warning:", _name,"was not provided. Falling back to default value:",default_value)
		else:
			_user_input = user_inputs[user_inputs_upper_case.index(_name) + 1]

		# Check if input is a absolute or local path. If not add full path to storage
		if not isabs(_user_input):
			_user_input = join(PATH_TO_STORAGE, _user_input)

		# Check if it is a file or path to directory
		if _name.find("FILE") != -1:
			if not check_if_is_file(_user_input):
				raise(AssertionError("Input file: ", _name, "is not a valid file. Please check arguments and try again."))
		elif _name.find("FOLDER") != -1:
			if not check_if_is_folder(_user_input):
				print("folder:",_user_input)
				raise(AssertionError("Input folder: ", _name, "is not a valid folder. Please check arguments and try again."))

		inputs[POSSIBLE_INPUTS[_name]] = _user_input

	print("Input arguments found:")
	for inp in inputs:
		print("- " + inp.name + ":", inputs[inp])

	return (command, inputs)


def check_if_is_file(inp):
	return True if isfile(inp) else False

def check_if_is_folder(inp):
	return True if isdir(inp) else False
