from copy import copy

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. classes import FEBio_soup, FEBio_xml_parser
from .. sys_functions.write_files import write_csv

def extract_geometry_data_from_feb(inputs):
	print("\n== Extracting geometry data ==")
	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))

	path_o_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]


	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		print("\n--> Extracting geometry data from:", path_feb_file[2])
		FEBio_xml = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])
		# Insert properties as tags for each selected property
		nodes, elems = FEBio_xml.get_geometry_data()
		write_csv(path_feb_file[2] + "_nodes", nodes, path=path_o_folder)
		write_csv(path_feb_file[2] + "_elems", elems, path=path_o_folder)


