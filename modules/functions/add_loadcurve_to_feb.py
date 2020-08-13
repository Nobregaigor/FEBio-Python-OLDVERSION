from copy import copy
from os.path import join
from bs4 import BeautifulSoup

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. classes import FEBio_xml_parser

from .. logger import console_log as log

def add_loadcurve_to_feb(inputs): 
	function_name = 'ADD_LOAD'
	log.log_step("\n== {} ==\n".format(function_name))

	# GET RA Inputs
	path_feb_files = get_path_to_FEB_files(inputs)

	load_name = get_optional_input(inputs, 'LOAD_NAME', function_name)
	load_folder = get_optional_input(inputs, 'LOAD_FOLDER', function_name)
	load_attrs = get_optional_input(inputs, 'LOAD_ATTRS', function_name)
	output_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)

	# Get files under load
	load_names = load_name.split("-") if load_name.find("-") != -1 else [load_name]
	loadData_files = find_files(load_folder,("fileFormat","xml"))
	# Match files that contain load_name
	loadData_files = [l for l in loadData_files if l[1].split("_")[0] in load_names]

	# Separate load "header"
	loads_files = [l for l in loadData_files if l[1].find("loadcurve") == -1]
	# Remove load "headers" from loadData_files
	for elem in loads_files:
		loadData_files.remove(elem)

	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		log.log_substep("Adding load to: {}.".format(path_feb_file[2]))
		febio_soup = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])

		# Check if FEBio_xml_parser has loadcurves
		if "LoadData" not in febio_soup.existing_tags:
			febio_soup.add_tag("<LoadData></LoadData>")
		
		if "Loads" not in febio_soup.existing_tags:
			febio_soup.add_tag("<Loads></Loads>")


		# Insert properties as tags for each selected property
		for load in loads_files:
			febio_soup.add_tag(load[0], "Loads")

		for load_data in loadData_files:
			febio_soup.add_tag(load_data[0], "LoadData")


		# Write new feb file at given folder
		febio_soup.write_feb(output_folder, path_feb_file[1])
