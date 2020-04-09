"""
	Possible commands:
		In this module, we store the possible commands and inputs that we can receive from the command line.
		The possible commands and possible inputs are stored in their respective lists. To add new command
		or input, just append them in its respective list.
		Also, these commands and inputs are converted to Enum classes. This facilitates the understaing in
		other modules and slightly increases the performance.
		Lastly, the commands and inputs are crosslinked at the COMMAND_INPUT dictionary

		rules:
			low case represents lists of commands/inputs
			upper case represents ENUMS created from the lists

		usage:
			inputs = COMMAND_INPUT[POSSIBLE_COMMANDS.COMMAND]

		example:
			inputs = COMMAND_INPUT[POSSIBLE_COMMANDS.ADD_FIBERS]
			--> returns: inputs = [<POSSIBLE_INPUTS.FEB_FILE: 1>, <POSSIBLE_INPUTS.FIBER_TABLES_FILE: 2>, <POSSIBLE_INPUTS.OUTPUT_FOLDER: 4>]
"""
############################################################################

from enum import Enum, auto

class INPUT_FLAG(Enum):
	R = auto() #	Required
	O = auto() #  Optional


####################################
# COMMANDS
####################################

# Create a list of possible commands that the program can recogine and execute
possible_commands = [
	"ADD_PROPERTIES",
	"ADD_FIBERS",
]

# Convert the possible commands list to an Enums class
POSSIBLE_COMMANDS = Enum('POSSIBLE_COMMANDS', {a:auto() for a in possible_commands})


###################################
# INPUTS
###################################

# Create a list of possible inputs that the program can receive
possible_inputs = [
	"FEB_FILE",
	"FIBER_TABLES_FILE",
	"FEB_FOLDER",
	"OUTPUT_FOLDER",

	# ADD_PROPERTIES
	"PROPERTIES_FOLDER",
	"SELECTED_PROPERTIES"
]

# Convert the possible inputs list to an Enum class
POSSIBLE_INPUTS = Enum('POSSIBLE_INPUTS', {a:auto() for a in possible_inputs})


######################################
# RELATE COMMANDS AND INPUTS
######################################

# Crosslink the commands and its inputs
COMMAND_INPUT = {
	# ADD_FIBERS
	POSSIBLE_COMMANDS.ADD_FIBERS: [\
		(INPUT_FLAG.R, POSSIBLE_INPUTS.FEB_FILE), \
		(INPUT_FLAG.R, POSSIBLE_INPUTS.FIBER_TABLES_FILE), \
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER)],

	# ADD_PROPERTIES
	POSSIBLE_COMMANDS.ADD_PROPERTIES: [\
		(INPUT_FLAG.R, POSSIBLE_INPUTS.FEB_FILE), \
		(INPUT_FLAG.O, POSSIBLE_INPUTS.PROPERTIES_FOLDER), \
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER),
		(INPUT_FLAG.O, POSSIBLE_INPUTS.SELECTED_PROPERTIES)]
}