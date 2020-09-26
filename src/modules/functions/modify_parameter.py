from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join, exists


from ast import literal_eval

from .. enums import POSSIBLE_INPUTS
from .. classes import FEBio_soup, FEBio_xml_parser
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.write_files import write_csv
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def modify_parameter(inputs):
	function_name = 'MODIFY_PARAMETER'
	log.log_step("\n== {} ==\n".format(function_name))

	# GET RA Inputs
	path_feb_files = get_path_to_FEB_files(inputs)

	# Get optional Inputs
	params_to_modify = get_optional_input(inputs, 'PARAM_VALS', function_name)
	output_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)
	make_new_file = get_optional_input(inputs, 'SAVE_AS_NEW', function_name)

	# eval params
	params_to_modify = literal_eval(params_to_modify)

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