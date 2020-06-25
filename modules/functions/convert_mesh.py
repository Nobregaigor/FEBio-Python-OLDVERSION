import pyansys

path_to_folder = "C:\\Users\\igorp\\University of South Florida\\Mao, Wenbin - Myocardium (organized)\\Geometries\\Ansys\\cdb\\"
input_file = path_to_folder + "file.cdb"
output_file = path_to_folder + "saved_from_pyansys.vtu"

# ------------------------------------------
# Read cdb file 
archive = pyansys.Archive(input_file)
print("------- archive -------")
print(archive)
print("--> Nodes:")
print(archive.nodes)
print("\n")
print("--> Elements:")
print(archive.elem)
print("\n")

# ------------------------------------------
# Create grid for plot
grid = archive.grid
# grid.plot(color='w', show_edges=True)

grid.save(output_file)


