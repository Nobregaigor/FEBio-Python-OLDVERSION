import subprocess
from difflib import get_close_matches as close_matches
from ast import literal_eval

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def calculate_fibers(inputs):
	function_name = 'CALCULATE_FIBERS'
	log.log_step("\n== {} ==\n".format(function_name))
	
	# Get inputs
	file_to_calculate = get_optional_input(inputs, 'FEB_NAME', function_name)
	geom_d_folder = get_optional_input(inputs, 'GEOMETRY_DATA_FOLDER', function_name)
	path_o_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)
	path_m_folder = get_optional_input(inputs, 'PATH_TO_MATLAB_FOLDER', function_name)
	matlab_params = get_optional_input(inputs, 'MATLAB_PARAMS', function_name)

	# eval matlab params
	matlab_params = literal_eval(matlab_params)

	# Get avaiable files 
	files = find_files(geom_d_folder,("fileFormat","csv"))

	# Get only needed files (if user did not requested all)
	if file_to_calculate != "all":
		files = [f for f in files if f[1].find(file_to_calculate) != -1]

	nodes_files = [f for f in files if f[1].find("_nodes") != -1 and f[1].find("hexbase") == -1]  #and f[1].find("hex") == -1]
	elems_files = [f for f in files if f[1].find("_elems") != -1 and f[1].find("hexbase") == -1]  #and f[1].find("hex") == -1]

	# nodes_files_hex = [f for f in files if f[1].find("_nodes") != -1 and f[1].find("hex") != -1]
	# elems_files_hex = [f for f in files if f[1].find("_elems") != -1 and f[1].find("hex") != -1]
	nodes_files_hexbase = [f for f in files if f[1].find("_nodes") != -1 and f[1].find("hexbase") != -1]
	elems_files_hexbase = [f for f in files if f[1].find("_elems") != -1 and f[1].find("hexbase") != -1]

	for node_file in nodes_files:
		fname = node_file[2].split("_nodes")[0]
		log.log_substep("Calculating fibers for: {}.".format(fname))

		mesh_type = "tet" if fname.find("tet") != -1 else "hex" # determine sif file is hex or tet

		if mesh_type == "hex":
			log.log_message("-matching hex")
			if len(nodes_files_hexbase) > 1:
				tet_nodes = [f for f in nodes_files_hexbase if len(close_matches(fname, [f[2].split("_nodes")[0].replace("hexbase","")])) > 0][0]
				tet_elems = [f for f in elems_files_hexbase if len(close_matches(fname, [f[2].split("_elems")[0].replace("hexbase","")])) > 0][0]
			else:
				tet_nodes = nodes_files_hexbase[0]
				tet_elems = elems_files_hexbase[0]
			hex_nodes = node_file
			hex_elems = [f for f in elems_files if f[2].split("_elems")[0] == fname][0]
		else:
			log.log_message("-matching tet")
			tet_nodes = node_file
			tet_elems = [f for f in elems_files if f[2].split("_elems")[0] == fname][0]
			hex_nodes = tet_nodes
			hex_elems = tet_elems


		theta_endo = matlab_params['endo']
		theta_epi = matlab_params['epi']

		log.log_message("Theta_endo: {}.".format(theta_endo))
		log.log_message("Theta_epi: {}.".format(theta_epi))


		params = "'"+ tet_nodes[0] + "'" + ',' + "'"+ tet_elems[0] + "'" + ',' + \
			"'" + hex_nodes[0] + "'" + ',' + "'" + hex_elems[0] + "'" + ',' + \
			str(theta_endo) + ',' + str(theta_epi) + ',' + \
			"'" + path_o_folder + "\\" + fname + "'"

		log.log("Openning MATLAB...", bold=True)
		res = subprocess.call([
		"matlab.exe",
		"-wait",
		"-nodisplay",
		"-nojvm",
		"-nosplash",
		"-nodesktop",
		'/r',
		'"cd'+ " '" + path_m_folder + "'; " + "calc_fibers("+params+");" + ' exit"'
		])

		if res != 0:
			print(res)