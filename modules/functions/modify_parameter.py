from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join, exists


from ast import literal_eval

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.write_files import write_csv
from .. classes import FEBio_soup, FEBio_xml_parser


def modify_parameter(inputs):
	print("=== Modifying tag ===")

	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))

	params_to_modify = literal_eval(inputs[POSSIBLE_INPUTS.PARAM_VALS])
	output_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]
	make_new_file = inputs[POSSIBLE_INPUTS.SAVE_AS_NEW]

	# print("Interpreted params: ", params_to_modify)
	
	# start loop
	for (fp, ff, fn) in path_feb_files:
		print("path:",fp)
		febio = FEBio_xml_parser.FEBio_xml_parser(fp)

		# modify params:
		tags=[]
		contents=[]
		for param_index, param in enumerate(params_to_modify):
			# check params
			for a in ['tag', 'content', 'branch']:
				if a not in param:
					raise(AssertionError("Missing input under PARAM_VALS:", a, "at param index:",param_index))

			tag = param['tag']
			content = str(param['content'])
			branch = param['branch']
			tags.append(tag)
			contents.append(content)
			febio.modify_tag(tag, content, branch)

		# set output file name
		print("NEW FILE:")
		# print("\\".join(fp.rsplit("\\")[:-1]))
		
		name = fn
		if make_new_file: 
			name = join(str(output_folder), fn + "_%s" + ".feb")
			i = 0
			while exists(name % i):
				i += 1

			name = name % i
			write_csv("modified_param_log.csv",[["index:", i, "param:", "; ".join(tags), "content:", "; ".join(contents)]], path=output_folder, mode="a")
		
		febio.write_feb(output_folder, name)	