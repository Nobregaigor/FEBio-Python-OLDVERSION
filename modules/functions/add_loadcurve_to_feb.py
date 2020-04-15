from copy import copy
from os.path import join
from bs4 import BeautifulSoup

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup


def add_loadcurve_to_feb(inputs): 
	print("\n== Adding load curve ==")

	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))

	load_name = inputs[POSSIBLE_INPUTS.LOAD_NAME]
	load_folder = inputs[POSSIBLE_INPUTS.LOAD_FOLDER]
	load_attrs = inputs[POSSIBLE_INPUTS.LOAD_ATTRS]
	load_name = inputs[POSSIBLE_INPUTS.LOAD_NAME]
	output_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]


	# Get files under load
	load_files = find_files(load_folder,("fileFormat","xml"))
	# Match files that contain load_name
	load_files = [l for l in load_files if l[1].find(load_name) != -1]
	# Separate load "header"
	load_headers_files = [l for l in load_files if l[1].find("loadcurve") == -1]
	# Remove load "headers" from load_files
	for elem in load_headers_files:
		load_files.remove(elem)

	# Read files
	loads = []
	for file in load_files:
		loads.append( (file[2], read_xml(file[0])) )

	headers = []	
	for file in load_headers_files:
		headers.append( (file[2], read_xml(file[0])) )

	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		print("\n--> Adding load to:", path_feb_file[2])
		febio_soup = FEBio_soup(path_feb_file[0])
		# Check if FEBio_soup has loadcurves
		load_data = febio_soup.soup.find("LoadData")
		if load_data != None:
			val = len(load_data.findChildren("loadcurve"))
			attr_id = val + 1
			has_loaddata = True
		else:
			attr_id = 1
			has_loaddata = False
				
		# Insert properties as tags for each selected property
		for header in headers:
			print("--- Adding header")
			print(header)
			febio_soup.add_tag("Loads", copy(header[1]))

		for load in loads:
			print("--- Adding load")
			if has_loaddata:
				c = copy(load[1])
				c.loadcurve['id'] = attr_id
				febio_soup.soup.LoadData.insert(attr_id, c)

			else:
				febio_soup.add_tag("LoadData", copy(load[1]))

		# print(febio_soup.soup)

			# febio_soup.insert_tag(copy(load[1]))
		# Write new feb file at given folder
		febio_soup.write_feb(output_folder, path_feb_file[1])
