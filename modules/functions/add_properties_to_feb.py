from copy import copy

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup


def add_properties_to_feb(inputs): 
	print("\n== Adding properties ==")

	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))

	# path_feb_file = inputs[POSSIBLE_INPUTS.FEB_FILE]
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

	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		print("\n--> Adding properties to:", path_feb_file[2])
		febio_soup = FEBio_soup(path_feb_file[0])
		# Insert properties as tags for each selected property
		for prop in properties:
			febio_soup.insert_tag(copy(prop[1]))
		# Write new feb file at given folder
		febio_soup.write_feb(path_o_folder, path_feb_file[1])
