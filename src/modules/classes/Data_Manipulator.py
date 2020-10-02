
import pandas as pd
from .FEBio_xml_parser import FEBio_xml_parser

D_NODESETS = [("NodeSet", "Endocardio", "node"), ("NodeSet", "Epicardio", "node"), ("NodeSet", "Top_surface", "node")]

class Data_Manipulator:
  def __init__(self, path_to_feb_file, Febio_inp = None, geo_data_info = D_NODESETS):
    self.febio_inp = Febio_inp if Febio_inp != None else FEBio_xml_parser(path_to_feb_file)

    self.set_names = [v[1] for v in geo_data_info]
    self.set_order = {v[1]: i for i,v in enumerate(geo_data_info)}
    self.geo_data_info = geo_data_info
    self.geo_data = self.febio_inp.get_geometry_data(what=geo_data_info)

    self.nodes = self.geo_data[0]
    self.elems = self.geo_data[1] if len(self.geo_data) > 1 else []
    self.node_dict  = self.get_nodes_from_elems()

    self.node_sets = self.geo_data[2] if len(self.geo_data) > 2 else []   
    self.face_sets  = self.get_faceSets()

    self.face_dicts = self.get_face_dict()

    self.initial_pos = self.get_initial_nodal_position()

  def get_nodes_from_elems(self, elems=None):
    """Creates a dictionary with nodes as keys and a list of element numbers for each node."""
    elems = self.elems if elems == None else elems
    nodeDict = dict()
    for el in elems:
        el_num = int(el[0])
        el_nods = [int(v) for v in el[1:]]
        for node_num in el_nods:
            if node_num in nodeDict:
                nodeDict[node_num].append(el_num)
            else:
                nodeDict[node_num] = [el_num]
    return nodeDict

  def get_faceSets(self, nodeLists=None):
    """Returns a list of sets containing node numbers of a given face"""
    nodeLists = [self.node_sets[v] for v in self.set_names] if nodeLists == None else nodeLists
    to_return = list()
    for _list in nodeLists:
        to_return.append(set([int(v[0]) for v in _list]))
    return to_return

  def get_face_dict(self, nodeDict=None, faceSets=None):
    """Returns list with dicts containing the intersections between a nodeDict and a faceSet"""
    nodeDict = self.node_dict if nodeDict == None else nodeDict
    faceSets = self.face_sets if faceSets == None else faceSets

    to_return = list()
    for _faceSet in faceSets:
        faceDict = dict()
        for node_num in _faceSet:
            faceDict[node_num] = nodeDict[node_num]
        to_return.append(faceDict)
    return to_return

  def get_initial_nodal_position(self):
    df = pd.DataFrame(self.nodes, columns=["node", "x", "y", "z"])
    df["node"] = df["node"].astype('int')
    return df

  def get_node_data_from_face(self, face, node_df = None):
    node_df = self.initial_pos if node_df == None else node_df
    return node_df.loc[node_df["node"].isin(face.keys())]

  def get_nodes_from_surface(self, surface_data):
    geo_data = self.febio_inp.get_geometry_data(what=surface_data, return_nodes=False, return_elems=False)
    data = [geo_data[0][surf[1]] for surf in surface_data]
    to_return = []
    for _surf in data:
      surf_dict = dict()
      for el in _surf:
        el_num = int(el[0])
        el_nods = [int(v) for v in el[1:]]
        surf_dict[el_num] = el_nods
      to_return.append(surf_dict)


    # nodes = [self.get_nodes_from_elems(v) for v in data]
    return to_return

