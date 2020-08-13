## !! work in Progress !!

### Guidelines

---

##### Reference list
Commands|Description|Inputs
-------|----------|-----
ADD_PROPERTIES|Adds selected properties to a given FEB.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>PROPERTIES_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li><li>SELECTED_PROPERTIES (O).</li></ul>
ADD_FIBERS|Adds fibers data to a feb file.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>FIBERS_DATA_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li></ul>
CREATE_LOADCURVE|Creates a load curve using FEB format (written in a xml file).|<ul><li>CURVE_NAME (R).</li><li>CURVE_MODEL (R).</li><li>CURVE_PARAMS (R).</li><li>CURVE_FOLDER (O).</li><li>CURVE_TYPE (O).</li></ul>
ADD_LOAD|Add Loads and LoadData to a given feb file.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li><li>LOAD_NAME (O).</li><li>LOAD_FOLDER (O).</li><li>LOAD_ATTRS (O).</li></ul>
EXTRACT_GEOMETRY_DATA|Extract the geometry data (nodes and elements) from a given feb file.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul>
CALCULATE_FIBERS|Calculates fiber orientation of a myocardium geometry.|<ul><li>FEB_NAME (O).</li><li>GEOMETRY_DATA_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li><li>PATH_TO_MATLAB_FOLDER (O).</li><li>MATLAB_PARAMS (O).</li></ul>
PREPARE|Prepares and executes a mesh study. Can also be used to do a parametric study with fiber orientation.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul>
RUN_FEB|Runs an feb file or all files in sub-folder of an input folder.|<ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li></ul>
CREATE_STORAGE_FOLDER|Creates the main folders of a study storage.|<ul><li>STORAGE_NAME (R).</li><li>PATH_TO_STORAGE (O).</li></ul>
CALCULATE_RESULTS|ndy|<ul><li>INPUT_FOLDER (O).</li></ul>
MODIFY_PARAMETER|Modifies given parameters of a feb file.|<ul><li>PARAM_VALS (R).</li><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>SAVE_AS_NEW (O).</li></ul>
PREPARE_PARAMETER_STUDY|Prepares a parametric study.|<ul><li>CONFIG_FILE (R).</li><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul>
MAKE_PICKLE|Makes a pickle from a colection of result files.|<ul><li>INPUT_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li></ul>
### Descriptions of Commands and Inputs

---

##### List of Commands


##### List of Inputs


| Inputs | Description |
| - | - |
| INPUT_FILE | Input file (AR): Uses this file as the main FEB file. |
| FEB_FILE | Feb file (AR): Same as input file, but will replace it if both are given. |
| INPUT_FOLDER | Input folder (AR): Finds all feb inside the given directory. Will overwrite input file or feb file if given. |
| OUTPUT_FOLDER | Output folder (O): Where the output file should be written. Default uses same directory as input folder. |
| PROPERTIES_FOLDER | Properties folder (O): Directory containg properties to add to feb. Properties must be xml files. |
| SELECTED_PROPERTIES | Selected properties (O): A string containg selected properties to include. To select all use -all-. |
| EXCLUDE_PROPERTIES | Exclude properties (O): A string containg selected properties to exclude. |
| FIBERS_DATA_FOLDER | Fibers data folder (O): Directory containg the fibers csv data files. |
| CURVE_NAME | Loadcurve name (R): A string that determines the name as the loadcurve will be saved as. |
| CURVE_MODEL | Loadcurve model (R): A string specifying the mathematical model to create the curve. Options are:<POLYNOMIAL>. |
| CURVE_PARAMS | Loadcurve model (R): A string containing necesssary parameters to compute loadcurve. Must follow python syntax. |
| CURVE_TYPE | Loadcurve type (O): A string determining the type of curve to be used in FEB. Values can be:<smooth>, <step>, and others (see FEBio docs for more info). |
| CURVE_FOLDER | Loadcurve folder (O): Output directory of the created loadcurve. |
| LOAD_NAME | Loadcurve name (O): A string containing load names to be included in a FEB file. Names must be separated by < - >. To input all, use < all >. Filenames must contain the given LOAD_NAME. |
| LOAD_FOLDER | Loadcurve folder (O): Input directory which contains the loadcurve file. |
| LOAD_ATTRS | Load attributes (O): -- NOT USED, WILL BE REMOVED -- |
| FEB_NAME | Feb name (O): Filenames of feb files to be used as the input files. Names must be separated by < - >. To input all, use < all >. Filenames must contain the given FEB_NAME. |
| GEOMETRY_DATA_FOLDER | Geometry data folder (O): Directory containing .csv geometry data files of the given FEB file. Geometry filenames must contain FEB_NAME and a specification of its type<nodes> or <elems>. Geometry folder must contain both nodes and elements files of desired FEB_NAME. |
| PATH_TO_MATLAB_FOLDER | Path to MATLAB folder (O): Directory containg matlab functions to be used with FEBio-Python. Can be a full path, but config file must specify JOIN_MATLAB_FOLDER as False, otherwise will join FEBIO-DIRECTORY path with given folder. Matlab .m files must be named as the function to be used and be able to run directly on cmd. |
| MATLAB_PARAMS | Matlab parameters (O): A string containg necessary parameters to execute matlab function. Must follow python syntax. |
| STORAGE_NAME | Storage name (R): Storage directory name. |
| PATH_TO_STORAGE | Path to storage (R): Path to given storage name. |
| PARAM_VALS | Parameter values (R): A string containg a dictionary of params to be modified in a FEB file. For now, it can only modify Material parameters (will include option to modify any in the future). |
| SAVE_AS_NEW | Save as new (O): A string<True> or <False> specifying if modified FEB file should be saved as a new file or be re-written. |
| CONFIG_FILE | Config file (R): Path to a config file to be used within a funtion. |
