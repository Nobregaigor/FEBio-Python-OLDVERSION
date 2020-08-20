# Example: Calculate Fibers

This command is used to calculate the fibers of a generic myocardium geometry. It uses a MATLAB script to compute the fiber orientation and saves the output on a fibers data file. It is important the the path to the matlabfolder containing the calculate_fibers function must be specified in the config file or during the execution of the command. We made this modular so that users can easily implement their own functions at their preffered directory for MATLAB.

This function requires the following inputs:

* FEB_NAME (O).
* GEOMETRY_DATA_FOLDER (O).
* OUTPUT_FOLDER (O).
* PATH_TO_MATLAB_FOLDER (O).
* MATLAB_PARAMS (O).

Calculate fibers is a special case function that does no take a .feb file directly. Instead, it must be provided the FEB_NAME that refers to the desired feb geometry in the GEOMETRY_DATA_FOLDER. This folder contains .csv files with the extracted geometry data of a generic feb model and are organized by filename containing: feb name, mesh type and data type. Mesh type must specify wheter the geometry contains a tetrahedral or hexagonal mesh with the prefix "tet" and "hex" respectively. Data type must specify wheter the file includes nodes or elements with the prefix "nodes" and "elems" respectively. In addition, if the geometry contains a hex mesh, a "hexbase" geometry (created using a tetrahedral format of the same geometry) file must be added in the geometry data folder.

Moreover, MATLAB_PARAMS should include necessary parameters to execute matlab function in a python dictionary syntax.

##### Providing values at command execution:

In the command line at the root directory of FEBio-Python, run:

```bash
./main run --CALCULATE_FIBERS --FEB_NAME "myo_hex_coarse" --GEOMETRY_DATA_FOLDER "path/to/geometry/dir" --PATH_TO_MATLAB_FOLDER "path/to/matlab/dir" --MATLAB_PARAMS "{'endo':45,'epi':75}" --OUTPUT_FOLDER "path/to/output/dir"
```

##### Providing value at config file:

At the config.json file add:
```json
"INPUT_DEFAULTS": {
  "CALCULATE_FIBERS": {
      "FEB_NAME": "all",
      "GEOMETRY_DATA_FOLDER": "geometry_data",
      "OUTPUT_FOLDER": "fibers_data",
      "PATH_TO_MATLAB_FOLDER": "matlab_functions",
      "MATLAB_PARAMS": "{'endo':45,'epi':75}"
  },
}
```
In the command line at the root directory of FEBio-Python, run:
```bash
./main run --CALCULATE_FIBERS
```







