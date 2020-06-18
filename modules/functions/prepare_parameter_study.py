import json
from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join, exists
from os import rename
import numpy as np

from ast import literal_eval

from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.write_files import write_csv
from .. classes import FEBio_soup, FEBio_xml_parser

from .modify_parameter import modify_parameter
from .run_feb import run_feb

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

	params_order = [param for param in data["parameters"]]

	print("order:", params_order)

	for (fp, ff, fn) in path_feb_files:
		file_counter = 0
		for i, parameter in enumerate(params_order):
			a = data["parameters"][parameter]
			a_start = a["range"][0]
			a_end = a["range"][1]
			a_n = (a_end - a_start) / a["step_size"]
			for val1 in np.linspace(a_start, a_end, a_n):

				for j, parameter2 in enumerate(params_order):

					if i != j:
						b = data["parameters"][parameter2]
						b_start = b["range"][0]
						b_end = b["range"][1]
						b_n = (b_end - b_start) / b["step_size"]

						for val2 in np.linspace(b_start, b_end, b_n):
							print(parameter, val1, "|", parameter2, val2)

							
							# Modify Parameter 
							# ------------------------------

							param_vals1 = "'tag':'{0}','content':{1},'branch':['Material','material','active_contraction']".format(str(parameter), val1)
							param_vals1 = "{" + param_vals1 + "}"

							param_vals2 = "'tag':'{0}','content':{1},'branch':['Material','material','active_contraction']".format(str(parameter2), val2)
							param_vals2 = "{" + param_vals2 + "}"
							# print("PARAM VALS:", param_vals)
							param_vals = "[" + param_vals1 +","+param_vals2+"]"

							# print("Setting params of ", parameter, "with respect to", parameter2, "with value of", k)
							modify_parameter({
								POSSIBLE_INPUTS.FEB_FILE: fp,
								POSSIBLE_INPUTS.OUTPUT_FOLDER: output_folder,
								POSSIBLE_INPUTS.SAVE_AS_NEW: False,
								POSSIBLE_INPUTS.PARAM_VALS: param_vals
							})

							# Run FEB
							# ------------------------------
							path_to_run = join(output_folder, ff)
							run_feb({
								POSSIBLE_INPUTS.FEB_FILE: path_to_run
							})

							# Modify Results filenames
							# ------------------------------

							# check if files exist:
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