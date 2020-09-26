import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import xml.etree.ElementTree as ET
from os.path import isfile, join
from os import getcwd

from scipy.spatial import distance


##############################
# MACROS
#################################

# # Geometry data
# A = -65
# B = 25
# YMAX = 20
# THICKNESS = -10 # negative to match equation

# # Mesh data
# VERTICAL_RES = 60
# N_LAYERS = 4 # from endo to epi, not including endo
# CIRCUNFERENTIAL_RES = 30



# Geo
A = -65
B = 25
H = 0
K = 0
YMAX = 20


_TYPE = 1

N_INTERNAL_LAYERS = 8  	# Horizontal res	--> will add two layers (internal and external)
N_NODES_PER_LAYER = 32	# Vertical res	--> will add one or 2 nodes to fix top/bottom constrains
N_REVS = 36						# Circf. res --> need to be multiple of 3 and 2

##############################
# 2D Functions
#################################

class vector2d:
	def __init__(self, p1, p2, has_normal=True):
		self.p1 = p1
		self.p2 = p2
		self.vec = self.vector2d()
		self.unit = self.unit_vector()
		self.to_plot = [[p1[0], p2[0]], [p1[1],p2[1]]]
		self.normal = vector2d([-self.vec[1], self.vec[0]], [self.vec[1], -self.vec[0]], has_normal=False) if has_normal else None
	
	def __call__(self):
		return self.vec
	
	def __str__(self):
		return "Vector2d: p1: {p1:} p2: {p2:}".format(p1=self.p1, p2=self.p2)

	def vector2d(self):
		return np.array([self.p2[a] - self.p1[a] for a in range(len(self.p1))])
	
	def unit_vector(self):
		return self.vec / np.linalg.norm(self.vec)

	def rotate(self,theta):
		rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
		p2 = np.matmul(rotation_matrix, self.vec)
		p2 += np.array(self.p1)

		return vector2d(self.p1, p2)

class dataPoint:
	def __init__(self, coord, l=-1, s=-1, rh=-1, n=-1):
		self.coord = coord
		self.layer = l
		self.section = s
		self.refH = rh
		self.nodeNumber = n
	
	def copy(self):
		return dataPoint(self.coord, self.layer, self.section, self.refH, self.nodeNumber)

def vector2dFromP1(center, length, dir):
	p1 = np.array(center)
	p2 = np.array([length * dir[0], length * dir[1]]) + p1
	return vector2d(p1,p2)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2' """
    return np.arccos(np.clip(np.dot(v1.unit, v2.unit), -1.0, 1.0))

def regress(xs,ys,deg):
	coeffs = np.polyfit(xs,ys,deg)

	# if _print == True:
	# 	a = ['(x^'+str(len(coeffs)-(i+1))+") * "+str(y) if i+1 !=len(coeffs) else str(y) for i, y in enumerate(coeffs)]
	# 	print("Coeffs: " + str(coeffs) + " | " + " + ".join(a)[:-1:])

	# return lambda x: np.sum([(x**len(coeffs)-(i+1))*y if i+1 !=len(coeffs) else y for i, y in enumerate(coeffs)])
	return np.poly1d(coeffs)

# Ellipse Functions

def ellipse(a, b, h=0, k=0, _type=0, ref=-1):
	def eq(val):
		if _type == 0: # solved for y (return y, given x)
			return (a/b) * -ref * np.sqrt(b**2 - (val-h)**2) + k
			# return np.sqrt((1 - (val - h)**2 ) /b**2) + k
		elif _type ==  1: # solved for x (return x, given y)
			return (b/a) * ref * np.sqrt(a**2 - (val-k)**2) + h
	
	return eq

def ellipse_focci(a,b,h=0,k=0):
	c = np.sqrt(a**2 - b**2)
	return np.array([h, k + c]), np.array([h, k - c])

