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
	R_NP = auto() # Required but it is not a path
	O_NP = auto() # Optional but it is not a path
	R1 = auto() # Required if optional is not found
	O1 = auto() # Optional that can substitue required



####################################
# COMMANDS
####################################

# Create a list of possible commands that the program can recogine and execute
possible_commands = [
	"ADD_PROPERTIES",
	"ADD_FIBERS",
	"CREATE_LOADCURVE",
	"ADD_LOAD",
	"EXTRACT_GEOMETRY_DATA", # nodes and elements
	"CALCULATE_FIBERS",
	"ADD_FIBERS",
	"PREPARE",
	"RUN_FEB",
	"CREATE_STORAGE_FOLDER",
	"CALCULATE_RESULTS"
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
	"INPUT_FOLDER",
	"FEB_NAME",

	# ADD_PROPERTIES
	"PROPERTIES_FOLDER",
	"SELECTED_PROPERTIES",

	# CREATE_CURVE
	"CURVE_NAME",
	"CURVE_MODEL",
	"CURVE_PARAMS",
	"CURVE_FOLDER",
	"CURVE_TYPE",

	# ADD_LOAD,
	"LOAD_FOLDER",
	"LOAD_NAME",
	"LOAD_ATTRS",
	"LOAD_TYPE",

	# EXTRACT_GEOMETRY_DATA,
	# None new inputs
	"GEOMETRY_DATA_FOLDER",
	"PATH_TO_MATLAB_FOLDER",

	"FIBERS_DATA_FOLDER",

	# CREATE_STORAGE_FOLDER
	"STORAGE_NAME",
	"PATH_TO_STORAGE",
]

# Convert the possible inputs list to an Enum class
POSSIBLE_INPUTS = Enum('POSSIBLE_INPUTS', {a:auto() for a in possible_inputs})

######################################
# RELATE COMMANDS AND INPUTS
######################################

# Crosslink the commands and its inputs
COMMAND_INPUT = {
	# ADD_FIBERS
	POSSIBLE_COMMANDS.ADD_FIBERS: [
		(INPUT_FLAG.R, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.R, POSSIBLE_INPUTS.FIBER_TABLES_FILE), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER) 
	],

	# ADD_PROPERTIES
	POSSIBLE_COMMANDS.ADD_PROPERTIES: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.PROPERTIES_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER), 
		(INPUT_FLAG.O_NP, POSSIBLE_INPUTS.SELECTED_PROPERTIES)
	],

	# CREATE LOADCURVE
	POSSIBLE_COMMANDS.CREATE_LOADCURVE: [
		(INPUT_FLAG.R_NP, POSSIBLE_INPUTS.CURVE_NAME), 
		(INPUT_FLAG.R_NP, POSSIBLE_INPUTS.CURVE_MODEL), 
		(INPUT_FLAG.R_NP, POSSIBLE_INPUTS.CURVE_PARAMS),
		(INPUT_FLAG.O, POSSIBLE_INPUTS.CURVE_FOLDER), 
		(INPUT_FLAG.O_NP, POSSIBLE_INPUTS.CURVE_TYPE),
	],

	# ADD_LOAD
	POSSIBLE_COMMANDS.ADD_LOAD: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER), 
		(INPUT_FLAG.O_NP, POSSIBLE_INPUTS.LOAD_NAME), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.LOAD_FOLDER), 
		(INPUT_FLAG.O_NP, POSSIBLE_INPUTS.LOAD_ATTRS), 
	],

	# EXTRACT_GEOMETRY_DATA
	POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER), 
	],

	# CALCULATE_FIBERS
	POSSIBLE_COMMANDS.CALCULATE_FIBERS: [
		(INPUT_FLAG.O_NP, POSSIBLE_INPUTS.FEB_NAME), # Name of the file or "all" (all files in geometry data folder)
		(INPUT_FLAG.O, POSSIBLE_INPUTS.GEOMETRY_DATA_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.PATH_TO_MATLAB_FOLDER), 
	],

	# ADD_FIBERS
	POSSIBLE_COMMANDS.ADD_FIBERS: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.FIBERS_DATA_FOLDER),
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER), 
	],

	# PREPARE
	POSSIBLE_COMMANDS.PREPARE: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.OUTPUT_FOLDER),
	],

	# RUN_FEB
	POSSIBLE_COMMANDS.RUN_FEB: [
		(INPUT_FLAG.R1, POSSIBLE_INPUTS.FEB_FILE), 
		(INPUT_FLAG.O1, POSSIBLE_INPUTS.INPUT_FOLDER), 
	],
	
	# CREATE_STORAGE_FOLDER: 
	POSSIBLE_COMMANDS.CREATE_STORAGE_FOLDER: [
		(INPUT_FLAG.R_NP, POSSIBLE_INPUTS.STORAGE_NAME), 
		(INPUT_FLAG.O, POSSIBLE_INPUTS.PATH_TO_STORAGE), 
	],

	# CALCULATE_RESULTS
	POSSIBLE_COMMANDS.CALCULATE_RESULTS: [
		(INPUT_FLAG.O, POSSIBLE_INPUTS.INPUT_FOLDER), 
	]
}