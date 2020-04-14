from bs4 import BeautifulSoup
from os.path import join
from prettierfier import prettify_xml

class FEBio_soup():
	def __init__(self, path_to_feb_file):
		self.path_to_file = path_to_feb_file

		# --------------------
		# Initialize object
		self.read_content()

		# --------------------
		# Set main tags:
		# Globals:
		self.globals = self.soup.Globals
		self.control = self.soup.Control
		self.loads = self.soup.Loads
		self.boundary = self.soup.Boundary
		self.load_data = self.soup.LoadData
		self.output = self.soup.Output
		# Material:
		self.materials = self.soup.Material.find_all("material") if self.soup.Material != None else None
		self.material = self.soup.Material.material if self.soup.Material != None else None
		# Geometry
		self.geometry = self.soup.Geometry
		self.nodes = self.soup.Geometry.Nodes if self.soup.Geometry != None else None
		self.elements = self.soup.Geometry.Elements if self.soup.Geometry != None else None
		self.node_sets = self.soup.Geometry.find_all("NodeSet") if self.soup.Geometry != None else None
		self.surfaces = self.soup.Geometry.find_all("Surface") if self.soup.Geometry != None else None


	#############################
	# general methods
	#############################

	# Method that reads and creates a soup from a xml content (path to file given from object)
	def read_content(self):
		print("Creating soup.")
		with open(self.path_to_file,"r") as feb_file:
			# Due limitations on bs4 and ISO-8859-1 encoding, skip first line
			self.header = feb_file.readline()
			self.soup = BeautifulSoup(feb_file.read(), "xml")

	# Method that transforms soup to string in a pretty manner
	def get_prettified(self):
		print("prettifying soup.")
		content = prettify_xml(self.soup.prettify())
		content = self.header.rstrip() + content[content.find(">")+1:]
		# print(content)
		return content

	# Method that transforms an xml string into a soup content
	def make_soup(self,content):
		print("Making content a soup.")
		# Convert content to a soup (should be in xml format)
		if not isinstance(content, BeautifulSoup): # If content is not already a BeautifulSoup
			try:
				content = BeautifulSoup(content, "xml")
				return content
			except:
				raise(ValueError("Content provided cannot be converted to BeautifulSoup"))

	#############################
	# Modify tag methods
	#############################

	# Method that adds a tag to main soup and set a new attr
	def add_tag(self, tag, content, insert_pos=1):
		print("Adding tag", tag, "to FEBio_soup.")
		if hasattr(self,tag):
			print("*** Warning: FEBio_soup already has tag", tag, ". Changing it with change_tag_content.")
			self.change_tag_content(tag,content)
		else:
			# Convert content to a soup (should be in xml format)
			content = self.make_soup(content)

			# Create new tag and insert the tag content into it
			new_tag = self.soup.new_tag(tag)
			new_tag.insert(0,content)

			# Insert new tag in main soup and create an attr to the FEBio_soup to ref this new tag
			self.soup.febio_spec.insert(insert_pos, new_tag)
			setattr(self,tag,self.soup.febio_spec.find(tag))

	# Method to remove a tag from main soup
	def remove_tag(self,tag,sub_tag=None,_all=False):
		print("Removing tag", tag,"from FEBio_soup.")
		# Find if tag exists
		if not _all:
			tag = self.soup.find(tag)
			if tag:
				tag.decompose()
		else:
			tags = self.soup.find_all(tag)
			if tags:
				for tag in tags:
					tag.decompose()

	# Method to change the content of a given tag from main soup
	def change_tag_content(self, tag, content):
		print("Changing content from tag", tag,"at FEBio_soup.")
		if not hasattr(self,tag):
			print("*** Warning: FEBio_soup does not have tag", tag, ". Adding it to the main soup.")
			self.add_tag(tag,content)
		else:
			_tag = getattr(self,tag)
			_tag.replace_with(self.make_soup(content))

	#############################
	# Modify attributes methods
	#############################

	# Metho that gets the attr_value and attr_ref from requested tag and attr
	def get_attr(self, tag, attr, sub_tags=None, is_search=False):
		print("Getting attr", attr, ", from tag", tag, ".")
		# tag is the tag of the FEBio_soup object
		# attr is the attribute from the tag
		# sub_tags is the '[path,to,desired,tag]' from outter to inner tags

		if sub_tags != None:
			first_elem = sub_tags[0]
			sub_tags.pop(0)
			sub_tags.append(tag)
		else:
			first_elem = tag

		if hasattr(self,first_elem):
			_tag = getattr(self,first_elem) 
			if sub_tags != None:
				for sr in sub_tags:
					if hasattr(_tag,sr):
						_tag = getattr(_tag,sr)
					else:
						print("*** Warning; Could not get sub_tag", _tag, "from", tag,". It does not have such sub_tag")
			if attr in _tag.attrs:
				return _tag[attr], _tag
			else:
				if not is_search:
					print("*** Warning; Could not get attr. FEBio_soup ", tag, "does not have attr:", attr)
				return None, _tag
		else:
			print("*** Warning; Could not get tag. FEBio_soup does not have tag:", tag)
			return None, None

	# Method that adds an attr with a given value to a given tag. Gets ref rom get_attr
	def add_attr(self, tag, attr, value, sub_tags=None):
		print("Adding attr", attr, "to tag:", tag,".")
		# Check if there is an attr before adding
		_attr_value, _attr_ref = self.get_attr(tag, attr, sub_tags, is_search=True)
		if _attr_ref != None and _attr_value != None:
			print("*** Warning: tag", tag, "already has attr with value:", _attr_value, ". Replacing it with change_attr")
			self.change_attr(_attr_ref, attr, value, is_ref=True)
		else:
			_attr_ref[attr] = value

	# Method that removes an attr from a given tag. Gets ref from get_attr
	def remove_attr(self, tag, attr, sub_tags=None):
		print("Removing attr", attr, "from tag", tag, ".")
		_attr_value, _attr_ref = self.get_attr(tag, attr, sub_tags)
		if _attr_ref != None:
			del _attr_ref[attr]

	# General method to modify an attribute, if ref and attr exists. Gets ref from get_attr
	def change_attr(self,tag, attr, value, sub_tags=None, is_ref=False):
		print("Changing attr:", attr,", in tag:", tag)
		# tag is the tag of the FEBio_soup object
		# attr is the attribute tag that will be modified

		if is_ref:
			attr_tag = tag
		else:
			_, attr_tag = self.get_attr(tag,attr,sub_tags)
		attr_tag[attr] = value

	# Method that uses change_attr directly to the material tag in main soup. Uses change_attr
	def change_attr_in_material(self,attr,value):
		self.change_attr("material",attr,value)

	#############################
	# Writing methods
	#############################

	# Method that writes the pretified version (required to be a string) of the main soup
	def write_feb(self,path_to_output_folder, file_name):
		print("Writing feb.")
		with open(join(path_to_output_folder,file_name), 'w') as file:
			# file.write(self.header)
			file.write(self.get_prettified())