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
	
	# Get prop files avaiable
	properties_files = find_files(path_p_folder,("fileFormat","xml"))
	# Create a dict with avaiable props if they are in selected props
	properties = []
	for file in properties_files:
		if selected_prop == "all":
			properties.append( (file[2], read_xml(file[0])) )
		else:
			if file[2] in selected_prop:
				properties.append( (file[2], read_xml(file[0])) )

	
	febio_soup = FEBio_soup(path_feb_file)
	for prop in properties:
		febio_soup.insert_tag(prop[1])

	febio_soup.write_feb(path_o_folder, "test.feb")



	# print(soup.prettify())

	# feb_file = open("path_feb_file","r")
	# contents = infile.read()
	# soup = BeautifulSoup(contents,'xml')
	# titles = soup.find_all('title')
	# for title in titles:
	# 		print(title.get_text())

	# print(inputs)


	# feb_file_name = path_feb_file.split("\\")[-1]

	# # Set properties that will be added in feb file
	# properties_list = ['control', 'material', 'boundary', 'load_data', 'output', 'endline']
	# # Read properties and append content in array
	# properties_content = read_properties(properties_list, path_p_folder)

	# # Read files:
	# with open(path_feb_file, 'r') as file:
	# 	file_content = file.readlines()

	# with open(join(path_o_folder, feb_file_name), 'w') as file:
	# 	trigger = False
	# 	trigger_2 = False
	# 	idx = 0
	# 	for content in file_content:

	# 			if idx == 2:
	# 				file.write('    <Module type="solid" />\n')
	# 				for prop in properties_content[0:2]:
	# 						file.writelines(prop)

	# 				properties_content = properties_content[2:]

	# 			if content.find("</febio_spec>") == -1:
	# 				found_content_to_write = [True if content.lower().find(prop) >= 0 else False for prop in properties_list]
	# 				if any(found_content_to_write):
	# 						trigger = not trigger

	# 				if not trigger and not trigger_2:
	# 						file.write(content)

	# 				if trigger != trigger_2:
	# 						trigger_2 = trigger
		
	# 			idx += 1
							
	# 	for content in properties_content:
	# 			file.writelines(content)




