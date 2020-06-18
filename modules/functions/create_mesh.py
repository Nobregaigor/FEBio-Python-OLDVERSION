import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import xml.etree.ElementTree as ET
from os.path import isfile, join
from os import getcwd

def centered_ellipse(a,b, res):
	xs = np.linspace(-b,b,res)
	ys = np.zeros(res)
	ys2 = np.zeros(res)

	for i, x in enumerate(xs):
		ys[i] = np.sqrt(1 - x**2 / b**2) * a
		ys2[i] = np.sqrt(1 - x**2 / b**2) * -a

	
	return np.concatenate((xs,xs)), np.concatenate((ys,ys2))

def quarter_centered_ellipse(a,b, yrange, res):
	yspace = np.linspace(yrange[0], yrange[1], res)
	# xspace = np.linspace(0, b, res)

	# ys = np.zeros(res)
	xs = np.zeros(res)

	for i, val in enumerate(yspace):
		xs[i] = np.sqrt(1 - val**2 / a**2) * b
		# ys[i] = np.sqrt(1 - xspace[i]**2 / b**2) * a

	return (xs, yspace)

def create_ref_nodes_in_plane(a, b, ymax, thickness, vertical_res, horizontal_res):
	
	lines = []
	dx = thickness / horizontal_res if horizontal_res != 0 else thickness
	for i, val in enumerate(range(horizontal_res + 1)):
		_a = a + dx * i
		_b = b - dx * i

		lines.append(quarter_centered_ellipse(_a,_b, [_a, ymax], vertical_res))

	return lines

def revolute_nodes(lines2d, res):
	
	def rotation_matrix(theta, axis='z'):
		if axis == 'z':
			return np.array([
				[np.cos(theta), np.sin(theta), 0],
				[-np.sin(theta), np.cos(theta), 0],
				[0, 0, 1],
				]
			)
		elif axis == 'y':
			return np.array([
				[np.cos(theta), 0, -np.sin(theta)],
				[0, 1, 0],
				[np.sin(theta), 0, np.cos(theta)],
				]
			)

	sections = []
	dtheta = 360 / res
	nodes = {}
	node_count = 1
	for i in range(res + 1):
		theta = i * dtheta
		layers = []
		for line in lines2d:
			line_3d = []

			for i in range(len(line[0])):
				point3d = np.array([line[0][i], 0, line[1][i]])

				rotated_point3d = np.matmul(point3d, rotation_matrix(np.radians(theta)))
				nodes[node_count] = rotated_point3d

				line_3d.append(node_count)
				node_count += 1

			layers.append(line_3d)
		sections.append(layers)
	
	return sections, nodes

def hexalise(shape):
	def get_elem(i,j,k,shape):
		if i != len(shape) -1:
			i2 = i + 1
		else:
			i2 = 0

		return(np.array([
			shape[i2][j][k+1],		# P6
			shape[i][j][k+1],			# P2
			shape[i][j+1][k+1],		# P4
			shape[i2][j+1][k+1],	# P8
			shape[i2][j][k],			# P5
			shape[i][j][k], 			# P1
			shape[i][j+1][k],			# P3
			shape[i2][j+1][k],		# P7
		]))
	
	elements = {}
	elem_count = 1

	n_sections = len(shape)
	for i in range(len(shape)): # sections
		for j in range(len(shape[i]) -1): # layers
			for k in range(len(shape[i][j]) -1): # points
				elem = get_elem(i,j,k,shape)


				elements[elem_count] = elem
				elem_count += 1

	return elements

def write_geometry(nodes, elems, file_name, path_to_output_folder):

	# Create MeshData Element
	geometry = ET.Element('Geometry')
	tree = ET.ElementTree(geometry)
	nodes_tag = ET.SubElement(geometry,"Nodes")
	nodes_tag.set("name","Object01")
	elems_tag = ET.SubElement(geometry,"Elements")
	elems_tag.set("type","hex8")
	elems_tag.set("name","Part1")
	
	# Add nodes data
	for node in nodes:
		# Create sub-elements
		_node = ET.SubElement(nodes_tag, "node")
		_node.set("id",str(node))
		_node.text = ",".join([str(x) for x in nodes[node]])

	# Add elems data
	for elem in elems:
		# Create sub-elements
		_elem = ET.SubElement(elems_tag, "elem")
		_elem.set("id",str(elem))
		_elem.text = ",".join([str(x) for x in elems[elem]])

	# print(ET.tostring(geometry))
	# root = ET.ElementTree(geometry)
	# print(root)
	indent(tree.getroot())
	tree.write(join(path_to_output_folder,file_name),encoding="ISO-8859-1")

def indent(elem, level=0):
		i = "\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			for e in elem:
				indent(e, level+1)
				if not e.tail or not e.tail.strip():
					e.tail = i + "  "
			if not e.tail or not e.tail.strip():
				e.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i


# Second approach

def cubic_regression(line):
	return np.polyfit(line[0], line[1], 3)

def regressed_value(x, coeffs):
	val = 0
	for c in enumerate(coeffs):
		val += x ** (len(coeffs) - c)
	return val




##############################
# MACROS
#################################

# Geometry data
A = -65
B = 25
YMAX = 20
THICKNESS = -10 # negative to match equation

# Mesh data
VERTICAL_RES = 60
N_LAYERS = 4 # from endo to epi, not including endo
CIRCUNFERENTIAL_RES = 30

######################################

if __name__ == "__main__":

	# endo_points = quarter_centered_ellipse(-65,25, [-65, 20], 50)
	# epid_points = quarter_centered_ellipse(-75,35, [-75, 20], 50)

	# CREATING
	print("Creating references...")
	references = create_ref_nodes_in_plane(A, B, YMAX, THICKNESS, VERTICAL_RES, N_LAYERS)




	print("Creating Shape...")
	shape, nodes = revolute_nodes(references, CIRCUNFERENTIAL_RES)
	# Shape: Sections -> Layers -> Points
	print("Hexalizing...")
	elems = hexalise(shape)

	print("Writing File...")
	write_geometry(nodes,elems,"geometry.feb", getcwd())


	print("Plotting...")
	################## 
	# Plot
	##################

	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	ax2 = fig.add_subplot(122)

	# for line in references:
	# 	ax1.scatter(line[0],line[1])

	for layer in shape[0]:
		xs = np.zeros(len(layer))
		zs = np.zeros(len(layer))
		for i, point in enumerate(layer):
			xs[i] = nodes[point][0]
			zs[i] = nodes[point][2]

		ax1.scatter(xs,zs)

	for section in shape:
		for layer in section:
			for i in np.linspace(0,len(layer) -1, 10):
				point = layer[int(np.floor(i))]
				ax2.scatter(nodes[point][0],nodes[point][1])


	ax1.set_xlabel('X')
	ax1.set_ylabel('Z')

	ax2.set_xlabel('X')
	ax2.set_ylabel('Y')

	plt.subplots_adjust(wspace = 0.3)
	plt.show()