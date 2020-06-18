from os import listdir
from os.path import isfile, join, isdir
import sys, getopt
import subprocess

import pandas as pd

def find_files(path_to_folder, condition=None):
	if (condition):
		if (condition[0] == "fileFormat"):
			_l = len(condition[1])
			return [(join(path_to_folder,f), f,f[:-_l - 1]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f)) and f[-_l:] == condition[1]]
		else:
			raise(ValueError("Condition should be a tuple where the first argument is the condition name and the second is its value"))
	else:
		return [(join(path_to_folder,f), f, f.rsplit(".")[0]) for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]



def compile_data(files):
  frames = []
  for (fp, ff, fn) in files:
    ndf = pd.read_pickle(fp)
    frames.append(ndf)

  df = pd.concat(frames)
  return df



if __name__ == "__main__":
  files = find_files('D:\Igor\Research_USF\Python\pickleData')
  print("compiling data")
  df = compile_data(files)
  print(df)
      
