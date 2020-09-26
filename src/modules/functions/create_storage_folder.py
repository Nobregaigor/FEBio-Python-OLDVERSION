from pathlib import Path
from os.path import join

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup

def create_storage_folder(inputs):
	print("\n== Creating storage...")

	storage_name = inputs[POSSIBLE_INPUTS.STORAGE_NAME]
	path_storage = inputs[POSSIBLE_INPUTS.PATH_TO_STORAGE]

	_path = join(path_storage,storage_name)
	print("Storage_path:", _path)
	Path(_path).mkdir(parents=True, exist_ok=True)

	folders_to_create = [
		'fibers_data',
		'geometry_data',
		'loads',
		'properties',
		'raw',
		'results',
		'with_fibers',
		'with_load',
		'with_properties'
	]

	for folder in folders_to_create:
		print("Making sub-directory:", folder)
		Path(join(_path,folder)).mkdir(parents=True)