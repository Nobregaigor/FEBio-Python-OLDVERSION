
from os.path import join
from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
# from .. enums import *


from .add_properties_to_feb import add_properties_to_feb
from .create_loadcurve_xml import create_load_curve_xml
from .add_loadcurve_to_feb import add_loadcurve_to_feb
from .extract_geometry_data_from_feb import extract_geometry_data_from_feb
from .calculate_fibers import calculate_fibers
from .add_fibers_to_feb import add_fibers_to_feb

def prepare_feb(inputs):

	# Raw -> with_properties -> with_load
	# Raw -> geometry_data -> fibers_data
	# fibers_data -> with_properties
	# fibers_data -> with_load

	# Set commands in order to be executed
	# to_execute = [
	# 	# Part 1: Raw -> with_properties -> with_load
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.ADD_PROPERTIES],
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.ADD_LOAD],
	# 	# Part 2: Raw -> geometry_data -> fibers_data
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA],
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.CALCULATE_FIBERS],
	# 	# Part 3: fibers_data -> with_properties
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.ADD_FIBERS],
	# 	# Part 4: fibers_data -> with_load
	# 	COMMAND_FUNCTION[POSSIBLE_COMMANDS.ADD_FIBERS],
	# ]

	# Set commands in order to be executed
	to_execute = [
		# Part 1: Raw -> with_properties -> with_load
		add_properties_to_feb,
		add_loadcurve_to_feb,
		# Part 2: Raw -> geometry_data -> fibers_data
		extract_geometry_data_from_feb,
		calculate_fibers,
		# Part 3: fibers_data -> with_properties
		add_fibers_to_feb,
		# Part 4: fibers_data -> with_load
		add_fibers_to_feb,
	]

	# Set inputs in order to be executed
	inputs = [
		# Part 1:
		INPUT_DEFAULTS[POSSIBLE_COMMANDS.ADD_PROPERTIES],
		INPUT_DEFAULTS[POSSIBLE_COMMANDS.ADD_LOAD],
		# Part 2:
		INPUT_DEFAULTS[POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA],
		INPUT_DEFAULTS[POSSIBLE_COMMANDS.CALCULATE_FIBERS],
		# Part 3:
		{
			POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
			POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE,"with_fibers")
		},
		# Part 4:
		{
			POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_load"),
			POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE,"with_fibers")
		}
	]

	# Execute commands with given inputs

	for i, command in enumerate(to_execute):
		command(inputs[i])

def execute_prepare_feb(inputs):
	prepare_feb(inputs)