import subprocess

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files, find_folders
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup

def run_feb(inputs):
	print("\n== Running FEB files == ")
	
	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_to_folders = find_folders(inputs[POSSIBLE_INPUTS.INPUT_FOLDER])
		path_feb_files = []
		for folder in path_to_folders:
			path_feb_files.extend(find_files(folder[0],("fileFormat","feb")))

	for feb_file in path_feb_files:
		print("\n--> Running: ", feb_file[2])
		res = subprocess.call([
			"FEBio2.exe",
			feb_file[0]
		])
		if res != 0:
			print(res)