
import sys, getopt
import os
from os.path import isfile, join
from pathlib import Path

from .. enums import POSSIBLE_INPUTS


def read_properties(properties_list,path_p_folder):
	props_content = []

	for prop in properties_list:
		try:
			with open(join(path_p_folder, prop + ".txt"), "r") as file:
					props_content.append(file.readlines())
		except:
			properties_list.remove(prop)
			print("Could not find file associated with property:", prop)
	return props_content

def add_properties_to_feb(inputs): 
	print("\nAdding properties...")
	path_feb_file = inputs[POSSIBLE_INPUTS.FEB_FILE]
	path_p_folder = inputs[POSSIBLE_INPUTS.PROPERTIES_FOLDER]
	path_o_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]

	print(inputs)


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




