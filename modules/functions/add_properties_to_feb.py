from bs4 import BeautifulSoup

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup


def add_properties_to_feb(inputs): 
	print("\nAdding properties...")

	# Get inputs
	path_feb_file = inputs[POSSIBLE_INPUTS.FEB_FILE]
	path_p_folder = inputs[POSSIBLE_INPUTS.PROPERTIES_FOLDER]
	path_o_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]
	selected_prop = inputs[POSSIBLE_INPUTS.SELECTED_PROPERTIES].lower()

	# Determine which properties should include
	if selected_prop.find("except") != -1:
		function_type = "except"
		excluded_files = selected_prop.strip("except").split("-")
		print("*** Warning: The following properties will be excluded:", excluded_files)
	elif selected_prop == "all":
		function_type = "all"
	else:
		function_type = "selected"
		selected_files = selected_prop.split()

	# Get prop files avaiable
	properties_files = find_files(path_p_folder,("fileFormat","xml"))
	# Create a dict with avaiable props if they are in selected props
	properties = []
	for file in properties_files:
		if function_type == "all":
			properties.append( (file[2], read_xml(file[0])) )
		elif function_type == "except":
			if file[2] not in excluded_files:
				properties.append( (file[2], read_xml(file[0])) )
		else:
			if file[2] in selected_files:
				properties.append( (file[2], read_xml(file[0])) )

	# Create FEBio_soup instace
	febio_soup = FEBio_soup(path_feb_file)
	# Insert properties as tags for each selected property
	for prop in properties:
		febio_soup.insert_tag(prop[1])
	# Write new feb file at given folder
	febio_soup.write_feb(path_o_folder, "test.feb")
