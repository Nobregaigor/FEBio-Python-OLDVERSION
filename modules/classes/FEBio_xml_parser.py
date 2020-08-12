import xml.etree.ElementTree as ET
from os.path import isfile, join

class FEBio_xml_parser():
	def __init__(self, path_to_feb_file, skip_tag_inspector=False):
		self.path_to_file = path_to_feb_file

		# ET tree reference for paesed xml file
		self.tree = None
		# Tree root reference for paesed xml file
		self.root = None

		# Order in which outer tags should be placed
		self.props_order = ['Module', 'Control', 'Material', 'Globals', 'Geometry', 'Boundary', 'Loads',  'Output', 'LoadData', 'MeshData']
		self.existing_tags = []

		self.was_initialized = False
		self.initialize()

	def __repr__(self):
		return "FEBio_xml_parser(*{!r})".format(self.existing_tags)

	def __len__(self):
		return len(self.existing_tags)

	def initialize(self):
		if not self.was_initialized:
			print("Initializing...")
			print("-Parsing.")
			self.tree = ET.parse(self.path_to_file)
			print("-Rooting.")
			self.root = self.tree.getroot()
			print("-Finding tags.")
			for child in self.root:
				tag_name = child.tag
				if not hasattr(self,tag_name):
					self.set_tag_obj_ref(child)
					print("--Found:", tag_name + ".")
			self.was_initialized = True

	def has_tag(self,tag):
		if hasattr(self,tag) and getattr(self,tag) != None:
			return True
		else:
			return False

	def set_tag_obj_ref(self,tag_elem):
		# This function sets a ref of the tag elem to the main obj
		# It returns true if it is a new tag, otherwise it returns false
		tag_name = tag_elem.tag
		if not hasattr(self,tag_name):
			# Set new attr to obj with ref to tag
			setattr(self,tag_name,tag_elem)
			# Keep control of existing tags
			self.existing_tags.append(tag_name)
			return True
		else:
			return False

	def parse(self, content):
		# Parse from file:
		# Try to parse as string
		if type(content) == str:
			if content.find(":\\") != -1:
				if isfile(content):
					tree = ET.parse(content)
					root = tree.getroot()
			else:
				try:
					tree = None
					root = ET.fromstring(content)
				except:
					raise(ValueError("Content was identified as string, but could not be parsed. Please, verify."))
		elif isinstance(content, ET.ElementTree):
			try:
				tree = content
				root = tree.getroot()
			except:
				raise(ValueError("Content was identified as ElementTree object, but could not get its root. Please, verify."))
		elif isinstance(content, ET.Element):
				tree = None
				root = content
		else:
			raise(ValueError("Content is not file, string or xml tree. Please, verify."))

		return tree, root 

	def add_tag(self, content, branch=None, insert_pos=-1):
		print("Adding tag...")
		# Parse content
		tree, root = self.parse(content)

		# If no branch was given, content is global
		if branch == None:
			tag_name = root.tag
			if not self.has_tag(tag_name):
				if tag_name in self.props_order:
					props_idx = self.props_order.index(tag_name)
					if props_idx == 0:
						insert_pos = 1
					elif props_idx == len(self.props_order) -1:
						insert_pos = -1
					else:
						insert_pos = props_idx
						# for tag_to_find in reversed(self.props_order[:props_idx]):
						# 	print("tag_to_find: ", tag_to_find)
						# 	if tag_to_find in self.existing_tags:
						# 		print("tag_to_find index: ", self.existing_tags.index(tag_to_find))
						# 		curr_loc = self.existing_tags.index(tag_to_find)
						# 		insert_pos = curr_loc + 1 if curr_loc > 1 else 0
						# 		break
					print("Adding: ", tag_name, "props_idx: ", props_idx, "| must add at pos: ", insert_pos)
			else:
				insert_pos = -1

			self.set_tag_obj_ref(root)
			if insert_pos == -1:
				self.root.append(root)
			else:
				self.root.insert(insert_pos, root)

		else:
			if type(branch) == list or type(branch) == tuple:
				a = getattr(self,branch[0])
				b = a.find(branch[1])
				if b != None:
					a = b
			else:
				a = getattr(self,branch)

			# exists = a.find(root.tag)
			# print("exists: ", exists)
			# if exists != None:
			# 	exists.text = root.text
			# else:
			
			if insert_pos == -1:
				a.append(root) # inserts as the last element
			else:
				a.insert(insert_pos, root)

		print("-Added:", root.tag + ".")

	def modify_tag(self, tag, content, branch):

		if type(branch) == list or type(branch) == tuple:
			# a = getattr(self,branch[0])
			# b = a.find(branch[1])
			# while b != None:
			# 	a = getattr(br)
			# if b != None:
			# 	a = b

			first_elem = branch[0]
			branch.pop(0)
			# branch.append(tag)

			if hasattr(self,first_elem):
				a = getattr(self,first_elem) 
				for sr in branch:
					new_a = a.find(sr)
					if new_a != None:
						a = new_a
			# 		print("inter a:", a)
			# print("final a:",a)
					# if hasattr(a,sr) == True:
					# 	a = getattr(a,sr)
					# 	print("new a:", a)
					# else:
					# 	print("*** Warning; Could not get sub_tag", tag, "from", branch[0],". It does not have such sub_tag")
		else:
			a = getattr(self,branch)

		exists = a.find(tag)
		if exists != None:
			exists.text = content
		else:
			a.insert(0,content)
		
		print("exists.text", exists.text)
		
		print('-Modified tag:', tag)

	def get_geometry_data(self):
		nodes = []
		elems = []

		if self.has_tag("Geometry"):
			for node in self.Geometry.find("Nodes").findall("node"): 		# pylint: disable=no-member
				a = [node.get('id')]
				a.extend([float(b) for b in str(node.text).split(",")])
				nodes.append(a)
		
			for all_elems in self.Geometry.findall("Elements"): 				# pylint: disable=no-member
				for elem in all_elems.findall("elem"):
					a = [elem.get("id")]
					a.extend([float(b) for b in str(elem.text).split(",")])
					elems.append(a)

		return nodes, elems

	def add_fibers(self,df_fibers):
		print("Adding fibers...")
		# Create MeshData Element
		mesh_data = ET.Element('MeshData')
		# Create sub-elements for each element set and list first id of each sub-element
		first_ids = []
		elems_ref = []
		max_penta_elem = -1
		for _, var in enumerate(self.Geometry.findall("Elements")):
			# if var.get("type").find("hex") != -1:
			element_set_name = var.get("name")
			element_set_type = var.get("type")
			elems_ref.append(element_set_name)
			first_ids.append(int(var.find("elem").get("id")))
			a = ET.SubElement(mesh_data,"ElementData")
			a.set("elem_set", element_set_name)
			a.set("var", "mat_axis")
			# sum number of penta elements (FEBio cannot have two fiber axis for a hex element connected to a penta element)
			if element_set_type.find("penta") != -1:
				number_of_penta_children = len(var.getchildren())
				max_penta_elem = number_of_penta_children if max_penta_elem == -1 else max_penta_elem + number_of_penta_children

		# get last element with fiber based on number of 
		last_elem_with_fiber = len(df_fibers) - max_penta_elem if max_penta_elem != -1 else len(df_fibers) + 1
		# Create node sub_elements
		l_first_ids = len(first_ids)
		belongs = 0
		# print("i", 0, "belongs", belongs, "elems_ref", elems_ref[belongs])
		local_id = 0
		for i, row in enumerate(df_fibers.itertuples()):
			# if i + 1 > last_elem_with_fiber:
			# 	break
			if l_first_ids > 1 and belongs + 1 < l_first_ids:
				if i + 2 > first_ids[belongs + 1]:
					belongs += 1
					local_id = 0

			local_id += 1
					# print("i", i, "belongs", belongs, "elems_ref", elems_ref[belongs])
					
			# Set fiber info
			# fid = row[0] + int(first_ids[0])
			fid = local_id
			f0 = ','.join(str(val) for val in row[3:6])
			s0 = ','.join(str(val) for val in row[6:9])

			

			# # Specify which element set the fiber belongs
			# if l_first_ids > 2:
			# 	for i in r_first_ids:
			# 		if first_ids[i] <= fid <= first_ids[i+1]:
			# 			belongs = i
			# 			break
			# elif l_first_ids == 2:
			# 	if first_ids[0] <= fid <= first_ids[1]:
			# 		belongs = 0
			# 	else:
			# 		belongs = 1
			# else:
			# 	belongs = 0

			# Create sub-elements
			elem = ET.SubElement(mesh_data[belongs], "elem")
			elem.set("lid",str(fid))
			a = ET.SubElement(elem,"a")
			d = ET.SubElement(elem,"d")

			a.text = f0
			d.text = s0		

		self.root.insert(len(self.existing_tags),mesh_data)

	def indent(self, elem, level=0):
		i = "\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			for e in elem:
				self.indent(e, level+1)
				if not e.tail or not e.tail.strip():
					e.tail = i + "  "
			if not e.tail or not e.tail.strip():
				e.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

	def write_feb(self, path_to_output_folder, file_name):
		file_name = file_name + ".feb" if file_name[-4:] != ".feb" else file_name
		print("Indenting root...")
		self.indent(self.root)
		print("Writing file...")
		self.tree.write(join(path_to_output_folder,file_name),encoding="ISO-8859-1")



# if __name__ == "__main__":
# 	print("hello")


# 	path = "C:\\Users\\IgorNobrega\\University of South Florida\\Mao, Wenbin - Myocardium (organized)\\Active\\Guccione_study\\raw\\myo_tet_4_fine.feb"
# 	material = "C:\\Users\\IgorNobrega\\University of South Florida\\Mao, Wenbin - Myocardium (organized)\\Active\\Guccione_study\\properties\\material.xml"
# 	control = "C:\\Users\\IgorNobrega\\University of South Florida\\Mao, Wenbin - Myocardium (organized)\\Active\\Guccione_study\\properties\\control.xml"

# 	o = FEBio_xml_parser(path)
# 	o.add_tag(material)
# 	o.add_tag(control)

# 	o.add_tag("<a>   500  </a>", branch=("Material","material1"))

# 	nodes, elems = o.get_geometry_data()
# 	print(len(elems))
