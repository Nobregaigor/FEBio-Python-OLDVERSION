from copy import copy

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. classes import FEBio_soup, FEBio_xml_parser
from .. sys_functions.write_files import write_csv
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def extract_geometry_data_from_feb(inputs):
	function_name = 'EXTRACT_GEOMETRY_DATA'
	log.log_step("\n== {} ==\n".format(function_name))

	# GET RA Inputs
	path_feb_files = get_path_to_FEB_files(inputs)
    
	# Get optional Inputs
	path_o_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)

	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		log.log_substep("Extracting geometry data from: {}.".format(path_feb_file[2]))
		FEBio_xml = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])
		# Insert properties as tags for each selected property
		nodes, elems = FEBio_xml.get_geometry_data()
		write_csv(path_feb_file[2] + "_nodes", nodes, path=path_o_folder)
		write_csv(path_feb_file[2] + "_elems", elems, path=path_o_folder)


