import json
from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join, exists
from os import rename
import numpy as np
import time

from ast import literal_eval

from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.write_files import write_csv
from .. classes import FEBio_soup, FEBio_xml_parser

from .modify_parameter import modify_parameter
from .run_feb import run_feb


def extract_training_data(data, param):
	p = data["parameters"][param]

	# Validade range and extract values
	if "range" in p:
		start_val = p["range"][0]
		end_val = p["range"][1]
	else:
		raise(AssertionError("'range' was not found in param:", param))
	
	# Validade interation method and create interarray
	if "step_size" in p:
		interarray = np.arange(start_val, end_val, p["step_size"])
	elif "num_elems" in p:
		interarray = np.linspace(start_val, end_val, p["num_elems"])
	else:
		raise(AssertionError("interation method not found in param:", param, "possible values are: 'step_size', 'num_elems' for training_data"))
	
	interarray = interarray.round(decimals=4)
	return start_val, end_val, interarray

def extract_validation_data(data, param):
	p = data["parameters"][param]

	# Validade range and extract values
	if "range" in p:
		start_val = p["range"][0]
		end_val = p["range"][1]
	else:
		raise(AssertionError("'range' was not found in param:", param))
	
	# Validade interation method and create interarray
	if "num_elems" in p:
		r_arr = np.random.random_sample((p['num_elems'], ))
		interarray = (end_val - start_val) * r_arr + start_val
		interarray = interarray.round(decimals=4)
	else:
		raise(AssertionError("interation method not found in param:", param, "possible values are: 'num_elems' for validadion_data"))

	return start_val, end_val, interarray

def read_param_data(study_type, data, param):
	if study_type == "training":
		return extract_training_data(data, param)
	elif study_type == "validation":
		return extract_validation_data(data, param)
	else:
		raise(ValueError("'study_type' not recognized at param:", param))

def create_mod_p_string(param, val):
	p_string = "'tag':'{0}','content':{1},'branch':['Material','material','solid']".format(str(param), val)
	p_string = "{" + p_string + "}"
	return p_string

def join_p_string(s1, s2):
	return "[" + s1 +","+s2+"]"

def prepare_parameter_study(inputs):
	print("=== Preparing parameter study ===")

	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))

	output_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]
	config_file = inputs[POSSIBLE_INPUTS.CONFIG_FILE]

	position_data_file_path = join(output_folder,"position_data.txt")
	displacement_data_file_path = join(output_folder,"displacement_data.txt")
	stress_data_file_path = join(output_folder,"stress_data.txt")


	# get parameter data
	with open(config_file) as f:
		data = json.load(f)

	
	study_type = data["study_type"]
	params_order = [param for param in data["parameters"]]

	if "repetition" in data:
		repRange = range(data['repetition'])
	else:
		repRange = [1]

	if "crossIteration" in data:
		if data["crossIteration"].lower() == "false":
			crossIteration = False
		else:
			crossIteration = True
	else:
		crossIteration = True

	used_combinations = set()

	print("\n")
	print("study_type:", study_type)
	print("params:", data["parameters"])
	# print("repetition", repetition)
	print("crossIteration", crossIteration)

	print(". " * 50)
	print("\n")

	total_params = len(params_order)
	total_feb_files = len(path_feb_files)

	for fi, (fp, ff, _) in enumerate(path_feb_files):

		file_counter = 0
		# Loop through repetions
		for _ in repRange:

			# Loop through all parameters
			for i, parameter in enumerate(params_order):
				# Get data for 'parent' parameter
				(_, _, interarray) = read_param_data(study_type, data, parameter)

				# Loop trhough all values in range of the 'parent' parameter
				for val1 in interarray:

					# Loop through all parameters and ignore if 'child' parameter is the same as 'parent'
					for j, parameter2 in enumerate(params_order):
						if i != j and parameter != parameter2:

							if crossIteration == False:
								# Get data for 'child' parameter
								(_, _, interarray_2) = read_param_data(study_type, data, parameter)
							else:
								(_, _, interarray_2) = read_param_data(study_type, data, parameter2)

							# Loop trhough all values in range of the 'child' parameter
							for val2 in interarray_2:

								print("Parameter: ", parameter, "| Val: ",  val1)
								print("Parameter: ", parameter2, "| Val: ",  val2)

								if (val1, val2) not in used_combinations:
									used_combinations.add((val1,val2))

									# Modify Parameter 
									# ------------------------------

									# Create strings
									param_vals1 = create_mod_p_string(parameter, val1)
									param_vals2 = create_mod_p_string(parameter2, val2)
									param_vals = join_p_string(param_vals1, param_vals2)

									# run modify parameter
									modify_parameter({
										POSSIBLE_INPUTS.FEB_FILE: fp,
										POSSIBLE_INPUTS.OUTPUT_FOLDER: output_folder,
										POSSIBLE_INPUTS.SAVE_AS_NEW: False,
										POSSIBLE_INPUTS.PARAM_VALS: param_vals
									})

									time.sleep(0.1)

									# Run FEB
									# ------------------------------
									path_to_run = join(output_folder, ff)

									run_feb({
										POSSIBLE_INPUTS.FEB_FILE: path_to_run
									})

									time.sleep(0.1)

									# Modify Results filenames
									# ------------------------------

									# Check if files exist:
									if exists(position_data_file_path): #pos
										rename(position_data_file_path,join(output_folder,"position_data_%s.txt" % file_counter))
									if exists(displacement_data_file_path): #displ
										rename(displacement_data_file_path,join(output_folder,"displacement_data_%s.txt" % file_counter))
									if exists(stress_data_file_path): # stress
										rename(stress_data_file_path,join(output_folder,"stress_data_%s.txt" % file_counter))

									# Record info
									write_csv("modified_param_log.csv",[["index:", file_counter, "param:", "; ".join([parameter, parameter2]), "content:", "; ".join([str(val1), str(val2)])]], path=output_folder, mode="a")

									# Increase counter:
									file_counter += 1

				
				print("=-"*60)
				print("Percentage completed: ", (i + 1)/total_params)
				print("=-"*60)

			print("=---"*30)
			print("FEB files read: ", (fi + 1)/total_feb_files)
			print("=---"*30)