def sctattered_ellipse(a,b,h,k, yrange, xrange, x_res, y_res):
	# Define eq of elipse
	y_ellpisis = ellipse(a,b,h,k,1)
	x_ellpisis = ellipse(a,b,h,k,0)

	# Get min and max values
	ymin = np.min(yrange)
	ymax = np.max(yrange)
	xmin = np.min(xrange)
	xmax = np.max(xrange)

	# Calculate undistributed points
	ys_ybased = np.linspace(ymin, ymax, x_res)
	xs_ybased = np.array([y_ellpisis(y) for y in ys_ybased ])
	xs_xbased = np.linspace(xmin, xmax, y_res)
	ys_xbased = np.array([x_ellpisis(x) for x in xs_xbased ])

	# Set points in a single array
	xs = np.append(xs_ybased, xs_xbased)
	ys = np.append(ys_ybased, ys_xbased)

	# Sort points
	s1 = np.zeros((len(xs), 2))
	for i, x in enumerate(xs):
		s1[i][0] = x
		s1[i][1] = ys[i]
	s1 = s1[np.argsort(s1[:, 1])]

	s2 = np.zeros((2,len(s1)))
	for i in range(len(s1)):
		s2[0][i] = s1[i][0]
		s2[1][i] = s1[i][1]

	return s1, s2

def regressed_ellipse(a,b,h,k, yrange, xrange, yswitch=0.80, breakpoints=[0], res=100, deg=2, axis=1):

	# Define min and max values
	ymin = np.min(yrange)
	ymax = np.max(yrange)
	xmin = np.min(xrange)
	xmax = np.max(xrange)

	# Calculate scattered ellipse
	s_original, _ = sctattered_ellipse(a,b,h,k, yrange, xrange, res, res)

	# Set yswtich based on the basal value of a
	yswitch = a * yswitch
	# print("yswith:",yswitch)

	# Remove breakpoints before yswitch
	# breakpoints = np.delete(breakpoints, [i for i, p in enumerate(breakpoints) if p <= yswitch])

	# Insert min and max breakpoints if they are not already included (do not duplicate)
	# breakpoints = np.insert(breakpoints, 0, yswitch) if yswitch > ymin else breakpoints
	breakpoints = np.insert(breakpoints, 0, ymin) if ymin not in breakpoints else breakpoints
	breakpoints = np.append(breakpoints, ymax) if ymax not in breakpoints else breakpoints

	# print("Breakpoints:", breakpoints)
	# Break s_original based on breakpoints
	polys = []
	r_range = range(len(breakpoints) - 1)
	count = 1
	for i in r_range:
		brkpoint1 = breakpoints[i]
		brkpoint2 = breakpoints[i+1]

		s = [[],[]]
		for j in range(count-1,len(s_original)):
			yval = s_original[j][1]
			# print(yval)
			if breakpoints[i] <= yval <= breakpoints[i+1]:
				s[0].append(s_original[j][0])
				s[1].append(s_original[j][1])

				# s.append([s_original[j][0], s_original[j][1]])
				count += 1
			else:
				break
		# print("---")
		# print("brk1:", breakpoints[i])
		# print("brk2:", breakpoints[i+1])
		# print("s[0]:")
		# print(s[0])
		# print("s[1]:")
		# print(s[1])
		# print("---")

		polys.append(regress(s[1], s[0], deg))


	def reg_ell(val):
		if val == ymin:
			return 0
		else:
			for i in r_range:
				if breakpoints[i] <= val <= breakpoints[i+1]:
					index = i
					break
			return polys[index](val)

	return reg_ell

def distributed_ellipse(a,b,h,k, yrange, xrange, x_res=500, y_res=500, dist_res=50, err=0.05):

	# Calculate original ellipse
	ell_original_coords, ell_original = sctattered_ellipse(a,b,h,k, yrange, xrange, x_res, y_res)
	# Calculate total length of the curve
	dist_matrix = distance.cdist(ell_original_coords, ell_original_coords, 'euclidean')
	# Get dist resolution
	dist = dist_matrix[0][-1] / (dist_res - 1)
	# Set min and max dist according to allowed error
	min_dist = dist*(1-err)
	max_dist = dist*(1+err)

	diff_sum = 0
	# Bound first coord
	ell_distr_coords = [ell_original_coords[0]]
	ell_distr = [[ell_original[0][0]],[ell_original[1][0]]]

	for i in range(len(dist_matrix) - 1):
		prev_dist = dist_matrix[i][0]
		next_dist = dist_matrix[i+1][0]
		diff_dist = next_dist - prev_dist
		diff_sum += diff_dist
		if min_dist <= diff_sum <= max_dist:
			ell_distr_coords.append(ell_original_coords[i])
			ell_distr[0].append(ell_original[0][i])
			ell_distr[1].append(ell_original[1][i])
			diff_sum = 0

	ell_distr_coords.append(ell_original_coords[-1])
	ell_distr[0].append(ell_original[0][-1])
	ell_distr[1].append(ell_original[1][-1])

	return np.array(ell_distr_coords), np.array(ell_distr)

