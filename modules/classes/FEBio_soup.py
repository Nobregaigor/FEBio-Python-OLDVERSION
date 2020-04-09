from bs4 import BeautifulSoup

class FEBio_soup():
	def __init__(self, path_to_feb_file):
		self.path_to_file = path_to_feb_file

		self.read_content()

		# Main tags:
		self.globals = self.soup.Globals
		self.control = self.soup.Control
		self.material = self.soup.Material
		self.geometry = self.soup.Geometry
		self.loads = self.soup.Loads
		self.boundary = self.soup.Boundary
		self.load_data = self.soup.LoadData
		self.output = self.soup.Output

	def read_content(self):
		print("Creating soup...")
		with open(self.path_to_file,"r") as feb_file:
			# Due limitations on bs4 and ISO-8859-1 encoding, skip first line
			self.header = feb_file.readline()
			self.soup = BeautifulSoup(feb_file.read(), "xml")

	def get_prettified(self):
		return self.soup.prettify()
