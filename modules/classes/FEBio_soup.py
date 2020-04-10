from bs4 import BeautifulSoup
from os.path import join
from prettierfier import prettify_xml

class FEBio_soup():
	def __init__(self, path_to_feb_file):
		self.path_to_file = path_to_feb_file

		self.read_content()

		# Main tags:
		self.globals = self.soup.Globals
		self.control = self.soup.Control
		self.materials = self.soup.Material.find_all("material") # in case there is more than one material
		self.material = self.soup.Material.material
		self.geometry = self.soup.Geometry
		self.nodes = self.soup.Geometry.Nodes
		self.elements = self.soup.Geometry.Elements
		self.node_sets = self.soup.Geometry.find_all("NodeSet")
		self.surfaces = self.soup.Geometry.find_all("Surface")
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
		content = prettify_xml(self.soup.prettify())
		content = self.header.rstrip() + content[content.find(">")+1:]
		# print(content)
		return content

	#############################
	# Modify attributes methods
	#############################

	# General method to modify an attribute, if ref and attr exists
	def change_attr(self,ref,attr,value,sub_refs=None):
		# Ref is the tag of the FEBio_soup object
		# atr is the attribute tag that will be modified

		if sub_refs != None:
			first_elem = sub_refs[0]
			sub_refs.pop(0)
			sub_refs.append(ref)
		else:
			first_elem = ref

		print(first_elem)
		print(sub_refs)
		# Check first elem:
		if hasattr(self,first_elem):
			_ref = getattr(self,first_elem) 
			if sub_refs != None:
				for sr in sub_refs:
					if hasattr(_ref,sr):
						_ref = getattr(_ref,sr)
					else:
						print("*** Warning; Could not change attr.", _ref, "does not have ref:", ref)
			if attr in _ref.attrs:
				_ref[attr] = value
			else:
				print("*** Warning; Could not change attr. FEBio_soup ", ref, "does not have attr:", attr)
		else:
			print("*** Warning; Could not change attr. FEBio_soup does not have ref:", ref)

	def change_attr_in_material(self,attr,value):
		self.change_attr("material",attr,value)

	def write_feb(self,path_to_output_folder, file_name):
		with open(join(path_to_output_folder,file_name), 'w') as file:
			# file.write(self.header)
			file.write(self.get_prettified())

	
		# 				print("error")
				
		# 		if at


		
		# if hasattr(self,ref):
		# 	_ref = getattr(self,ref) 
		# 	if sub_refs != None:
		# 		for sr in sub_refs:
		# 			if hasattr(_ref,sr):
		# 				_ref = getattr(self,ref) 
		# 			else: