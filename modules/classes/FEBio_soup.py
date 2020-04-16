from bs4 import BeautifulSoup
from os.path import join
from prettierfier import prettify_xml

class FEBio_soup():
	def __init__(self, path_to_feb_file, skip_tag_inspector=False):
		self.path_to_file = path_to_feb_file

		self.skip_tag_inspector = skip_tag_inspector

		# --------------------
		# Set main tags:
		# Globals:
		self.globals = None
		self.control = None
		self.loads = None
		self.boundary = None
		self.load_data = None
		self.output = None
		# Material:
		self.materials = None
		self.material = None
		# Geometry
		self.geometry = None
		self.nodes = None
		self.elements = None
		self.node_sets = None
		self.surfaces = None

		# Order in which outer tags should be placed
		self.props_order = ['control', 'material', 'globals', 'geometry', 'boundary', 'loads',  'output', 'loaddata', 'meshdata']
		self.existing_tags = None

		# --------------------
		# Initialize object
		self.was_initialized = False
		self.initialize()


	#############################
	# general methods
	#############################

	def initialize(self):
		if not self.was_initialized:
			self.read_content()
			# if self.skip_tag_inspector == False:
			self.set_tags_obj_ref(is_initializing=True)				
			self.was_initialized = True
		else:
			pass

	# Method that reads and creates a soup from a xml content (path to file given from object)
	def read_content(self):
		print("Creating soup.")
		with open(self.path_to_file,"r") as feb_file:
			# Due limitations on bs4 and ISO-8859-1 encoding, skip first line
			self.header = feb_file.readline()
			self.soup = BeautifulSoup(feb_file.read(), "xml")

	def update_existing_tags(self):
		self.existing_tags = list(tag.name for tag in self.soup.febio_spec.find_all() if tag.parent.name is self.soup.febio_spec.name)
		self.l_existing_tags = [a.lower() for a in self.existing_tags]

	def set_tags_obj_ref(self, is_initializing=False):
		if is_initializing:
			print("Setting attributes:")
		else:
			print("Searching for new attr to create ref in FEBio_soup.")
		if self.globals == None:
			_globals = self.soup.Globals
			if _globals != None:
				print("- Found: globals")
				self.globals = _globals
		if self.control == None:
			_control = self.soup.Control
			if _control != None:
				print("- Found: control")
				self.control = _control
		if self.boundary == None:
			_boundary = self.soup.Boundary
			if _boundary != None:
				print("- Found: boundary")
				self.boundary = _boundary
		if self.loads == None:
			_loads = self.soup.Loads
			if _loads != None:
				print("- Found: loads")
				self.loads = _loads
		if self.output == None:
			_output = self.soup.Output
			if _output != None:
				print("- Found: output")
				self.output = _output
		if self.materials == None:
			materials = self.soup.Material.find_all("material") if self.soup.Material != None else None
			if materials != None:
				print("- Found: materials")
				self.materials = materials
		if self.material == None:
			material = self.soup.Material.material if self.soup.Material != None else None
			if material != None:
				print("- Found: material")
				self.material = material
		if self.geometry == None:
			_geometry = self.soup.Geometry
			if _geometry != None:
				print("- Found: geometry")
				self.geometry = _geometry
		if self.nodes == None:
			nodes = self.soup.Geometry.Nodes if self.soup.Geometry != None else None
			if nodes != None:
				print("- Found: nodes")
				self.nodes = nodes
		if self.elements == None:
			elements = self.soup.Geometry.Elements if self.soup.Geometry != None else None
			if elements != None:
				print("- Found: elements")
				self.elements = elements
		if self.node_sets == None:
			node_sets = self.soup.Geometry.find_all("NodeSet") if self.soup.Geometry != None else None
			if node_sets != None:
				print("- Found: node_sets")
				self.node_sets = node_sets
		if self.surfaces == None:
			surfaces = self.soup.Geometry.find_all("Surface") if self.soup.Geometry != None else None
			if surfaces != None:
				print("- Found: surfaces")
				self.surfaces = surfaces

		self.update_existing_tags()

	def check_if_file_can_run(self):
		# Make sure that it has <Module type="solid" />
		if self.soup.find("Module") == None:
			self.insert_tag(BeautifulSoup('<Module type="solid" />', "xml"), insert_pos=1, check_input_order=False)
		# Make sure that material has mat="1"
		self.add_attr('elements','mat',"1")

	# Method that transforms soup to string in a pretty manner
	def get_prettified(self):
		self.check_if_file_can_run()
		print("prettifying soup.")
		# soup = self.soup.prettify()
		print("pretifying xml.")
		# content = prettify_xml(str(self.soup))
		content = str(self.soup)
		content = self.header.rstrip() + content[content.find(">")+1:]
		# print(content)
		return content

	# Method that transforms an xml string into a soup content
	def make_soup(self,content):
		# Convert content to a soup (should be in xml format)
		if not isinstance(content, BeautifulSoup): # If content is not already a BeautifulSoup
			try:
				print("Making content a soup.")
				content = BeautifulSoup(content, "xml")
				return content
			except:
				raise(ValueError("Content provided cannot be converted to BeautifulSoup"))
		else:
			return content 

	#############################
	# Modify tag methods
	#############################

	# Method that adds a tag to main soup and set a new attr
	def add_tag(self, tag, content, insert_pos=1):
		print("Adding tag", tag, "to FEBio_soup.")
		if hasattr(self,tag.lower()) and getattr(self,tag.lower()) != None:
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
		content = self.make_soup(content)
		if not hasattr(self,tag.lower()):
			print("*** Warning: FEBio_soup does not have tag", tag, ". Adding it to the main soup.")
			self.add_tag(tag,content)
		else:
			_tag = getattr(self,tag.lower())
			if _tag == None:
				print("*** Warning: FEBio_soup does not have tag", tag, ". Adding it to the main soup.")
				self.add_tag(tag,content)
			else:
				if content != None:
					_tag.contents[0].replace_with(content)

	# Method to insert a blob of tag with content
	def insert_tag(self,tag_with_content, insert_pos=1, check_input_order=True):
		_tag = tag_with_content.findChildren()[0]
		_tag_name = _tag.name.lower()
		print("Inserting tag:", _tag.name, " in soup.")
		if hasattr(self,_tag_name) and getattr(self,_tag_name) != None:
			print("*** Warning: FEBio_soup already has tag:", _tag_name,". Changing its content with change_tag_content")
			self.change_tag_content(_tag_name, tag_with_content)
		else:
			if check_input_order is True:		
				if _tag_name in self.props_order:
					props_idx = self.props_order.index(_tag_name)
					if props_idx == 0:
						insert_pos = 1
					elif props_idx == len(self.props_order) -1:
						insert_pos = -1
					else:
						# l_existing_tags = [a.lower() for a in self.existing_tags]
						for tag_to_find in reversed(self.props_order[:props_idx]):
							if tag_to_find in self.l_existing_tags:
								insert_pos = self.l_existing_tags.index(tag_to_find) + 4 # Not sure why +4
								break

			self.soup.febio_spec.insert(insert_pos, tag_with_content)

			if (hasattr(self,_tag_name) and getattr(self,_tag_name) == None):
				setattr(self,_tag_name, getattr(self.soup, _tag.name))
				print("- Found:", _tag_name)
			
			if (hasattr(self,_tag_name) and getattr(self,_tag_name) == None) or _tag_name in self.props_order:
				self.update_existing_tags()

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
		# print("Changing attr:", attr,", in tag:", tag)
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
	# Extracting methods
	#############################

	def get_geometry_data(self):
		nodes = []
		elems = []
		for node in self.nodes.findChildren():
			a = [node['id']]
			a.extend([float(b) for b in str(node.string).split(",")])
			nodes.append(a)

		for elem in self.elements.findChildren():
			a = [elem['id']]
			a.extend([float(b) for b in str(elem.string).split(",")])
			elems.append(a)


		return nodes, elems

	#############################
	# Writing methods
	#############################

	# Method that writes the pretified version (required to be a string) of the main soup
	def write_feb(self,path_to_output_folder, file_name):
		file_name = file_name + ".feb" if file_name[-4:] != ".feb" else file_name
		with open(join(path_to_output_folder,file_name), 'w') as file:
			prefitied_soup = self.get_prettified()
			print("Writing feb.")
			file.write(prefitied_soup)