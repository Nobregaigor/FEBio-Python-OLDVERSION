from os import listdir
from os.path import isfile, join
import sys, getopt
import subprocess



def find_files(path_to_folder, condition=None):
	if (condition):
		if (condition[0] == "fileFormat"):
			_l = len(condition[1])
			return [(f,f[:-_l]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f)) and f[-_l:] == condition[1]]
		else:
			raise(ValueError("Condition should be a tuple where the first argument is the condition name and the second is its value"))
	else:
		return [(f,f.rsplit(".")[0]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]