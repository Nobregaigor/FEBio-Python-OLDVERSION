from copy import copy
import pandas as pd
from pathlib import Path
from os.path import join

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup


def format_data_to_write(data):
	print("Formating data to write.")
	data_to_write = []
	data_to_write.append("\t<MeshData>\n")
	data_to_write.append('\t\t<ElementData elem_set="Part1" var="mat_axis">\n')
	template = '\t\t\t<elem lid="{_id}">\n\t\t\t\t<a>{_f0}</a>\n\t\t\t\t<d>{_s0}</d>\n\t\t\t</elem>\n'
	for row in data.itertuples():
		fid = str(row[0] + 1)
		f0 = ','.join(str(val) for val in row[3:6])
		s0 = ','.join(str(val) for val in row[6:9])
		data_to_write.append(template.format(_id=fid, _f0=f0, _s0=s0))

	data_to_write.append("\t\t</ElementData>\n")
	data_to_write.append('\t</MeshData>\n')

	# s = ""
	# s = s.join(data_to_write)

	return data_to_write


def add_fibers_to_feb2(inputs):
	print("\n== Adding Fibers ==")

	# Get inputs
	if POSSIBLE_INPUTS.FEB_FILE in inputs:
		path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
		feb_filename = path_to_feb.split("\\")[-1]
		# output_filename = feb_filename if "load" not in path_to_feb.split("\\")[-2] else "with_load_" + feb_filename
		path_feb_files = [(path_to_feb, feb_filename,feb_filename[:-4])]
	else:
		path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER],("fileFormat","feb"))
		feb_filename = path_feb_files[0][2]
		# output_filename = feb_filename if "load" not in inputs[POSSIBLE_INPUTS.INPUT_FOLDER].split("\\")[-1] else "with_load_" + feb_filename

	path_f_folder = inputs[POSSIBLE_INPUTS.FIBERS_DATA_FOLDER]
	path_o_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]

	# Set file name (check if it comes from a "with_properties" or "with_load" folder)

	# Get fiber files
	fibers_files = find_files(path_f_folder,("fileFormat","csv"))

	# Prepare fibers and insert in FEBio
	for p in path_feb_files:
		fname = p[2]
		print("\n--> Adding fibers to:",fname)

		global_output_filename = fname if "load" not in p[0] else "with_load_" + fname 
		
		# Match all existing files:
		matched_fibers = [f for f in fibers_files if fname in f[2]]

			# for f in fibers_files:
			# 	if fname in f[2]:
			# 		fibers = f
			# 		# fibers_files.remove(f)
			# 		break

		for fibers in matched_fibers:
			f_or = fibers[2].split('_o_')[-1].split('.')[0]
			print("\n---> Fiber orientation:",f_or)
			output_filename = global_output_filename + "_" + f_or
		
			# Read data and format to create soup (due limitations in bs4, and, since this is pretty much an
			# immutable tag, we will be using it as a string that will be converted to a soup)
			print("Reading csv file.")
			df_fibers = pd.read_csv(fibers[0], header=None)
			meshdata = format_data_to_write(df_fibers)

			# read FEB file
			print("Reading feb file...")
			with open(p[0], 'r') as no_fiber_FEB_file:
				feb_file_content = no_fiber_FEB_file.readlines()
			
			# For simplicity, mesh data will be inputed as the last element before the closing line of the feb file
			end_file = feb_file_content[-1]
			feb_file_content.pop(-1)
			feb_file_content.extend(meshdata)
			feb_file_content.append(end_file)

			# Make directory for new file
			_path = join(path_o_folder,output_filename)
			Path(_path).mkdir(parents=True, exist_ok=True)

			# write new file:
			print("Writing feb file with fibers...")
			with open(join(_path, output_filename + ".feb"),'w') as with_fibers_file:
				with_fibers_file.writelines(feb_file_content)


			# febio_soup = FEBio_soup(p[0])
			# meshdata_soup = febio_soup.make_soup(meshdata)
			# febio_soup.insert_tag(meshdata_soup)
			# febio_soup.write_feb(_path, output_filename)