# Geometry build functions

def refractions(ell_coords, focci, n1, n2, bias_factor=0, plot_ax=None, flat_top=True):
	# NOTE: Refreaction only inside object (not on edges)

	def snellsLaw(n1,n2,theta1):
		""" Returns theta2 based on snell's refraction law"""
		theta2 = np.arcsin((n1/n2) * np.sin(theta1))
		# if theta2 <= np.pi * 0.5:
		# 	print("true")
		# 	theta2 = -theta2
		return theta2

	refracs = []

	for i in range(-1, len(ell_coords) - 1):

		# Calculate "refraction" rays for borders along y axis
		if i < 0 and ell_coords[i+1][0] == 0:
			incomming_ray = vector2d(focci, ell_coords[i+1])
			ref_vector = vector2d(ell_coords[i+1],ell_coords[i+2]) # Not really used (just for plot consistence)
			n_vec1 = vector2dFromP1(ref_vector.p1, 5, incomming_ray.normal.unit_vector())
			n_vec2 = vector2dFromP1(ref_vector.p1, 5, -incomming_ray.normal.unit_vector())
			
			refracted_ray = vector2dFromP1(ref_vector.p1, 5, incomming_ray.unit_vector())

		elif flat_top == True and i >= len(ell_coords) - 4:
			incomming_ray = vector2d(focci, ell_coords[i+1])
			ref_vector = vector2d(ell_coords[i+1], [ell_coords[i+1][0] + 5, ell_coords[i+1][1]]) # Not really used (just for plot consistence)

			n_vec1 = vector2dFromP1(ref_vector.p1, 5, -ref_vector.unit_vector())
			n_vec2 = vector2dFromP1(ref_vector.p1, 5, ref_vector.unit_vector())
			
			refracted_ray = vector2dFromP1(ref_vector.p1, 5, ref_vector.unit_vector())

		else:
			# Get incomming ray and ref vectors
			incomming_ray = vector2d(focci, ell_coords[i+1])
			ref_vector = vector2d(ell_coords[i],ell_coords[i+1])

			# Get normal vectors (2 of them for plotting)
			n_vec1 = vector2dFromP1(ref_vector.p2, 5, -ref_vector.normal.unit_vector())
			n_vec2 = vector2dFromP1(ref_vector.p2, 5, ref_vector.normal.unit_vector())

			# Refraction angle will be used for yvals below than zero
			if n_vec2.p1[1] < 0:

				# Calculate refraction angle
				theta1 = angle_between(incomming_ray, n_vec1)
				theta2 = snellsLaw(n1,n2,theta1)

				# Apply bias factor
				bias_factor = bias_factor * 1/np.log(abs(n_vec2.p1[1]) + 100)
				theta2 = theta2 * (1 - bias_factor)

				# Rotate vec_2 based on theta 2
				refracted_ray = n_vec2.rotate(-theta2) if n_vec2.p1[1] < 0 else  n_vec2.rotate(theta2)
			
			else:
				refracted_ray = n_vec2
				# n_vec2 = n_vec1
			
		refracs.append((refracted_ray, n_vec2))

		# Storing info for plot
		if plot_ax != None:
			xs = []
			ys = []
			xs.extend(incomming_ray.to_plot[0])
			xs.extend(ref_vector.to_plot[0])
			xs.extend(refracted_ray.to_plot[0])

			ys.extend(incomming_ray.to_plot[1])
			ys.extend(ref_vector.to_plot[1])
			ys.extend(refracted_ray.to_plot[1])

			xs1 = []
			ys1 = []
			# xs1.extend(n_vec1.to_plot[0])
			xs1.extend(n_vec2.to_plot[0])
			# ys1.extend(n_vec1.to_plot[1])
			ys1.extend(n_vec2.to_plot[1])

			xs2 = []
			ys2 = []
			xs2.extend(refracted_ray.to_plot[0])
			ys2.extend(refracted_ray.to_plot[1])

			plot_ax.plot(xs,ys)
			plot_ax.plot(xs1,ys1, linestyle="--", c="k")

	# # Calculate "refraction" rays for borders along y axis
	# for i in range(0,len(ell_coords), len(ell_coords) -1):
	# 	if ell_coords[i][0] == 0:
	# 		incomming_ray = vector2d(focci, ell_coords[i])
	# 		n_vec2 = vector2dFromP1(ref_vector.p2, 5, ref_vector.normal.unit_vector())


	return refracs, [(xs,ys), (xs2,ys1)] #plot data

