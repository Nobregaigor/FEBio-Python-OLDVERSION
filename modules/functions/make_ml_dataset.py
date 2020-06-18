
import csv
import re
import pandas as pd
from os.path import join

from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
from .. sys_functions.find_files_in_folder import find_files

# define headers
HEADER_PAR = ['a','b']
HEADER_TIM = ['time']
HEADER_STR = ['sx','sy','sz','sxy','sxz','syz']
HEADER_DIS = ['ux','uy','uz']
HEADER_POS = ['x','y','z']

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

def make_ml_dataset(inputs):
	print("== MAKE ML DATASET ==")

	# Get files
	print("-- Getting input files")
	inp_folder = inputs[POSSIBLE_INPUTS.INPUT_FOLDER]
	out_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]

	files = find_files(inp_folder, ("fileFormat","txt"))
	csv_files = find_files(inp_folder, ("fileFormat","csv"))

	for (fp, ff, fn) in csv_files:
		if fn.find('modified_param_log') != -1:
			param_file = (fp, ff, fn)
		else:
			raise(AssertionError("modified_params_log file not found."))

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

	print("-- Checking lengths")
	lengths = [len(l) for l in files]
	idxmin = lengths.index(min(lengths)) 
	baseDict = files[idxmin]
	baseDictLength = len(baseDict)

	# get param values
	print("-- Getting params")
	params = get_param_val(param_file[0])
	for i in range(10):
		print("key:", i, "a,b:", params[i])
	# print(params)

	# create dataframe
	print("-- Creating dataframe")
	header = columns=create_header()
	df = pd.DataFrame(columns=header)
	rowCounter = 0
	fileCounter = 0
	for i, key in enumerate(baseDict):

		if key in params:
			str_data = decode_data(str_files[key][0])
			dis_data = decode_data(dis_files[key][0])
			pos_data = decode_data(pos_files[key][0])

			for time in str_data.keys():
				df.loc[rowCounter] = params[key] + [time] + pos_data[time] + dis_data[time] + str_data[time]
				rowCounter += 1


		if i % 100 == 0 and i != 0:
			print("Batch: #", fileCounter, "->", i/baseDictLength,"%")
			# show
			print(df)
			print("...")
		# save 
			df.to_pickle(join(out_folder,"data%s.pickle" % fileCounter))
			# create new instance
			df = pd.DataFrame(columns=header)
			# print(df)
			rowCounter = 0
			fileCounter += 1
	

	# for key in str_files:


	# for i, time in enumerate(data):
	# 	df.loc[i] = [time] + data[time]
	# 	# print(len([time] + data[time]))

	print(df)

	df.to_pickle(join(out_folder,"data%s.pickle" % fileCounter))