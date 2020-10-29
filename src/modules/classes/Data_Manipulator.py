
import pandas as pd
import os
from .FEBio_xml_parser import FEBio_xml_parser
from .. sys_functions import next_path

D_NODESETS = [("NodeSet", "Endocardio", "node"), ("NodeSet",
                                                  "Epicardio", "node"), ("NodeSet", "Top_surface", "node")]


class Data_Manipulator:
    def __init__(self, path_to_feb_file, Febio_inp=None, geo_data_info=D_NODESETS):
        self.febio_inp = Febio_inp if Febio_inp != None else FEBio_xml_parser(
            path_to_feb_file)

        self.set_names = [v[1] for v in geo_data_info]
        self.set_order = {v[1]: i for i, v in enumerate(geo_data_info)}
        self.geo_data_info = geo_data_info
        self.geo_data = self.febio_inp.get_geometry_data(what=geo_data_info)

        self.nodes = self.geo_data[0]
        self.elems = self.geo_data[1] if len(self.geo_data) > 1 else []
        self.node_dict = self.get_nodes_from_elems()

        self.node_sets = self.geo_data[2] if len(self.geo_data) > 2 else []
        self.face_sets = self.get_faceSets()

        self.face_dicts = self.get_face_dict()

        self.initial_pos = self.get_initial_nodal_position()

        self.data = pd.DataFrame()
        self.data_keys = []

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
        nodeLists = [self.node_sets[v]
                     for v in self.set_names] if nodeLists == None else nodeLists
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

    def get_node_data_from_face(self, face, node_df=None):
        node_df = self.initial_pos if node_df == None else node_df
        return node_df.loc[node_df["node"].isin(face.keys())]

    def get_nodes_from_surface(self, surface_data):
        geo_data = self.febio_inp.get_geometry_data(
            what=surface_data, return_nodes=False, return_elems=False)
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

    def read_plot_file(self, files, data_formats, refs, out_file_name, run_ref="", param_val=0.0, dtypes={}, save_pickle=False):
        df_list = []
        for (file, data_format, _ref) in zip(files, data_formats, refs):
            data_keys = data_format.split(";")
            data_vec = list()
            with open(file, 'r') as _f:
                for line in _f:
                    line = line.strip()
                    if line[0:2] == "*T":
                        timestep = float(line.split("=")[1])
                    elif line[0] == "*":
                        continue
                    else:
                        data = line.split(" ")
                        new_data = dict([(data_keys[k-1], float(data[k]))
                                         for k in range(1, len(data))])
                        new_data[_ref] = int(data[0])
                        new_data["timestep"] = timestep
                        new_data["run_ref"] = run_ref
                        new_data["param_val"] = param_val
                        data_vec.append(new_data)

            df_temp = pd.DataFrame.from_records(data_vec)

            df_list.append(df_temp)
            
        df = pd.concat(df_list, sort=False).drop_duplicates(
        ).reset_index(drop=True)

        for column_key in dtypes:
            df.loc[:,column_key] = df[column_key].astype(dtypes[column_key])

        self.data = df
        self.data_keys = df.columns

        if save_pickle:
            file_path = os.path.dirname(os.path.abspath(file))
            temp_path = os.path.join(file_path, "tmp")
            if not os.path.isdir(temp_path):
                os.mkdir(temp_path)

            new_filepath_pattern = os.path.join(
                temp_path, '{outfile}-%s.pickle'.format(outfile=out_file_name))
            new_file_path = next_path(new_filepath_pattern)

            df.to_pickle(new_file_path)

    def concat_data(self, new_dfs=[]):
        df_list = [self.data]
        df_list.extend(new_dfs)
        df = pd.concat(df_list, sort=False).drop_duplicates(
        ).reset_index(drop=True)

        self.data = df
        self.data_keys = df.columns

        return self.data

    def set_data(self, data_df = None, pickle_path=None):
        if pickle_path != None:
            self.data = pd.read_pickle(pickle_path)
        elif data_df != None:
            self.data = data_df
        else:
            pass