def ref_nodes(refracts, thickness, n_layers, focci=np.array([0,0]), flat_top=True):

	layers_space = np.linspace(0,thickness,n_layers + 2)
	print(layers_space)

	points_matrix_coords = []
	points_matrix = [[],[]]
	ref_vectors = np.copy(refracts)

	dL = layers_space[1] - layers_space[0]
	print("dL:",dL)
	for L in layers_space:
		for i, vecs in enumerate(ref_vectors):
			refracted_vec = vecs[0]
			normal_vec = vecs[1]
			theta = angle_between(normal_vec,refracted_vec)
			if theta == np.pi*0.5:
				theta = 0

		
			if L > 0:
				# vec = vector2dFromP1(refracted_vec.p1, L, refracted_vec.unit)
				# vec = vector2dFromP1(refracted_vec.p1, L, normal_vec.unit)

				cosTheta = np.cos(theta)
				cdL = L * np.reciprocal(cosTheta) if cosTheta > 0 else 0
		
				print("L:", round(L,3), "| theta:", round(np.degrees(theta),3), "| cdL", round(cdL,5), "| 	L+cdL:", round(L + cdL,5))

				
				vec = vector2dFromP1(refracted_vec.p1, L, normal_vec.unit)
				# print(vec)
				# # print(vec)
				# vec = vec.rotate(theta)

				# print("vec*unit:",vec.vec * refracted_vec.unit)
				# vec = vector2d(normal_vec.p1, vec.vec * refracted_vec.unit + vec.p1)

				points_matrix_coords.append(vec.p2)
				points_matrix[0].append(vec.p2[0])
				points_matrix[1].append(vec.p2[1])
			else:
				vec = refracted_vec
				points_matrix_coords.append(vec.p1)
				points_matrix[0].append(vec.p1[0])
				points_matrix[1].append(vec.p1[1])

			# print(vec)

	return np.array(points_matrix_coords), np.array(points_matrix)

def ref_nodes2(refracts, thickness, n_layers, focci=np.array([0,0]), layer_res=N_NODES_PER_LAYER+2, flat_top=True):
	
	def is_parallel(p1, vec, err=np.radians(1)):
		if p1[0] != vec.p1[0] and p1[1] != vec.p1[1]:
			v1 = vector2d(p1,vec.p1) 
			theta = angle_between(vec, v1)
			# print(np.degrees(theta))
			if theta <= err or (np.pi - err <= theta <= np.pi + err) or theta >= np.pi*2 - err:
				return True
			else:
				return False
		else:
			return True

	layers_space = np.linspace(0,thickness,n_layers + 2)

	points_matrix_coords = []
	points_matrix = [[],[]]
	ref_vectors = np.copy(refracts)

	for Lindex, L in enumerate(layers_space):
		if Lindex == 0:
			for refH, vecs in enumerate(ref_vectors):
				ref_coord = vecs[0].p1
				dp = dataPoint(ref_coord)
				dp.layer = Lindex
				dp.refH = refH

				points_matrix_coords.append(dp)
				points_matrix[0].append(ref_coord[0])
				points_matrix[1].append(ref_coord[1])
			print("node_per_layer:", len(points_matrix_coords))
		else:			
			layer_coords, layer_xy = sctattered_ellipse(A-L,B+L,H,K, [A-L,YMAX], [0,B+L], 600, 600)

			node_per_layer_counter = 0
			angle_err = np.radians(0.5)
			# while node_per_layer_counter != layer_res:
			# 	node_per_layer_counter = 0
			tracker = 0
			for vecs in ref_vectors:
				found_match = False
				angle_err = np.radians(0.5)
				while not found_match:
					local_tracker = tracker
					
					for i in range(tracker,len(layer_coords)):
						# print("tracker", tracker, "local_tracker", local_tracker)
						if is_parallel(layer_coords[i],vecs[0], err=angle_err):
							dp = dataPoint(layer_coords[i])
							dp.layer = Lindex
							dp.refH = node_per_layer_counter

							points_matrix_coords.append(dp)
							points_matrix[0].append(layer_xy[0][i])
							points_matrix[1].append(layer_xy[1][i])
							node_per_layer_counter += 1
							found_match = True
							break
						else:
							local_tracker += 1
					angle_err += np.radians(0.5) # increase a tolerable degree
				tracker = local_tracker

			print("node_per_layer:",node_per_layer_counter)

	return np.array(points_matrix_coords), np.array(points_matrix)

