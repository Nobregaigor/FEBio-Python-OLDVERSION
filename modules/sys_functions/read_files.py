from bs4 import BeautifulSoup

def read_xml(path_to_file, skip_header=False):
	print("Reading file:", path_to_file)
	with open(path_to_file,"r") as file:
		# Due limitations on bs4 and ISO-8859-1 encoding, skip first line
		try:
			if skip_header == True:
				h = file.readline()
			return BeautifulSoup(file.read(), "xml")
		except:
			print("*** Non-fatal ERROR: xml file provided", path_to_file," could not be converted to soup.")
			return None