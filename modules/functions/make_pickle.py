
import csv
import re
import pandas as pd
from os.path import join, exists
from os import mkdir
from os import remove as remove_file
from sys import stdout 
import zipfile

from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
from .. sys_functions.find_files_in_folder import find_files



# define headers
HEADER_PAR = ['a','b']
HEADER_TIM = ['time']
HEADER_STR = ['sx','sy','sz','sxy','sxz','syz']
HEADER_DIS = ['ux','uy','uz']
HEADER_POS = ['x','y','z']
HEADER_FAL = ['fail']

# define last simulation timestamp
LAST_TIMESTAMP = 0.2

def includeNodeNumberInHeader(header):
	clock = 0
	counter = 0
	new_header = []
	for _ in range(8):
		for i in range(len(header)):
			if clock == 0:
				counter += 1
			new_header.append(header[i] + "_" + str(counter))
			
			clock = clock + 1 if clock < 2 else 0
	return new_header

def create_header():
	a = HEADER_PAR
	a.extend(HEADER_TIM)
	a.extend(HEADER_FAL)
	a.extend(includeNodeNumberInHeader(HEADER_POS))
	a.extend(includeNodeNumberInHeader(HEADER_DIS))
	a.extend(HEADER_STR)
	return a

def decode_data(file):
	data = {}
	with open(file, 'r') as datafile:
		for line in datafile:
			if line.find("*Time") != -1:
				time = float(line.split("=")[1])
				data[time] = []
			elif line.find("*") == -1:
				# if line.find(","):
				# 	line = line.replace(",","")

				# line.replace("\\n","")
				line = re.sub(",", '', line)
				line = re.sub("\n", '', line)
				str_data = line[2:].split(" ")

				data[time].extend([float(s) for s in str_data])
	return data

def get_param_val(file):
	params = {}
	with open(file, 'r',newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for i, row in enumerate(spamreader):
			params[i] = [float(v) for v in row[-1].split(";")]
	return params

def compile_data(files):
	frames = []
	total_files = len(files)
	for i, (fp, _, _) in enumerate(files):
		ndf = pd.read_pickle(fp)
		frames.append(ndf)
		print("compiled pickle: ", (i + 1) /total_files)
		df = pd.concat(frames, ignore_index=True)
	return df

def make_pickle(inputs):
	print("== MAKE PICKLE ==")

	# Get files
	print("-- Getting input files")
	inp_folder = inputs[POSSIBLE_INPUTS.INPUT_FOLDER]
	out_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]

	temp_folder = join(inp_folder,"tmp")
	if not exists(temp_folder):
		mkdir(temp_folder)

	# zipfile handler
	zipf = zipfile.ZipFile(join(out_folder,'zipped_data.zip'), 'w', zipfile.ZIP_DEFLATED)

	files = find_files(inp_folder, ("fileFormat","txt"))
	csv_files = find_files(inp_folder, ("fileFormat","csv"))

	for (fp, ff, fn) in csv_files:
		if fn.find('modified_param_log') != -1:
			param_file = (fp, ff, fn)
		else:
			raise(AssertionError("modified_params_log file not found."))

	# -----------------
	# organize files:
	str_files = {}
	dis_files = {}
	pos_files = {}
	print("-- Sorting files")
	for (fp, ff, fn) in files:
		fs = fn.split("_")
		if len(fs) == 2:
			key = "initial"
		else:
			key = int(fs[-1])
		
		if fs[0] == 'displacement':
			dis_files[key] = (fp, ff, fn)
		elif fs[0] == 'stress':
			str_files[key] = (fp, ff, fn)
		elif fs[0] == 'position':
			pos_files[key] = (fp, ff, fn)
	files = [str_files, dis_files, pos_files]

	# -----------------
	# Determining critial values
	print("-- Checking lengths")
	lengths = [len(l) for l in files]
	idxmin = lengths.index(min(lengths)) 
	baseDict = files[idxmin]
	baseDictLength = len(baseDict)

	# get param values
	print("-- Getting params")
	params = get_param_val(param_file[0])

	# -----------------
	# create dataframe
	print("-- Creating dataframe")
	header = create_header()
	df = pd.DataFrame(columns=header)
	rowCounter = 0
	fileCounter = 0

	# -----------------
	# creating temporary pickles
	print("-- Filling dataframe")
	for i, key in enumerate(baseDict):

		if key in params:
			str_data = decode_data(str_files[key][0])
			dis_data = decode_data(dis_files[key][0])
			pos_data = decode_data(pos_files[key][0])

			org_keys = sorted(str_data.keys())

			last_timestamp = org_keys[-1]
			failed = 1 if float(last_timestamp) != LAST_TIMESTAMP else 0

			for time in org_keys:
				df.loc[rowCounter] = params[key] + [time] + [failed] + pos_data[time] + dis_data[time] + str_data[time]
				rowCounter += 1

		stdout.write(".")
		stdout.flush()
		if i % 100 == 0 and i != 0:
			# Log
			print("\nBatch: #", fileCounter, "->", i/baseDictLength,"%")
			df.to_pickle(join(temp_folder,"data%s.pickle" % fileCounter))
			# create new instance
			df = pd.DataFrame(columns=header)
			# print(df)
			rowCounter = 0
			fileCounter += 1

		# zip files
		zipf.write(str_files[key][0], arcname="/str/" + str_files[key][1])
		zipf.write(dis_files[key][0], arcname="/dis/" + dis_files[key][1])
		zipf.write(pos_files[key][0], arcname="/pos/" + pos_files[key][1])
		# delete files
		remove_file(str_files[key][0])
		remove_file(dis_files[key][0])
		remove_file(pos_files[key][0])
	df.to_pickle(join(temp_folder,"data%s.pickle" % fileCounter))

	# -----------------
	# creating final pickle
	print("-- Compiling pickle files")
	pickle_files = find_files(temp_folder, ("fileFormat","pickle"))
	df = compile_data(pickle_files)
	df.to_pickle(join(out_folder, "pickle_data.pickle"))
	# delete tpm folder
	remove_file(temp_folder)