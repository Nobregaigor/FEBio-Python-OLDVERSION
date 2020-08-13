import subprocess

from .. enums import POSSIBLE_INPUTS
from .. classes import FEBio_soup
from .. sys_functions.find_files_in_folder import find_files, find_folders
from .. sys_functions.read_files import read_xml
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def run_feb(inputs):
	function_name = 'RUN_FEB'
	log.log_step("\n== {} ==\n".format(function_name))
	
	# GET RA Inputs
	path_feb_files = get_path_to_FEB_files(inputs)

	for feb_file in path_feb_files:
		print("\n--> Running: ", feb_file[2])
		res = subprocess.call([
			"FEBio2.exe",
			feb_file[0]
		])
		if res != 0:
			print(res)