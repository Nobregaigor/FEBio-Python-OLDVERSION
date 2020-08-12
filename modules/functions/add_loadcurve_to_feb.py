from copy import copy
from os.path import join
from bs4 import BeautifulSoup

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup, FEBio_xml_parser


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
	load_names = load_name.split("-") if load_name.find("-") != -1 else [load_name]
	print("load names: ", load_names)
	loadData_files = find_files(load_folder,("fileFormat","xml"))
	# Match files that contain load_name
	loadData_files = [l for l in loadData_files if l[1].split("_")[0] in load_names]

	# Separate load "header"
	loads_files = [l for l in loadData_files if l[1].find("loadcurve") == -1]
	# Remove load "headers" from loadData_files
	for elem in loads_files:
		loadData_files.remove(elem)

	print("loadData_files: ", loadData_files)
	# Read files
	# loads = []
	# for file in loadData_files:
	# 	loads.append( (file[2], read_xml(file[0])) )

	# headers = []	
	# for file in loads_files:
	# 	headers.append( (file[2], read_xml(file[0])) )

	for path_feb_file in path_feb_files:
		# Create FEBio_soup instace
		print("\n--> Adding load to:", path_feb_file[2])
		febio_soup = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])

		# Check if FEBio_xml_parser has loadcurves
		if "LoadData" not in febio_soup.existing_tags:
			febio_soup.add_tag("<LoadData></LoadData>")
		
		if "Loads" not in febio_soup.existing_tags:
			febio_soup.add_tag("<Loads></Loads>")

		# else:


		# load_data = febio_soup.soup.find("LoadData")
		# if load_data != None:
		# 	val = len(load_data.findChildren("loadcurve"))
		# 	attr_id = val + 1
		# 	has_loaddata = True
		# else:
		# 	attr_id = 1
		# 	has_loaddata = False
				
		# Insert properties as tags for each selected property
		for load in loads_files:
			print("--- Adding content to Loads")
			febio_soup.add_tag(load[0], "Loads")

		for load_data in loadData_files:
			print("--- Adding content to LoadData")
			febio_soup.add_tag(load_data[0], "LoadData")
			# if has_loaddata:
			# 	c = copy(load[1])
			# 	c.loadcurve['id'] = attr_id
			# 	print("LOAD CURVE ID = ",attr_id )
			# 	febio_soup.soup.LoadData.insert(attr_id, c)

			# else:
			# 	febio_soup.add_tag("LoadData", copy(load[1]))

		# print(febio_soup.soup)

			# febio_soup.insert_tag(copy(load[1]))
		# Write new feb file at given folder
		febio_soup.write_feb(output_folder, path_feb_file[1])
