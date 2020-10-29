from os import listdir
from os.path import isfile, join, isdir, basename
import sys, getopt
import subprocess

def find_files(path_to_folder, condition=None):
	if (condition):
		if (condition[0] == "fileFormat"):
			_l = len(condition[1])
			return [(join(path_to_folder,f), f,f[:-_l - 1]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f)) and f[-_l:] == condition[1]]
		else:
			raise(ValueError("Condition should be a tuple where the first argument is the condition name and the second is its value"))
	else:
		return [(join(path_to_folder,f), f, f.rsplit(".")[0]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]


def find_folders(path_to_folder, condition=None):
	if (condition):
		if (condition[0] == "has_name"):
			return [(join(path_to_folder,f), f ) for f in listdir(path_to_folder) if isdir(join(path_to_folder, f)) and condition[1] in f]
		else:
			raise(ValueError("Condition should be a tuple where the first argument is the condition name and the second is its value"))
	else:
		return [(join(path_to_folder,f), f, f.rsplit(".")[0]) for f in listdir(path_to_folder) if isdir(join(path_to_folder, f))]


def search_dirs(dir, file_extension, filename=None, files=[]):
	""" Runs a tree search for files with given extension in all folders and subfolders of a given directory"""
	contents = listdir(dir)

	for c in contents:
		abs_path = join(dir, c)

		if isfile(abs_path):
			if abs_path.endswith(file_extension):
				if filename != None:
					if basename(abs_path).find(filename) != -1:
						files.append(abs_path)
				else:
					files.append(abs_path)
		elif isdir(abs_path):
			search_dirs(abs_path, file_extension, filename, files)
		else:
			pass

	return files