def make_3d(points_matrix_coords, points_matrix, shift_yz=True):

	points_matrix_coords_3d = []
	for a in points_matrix_coords:
		if shift_yz == True:
			a.coord = np.insert(a.coord,1,0.)
		else:
			a.coord = np.append(a.coord,0)
			
		points_matrix_coords_3d.append(a)

	
	if len(points_matrix) > 0:
		z = np.zeros(len(points_matrix[0]))
		if shift_yz == True:
			a = points_matrix[0]
			b = points_matrix[1]
			points_matrix = np.vstack((a,z))
			points_matrix = np.vstack((points_matrix,b))
			# points_matrix = np.insert(points_matrix, 1, z)
		else:
			points_matrix = np.vstack(points_matrix, z)

		return np.array(points_matrix_coords_3d), points_matrix

def revolute(points_matrix_coords, rev=360, res=4, exclude_axis=True, axis='z'):
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
	
	point_cloud_by_coord = {}

	theta_space = np.linspace(0, rev, res + 1)
	node_count = 0
	section_count = 0
	for dtheta in theta_space[:-1]:
		
		for dp in points_matrix_coords:
			coord = np.matmul(dp.coord, rotation_matrix(np.radians(dtheta)))
			
			# Conditioning rotation on axis
			if coord[0] == 0:
				section = 0
			else:
				section = section_count

			newdp = dp.copy()
			newdp.coord = coord # update coord
			newdp.section = section
			newdp.nodeNumber = node_count

			point_cloud_by_coord[tuple(coord)] = newdp
			node_count += 1

		section_count += 1

	# print("number of nodes:", node_count - 1)
		

	# print("n_sections ", section_count - 1 )

	# Setting a dict of point cloud by node number
	point_cloud = {}
	for key in point_cloud_by_coord:
		dp = point_cloud_by_coord[key]
		point_cloud[dp.nodeNumber] = dp

	# Setting a matrix of x,y,z (explicit coordinates matrix)
	point_matrix = np.zeros((3, len(point_cloud)))
	for i, point in enumerate(point_cloud):
		point_matrix[0][i] = point_cloud[point].coord[0]
		point_matrix[1][i] = point_cloud[point].coord[1]
		point_matrix[2][i] = point_cloud[point].coord[2]

	return point_cloud, point_cloud_by_coord, point_matrix

