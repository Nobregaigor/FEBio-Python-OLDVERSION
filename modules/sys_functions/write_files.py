from os.path import join
import csv

def write_csv(filename, data, path=None):
	print("Writing csv file:", filename)
	
	filename += ".csv" if filename.find('.csv') < 0 else ''
	filepath = filename if path == None else join(path,filename)

	with open(filepath,"w", newline='') as file:
		csv_file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		try:
			csv_file_writer.writerows(data)
		except:
			raise(ValueError('Content must be an array.'))