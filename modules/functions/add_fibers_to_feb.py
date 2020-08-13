from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join

from .. enums import POSSIBLE_INPUTS
from .. classes import FEBio_xml_parser
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def format_data_to_write(data):
	print("Formating data to write.")
	data_to_write = []
	data_to_write.append("\t<MeshData>\n")
	data_to_write.append('\t\t<ElementData elem_set="Part1" var="mat_axis">\n')
	template = '\t\t\t<elem lid="{_id}">\n\t\t\t\t<a>{_f0}</a>\n\t\t\t\t<d>{_s0}</d>\n\t\t\t</elem>\n'
	for row in data.itertuples():
		fid = str(row[2])
		f0 = ','.join(str(val) for val in row[3:6])
		s0 = ','.join(str(val) for val in row[6:9])
		data_to_write.append(template.format(_id=fid, _f0=f0, _s0=s0))

	data_to_write.append("\t\t</ElementData>\n")
	data_to_write.append('\t</MeshData>\n')

	s = ""
	s = s.join(data_to_write)

	return s


def add_fibers_to_feb(inputs):
	function_name = 'ADD_FIBERS'
	log.log_step("\n== {} ==\n".format(function_name))

	# GET RA Inputs
	path_feb_files = get_path_to_FEB_files(inputs)

	# Get optional Inputs
	path_f_folder = get_optional_input(inputs, 'FIBERS_DATA_FOLDER', function_name)
	path_o_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)

	# Set file name (check if it comes from a "with_properties" or "with_load" folder)

	# Get fiber files
	fibers_files = find_files(path_f_folder,("fileFormat","csv"))

	# Prepare fibers and insert in FEBio
	for p in path_feb_files:
		fname = p[2]
		log.log_substep("Adding fibers to: {}.".format(fname))

		global_output_filename = fname if "load" not in p[0] else "with_load_" + fname 
		
		# Match all existing files:
		matched_fibers = [f for f in fibers_files if fname in f[2]]

		for fibers in matched_fibers:
			f_or = fibers[2].split('_o_')[-1].split('.')[0]
			log.log_substep("Fiber orientation: {}.".format(f_or), indent=2, ind_ch='-')
			output_filename = global_output_filename + "_" + f_or
		
			# Read data and format to create soup (due limitations in bs4, and, since this is pretty much an
			# immutable tag, we will be using it as a string that will be converted to a soup)
			log.log_message("Reading csv file.")
			df_fibers = pd.read_csv(fibers[0], header=None)
			# meshdata = format_data_to_write(df_fibers)

			febio_soup = FEBio_xml_parser.FEBio_xml_parser(p[0])
			# meshdata_soup = febio_soup.parse(meshdata)
			# febio_soup.add_tag(meshdata)
			febio_soup.add_fibers(df_fibers)
			# Make directory for new file
			_path = join(path_o_folder,output_filename)
			Path(_path).mkdir(parents=True, exist_ok=True)
			febio_soup.write_feb(_path, output_filename)