def hex8(point_cloud, nodes, n_layers=N_INTERNAL_LAYERS+2):
	def get_elem(S,L,R,shape, maxS, on_center=False):
		if on_center==False:
			if S != maxS:
				S2 = S + 1 
			else:
				S2 = 0

			return(np.array([
				shape[(S , L  ,R )].nodeNumber,	#P1
				shape[(S2, L , R )].nodeNumber,	#P2
				shape[(S2,L+1, R )].nodeNumber,	#P3
				shape[(S ,L+1, R )].nodeNumber,	#P4
				shape[(S , L ,R+1)].nodeNumber,	#P5
				shape[(S2, L ,R+1)].nodeNumber,	#P6
				shape[(S2,L+1,R+1)].nodeNumber,	#P7
				shape[(S ,L+1,R+1)].nodeNumber	#P8
			]))
		else:
			Sp2 = S + 2
			if Sp2 == maxS+1:
				Sp2 = 0

			return(np.array([
				shape[(0,  L , 0)].nodeNumber,	#P1
				shape[( S,  L, 1 )].nodeNumber,	#P2
				shape[(S+1, L, 1 )].nodeNumber,	#P3
				shape[(Sp2, L, 1 )].nodeNumber,	#P4
				
				shape[(0 ,  L+1, 0)].nodeNumber,	#P5
				shape[( S,  L+1, 1)].nodeNumber,	#P6
				shape[(S+1, L+1, 1)].nodeNumber,	#P7
				shape[(Sp2, L+1, 1)].nodeNumber		#P8
			]))




	# print(point_cloud)
	shape = dict()
	maxS = 0
	maxL = 0
	maxR = 0

	for i, key in enumerate(point_cloud):
		dp = point_cloud[key]
		dp.nodeNumber = i
		shapeKey = (dp.section, dp.layer, dp.refH)
		shape[shapeKey] = dp
		maxS = maxS if dp.section < maxS else dp.section
		maxL = maxL if dp.layer < maxL else dp.layer
		maxR = maxR if dp.refH < maxR else dp.refH


	print("lenpointcloud", len(point_cloud), "lenshape", len(shape))
	print("maxS",maxS, "maxL", maxL, "maxR", maxR)

	elems = dict()
	elem_count = 0
	for s in range(maxS + 1):
		for l in range(maxL):
			for r in range(1, maxR - 1):
				elems[elem_count] = get_elem(s,l,r,shape,maxS)
				# print("elems[i]",elems[elem_count])
				elem_count += 1

	sSpace = np.linspace(0, maxS, (maxS+1)/3)
	print(sSpace)
	maxSBottom = int((maxS+1) / 3)
	maxSBottom = maxSBottom if maxSBottom%2 == 0 else maxSBottom-1
	maxSBottom = 2 * maxSBottom
	print("maxSBottom:",maxSBottom, maxS)

	for s in range( maxSBottom - 3):
		ss = s *2 if s != 0 else 0
		print(s, ss)
		if ss < maxS:
			for l in range(0,maxL):
				elems[elem_count] = get_elem(ss,l,1,shape,maxS, on_center=True)
				elem_count += 1
	# for i in range(maxS + 1 %)


	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# cs = ['b', 'r', 'g', 'c', 'k']
	# for key in shape:
	# 	if key[0] != 0:
	# 		break
	# 	coord = shape[key].coord
	# 	ax.scatter(coord[0],coord[2], c=cs[key[1]])

	return elems

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
	for key in nodes:
		node = nodes[key]
		# Create sub-elements
		_node = ET.SubElement(nodes_tag, "node")
		_node.set("id",str(node.nodeNumber))
		_node.text = ",".join([str(x) for x in node.coord])

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


######################################

if __name__ == "__main__":

	print("==== Test case ===")

	fig = plt.figure()
	axs = fig.add_subplot(121)
	axs2 = fig.add_subplot(122)

	fig2 = plt.figure()
	axs3 = fig2.add_subplot(111, projection='3d')

	## Focci points
	focci_pos, focci_neg = ellipse_focci(A,B,H,K)
	# plt.scatter(focci_pos[0],  focci_pos[1],c='y')
	
	## Scattered ellipse
	ell_original_coords, ell_original = sctattered_ellipse(A,B,H,K, [A,YMAX], [0,B], 1000, 1000)
	axs.scatter(ell_original[0],  ell_original[1],c='b')

	ell_distr_coords, ell_distr = distributed_ellipse(A,B,H,K, [A,YMAX], [0,B], dist_res=N_NODES_PER_LAYER)
	axs.scatter(ell_distr[0], ell_distr[1],c='g')

	refractions, _ = refractions(ell_distr_coords, [0,0], n1=1, n2=0.85,  bias_factor=-1.5, plot_ax=axs)

	
	# ell_2_coords, ell_2 = sctattered_ellipse(A-10,B+10,H,K, [A-10,YMAX], [0,B+10], 100, 100)
	# axs2.scatter(ell_2[0],  ell_2[1],c='g')

	ref_nodes_coords, ref_nodes = ref_nodes2(refractions, 10, N_INTERNAL_LAYERS)
	print("total n nodes:", len(ref_nodes_coords))
	axs2.scatter(ref_nodes[0], ref_nodes[1])

	

	ref_nodes_coords, ref_nodes = make_3d(ref_nodes_coords, ref_nodes)

	node_cloud, _, nodes = revolute(ref_nodes_coords, res=N_REVS, axis='z')
	axs3.scatter3D(nodes[0],nodes[1],nodes[2])

	elems = hex8(node_cloud, nodes)

	print("Writing File...")
	write_geometry(node_cloud,elems,"geometry.feb", getcwd())


	# xnodes = np.ma.array([0,1,2,3], mask=False)
	# ynodes = np.ma.array([0,1,2,3], mask=False)

	# def mask(arrays, idx):
	# 	for arr in arrays:
	# 		arr.mask[idx] = True

	# mask([xnodes, ynodes], 1)
	# print(xnodes)



	axs.grid()
	axs.axis('equal')

	axs2.grid()
	axs2.y_res = 2
	axs2.axis('equal')
	# axs2.x_res = 5

	plt.show()





