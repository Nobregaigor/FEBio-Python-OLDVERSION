# FEBIO-Python

#### Welcome!

FEBio-Python is an open source repo for optmizing FEA studies using FEBio solver. The library makes it possible to easily set up parametric studies, modify .feb files using command line. One can also use it to run several feb files and extract geometric and result files from each simulation.

#### FEBio

The FEBio software suite is a set of software tools for nonlinear finite element analysis in biomechanics and biophysics. To learn more, visit their website https://febio.org/ or their repo: https://github.com/febiosoftware/FEBio.git.

#### Contribute!

All ideas are welcome. Open/close issues, fork the repo, implement your own functions and share your code with a Pull Request. You can clone this project to your machine with:

```bash
git clone https://github.com/Nobregaigor/FEBio-Python.git
```

# Installation

### To install FEBio-Python using pip:
 (future implementation)

### Download or clone from this repository:
```bash
git clone https://github.com/Nobregaigor/FEBio-Python.git
```
### Dependencies

FEBio-Python depends on the following packages:
```
six == 1.15.0
pyfiglet == 0.8.post1
pandas == 1.0.5
colorama == 0.4.3
scipy == 1.4.1
prettierfier == 1.0.3
termcolor == 1.1.0
matplotlib == 3.3.0
numpy == 1.19.1
click == 7.1.2
beautifulsoup4 == 4.9.1
PyInquirer == 1.0.3
```
To install dependencies with pip, run:
```bash
pip install six pyfiglet pandas colorama scipy prettierfier termcolor matplotlib numpy click beautifulsoup4 PyInquirer
```

# Usage
### How to run:
In the project's folder directory, run:
```
 $ .\main.py run [COMMAND] [COMMAND-OPTIONS]
```
### Example:
```
 $ .\main.py run add-properties --INPUT_FOLDER 'path/to/input/folder'
```
### The help command:
You can ask for help at any command in the CLI:
```
 $ .\main.py --help
```
Or, to show a list of possible commands:
```
 $ .\main.py run --help
```
Or, to show a list of inputs accepted by the command:
```
 $ .\main.py run add-properties --help
```
### Command input requirement types:
Each command requires a certain list of inputs, however, if you are using a config file, you do not need to keep providing all the inputs at all times. Each input is categorized into one of the following type:
* Required **(R)**: Must be included in the command line every time the command is executed. There is no reference to it in the config file.
* Required, but has alternative options **(RA)**: The input is require, but there are different choices that satisfy its category. For instance, in some functions you can use FEB_FILE or INPUT_FILE with the same meaning. 
* Optional **(O)**: Inputs categorized as optional can have a reference to it in the config file. When the function is executed, if the given input is not listed withn its command, the program will look for it in the config file. If the program does not find its reference, it might cause issues at run time.
To check which input and what type of input the command requires, check the Reference list.

### The config file:
The config file must be present at the root of the project's directory. Within the config file, you are able to establish directories and input values to be used along with FEBio-Python. You can list pre-defined arguments for each command with an optional input (see previous section). 

Also, for inputs that requires PATH attributes, you can opt to use a 'working/storage' directory or provide the absolute path to its file/directory. However, if you choose to manually include the path, you must provide the absolute path for all inputs, otherwise the program will join the project's core directory with the given path.

### To learn more:
Check the project's guidelines for a list of commands and their possible inputs. To learn more about each command or input individually, check the descriptions section.



# Guidelines

---

### Reference list


| Commands | Description | Inputs |
| - | - | - |
| ADD_PROPERTIES | Adds selected properties to a given FEB. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>PROPERTIES_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li><li>SELECTED_PROPERTIES (O).</li></ul> |
| ADD_FIBERS | Adds fibers data to a feb file. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>FIBERS_DATA_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li></ul> |
| CREATE_LOADCURVE | Creates a load curve using FEB format (written in a xml file). | <ul><li>CURVE_NAME (R).</li><li>CURVE_MODEL (R).</li><li>CURVE_PARAMS (R).</li><li>CURVE_FOLDER (O).</li><li>CURVE_TYPE (O).</li></ul> |
| ADD_LOAD | Add Loads and LoadData to a given feb file. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li><li>LOAD_NAME (O).</li><li>LOAD_FOLDER (O).</li><li>LOAD_ATTRS (O).</li></ul> |
| EXTRACT_GEOMETRY_DATA | Extract the geometry data (nodes and elements) from a given feb file. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul> |
| CALCULATE_FIBERS | Calculates fiber orientation of a myocardium geometry. | <ul><li>FEB_NAME (O).</li><li>GEOMETRY_DATA_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li><li>PATH_TO_MATLAB_FOLDER (O).</li><li>MATLAB_PARAMS (O).</li></ul> |
| PREPARE | Prepares and executes a mesh study. Can also be used to do a parametric study with fiber orientation. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul> |
| RUN_FEB | Runs an feb file or all files in sub-folder of an input folder. | <ul><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li></ul> |
| CREATE_STORAGE_FOLDER | Creates the main folders of a study storage. | <ul><li>STORAGE_NAME (R).</li><li>PATH_TO_STORAGE (O).</li></ul> |
| CALCULATE_RESULTS | ndy | <ul><li>INPUT_FOLDER (O).</li></ul> |
| MODIFY_PARAMETER | Modifies given parameters of a feb file. | <ul><li>PARAM_VALS (R).</li><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>SAVE_AS_NEW (O).</li></ul> |
| PREPARE_PARAMETER_STUDY | Prepares a parametric study. | <ul><li>CONFIG_FILE (R).</li><li>FEB_FILE (RA).</li><li>INPUT_FILE (RA).</li><li>INPUT_FOLDER (RA).</li><li>OUTPUT_FOLDER (O).</li></ul> |
| MAKE_PICKLE | Makes a pickle from a colection of result files. | <ul><li>INPUT_FOLDER (O).</li><li>OUTPUT_FOLDER (O).</li></ul> |

# Descriptions of Commands and Inputs

---

### List of Commands


| Commands | Description |
| - | - |
| ADD_PROPERTIES | This command can be used to add selected properties to one or more feb files. Properties must be a valid direct child of the febio_spec root and be named with its outermost element. Properties must be written in xml format. |
| ADD_FIBERS | This command can be used to add MeshData element to a feb file containing fibers data. Fibers are organized by element type and can be computed using CALCULATE_FIBERS command. Fibers data .csv file must contain the name of the FEB file which it refers to and first row must have node number information. |
| CREATE_LOADCURVE | This command can be used to create a loadcurve with specified parameters. |
| ADD_LOAD | This command can be used to add one or more<loadcurve> to a <LoadData> or one or more <load> to a <Loads> in a FEB file. Moreover, loadfiles must contain the name of the load or loadcurve to be included. Loadcurves must also contain <loadcurve> in its name. |
| EXTRACT_GEOMETRY_DATA | This command is used to extract the geometry data (nodes and elements) from a given feb file. It saves nodes and elements in seperate files in a .csv format where the first colum is the node or element id and the following columns are the geometry data. |
|   |   |
| CALCULATE_FIBERS | This command is used to calculate the fibers of a generic myocardium geometry. It uses MATLAB to compute the fiber orientation and saves the output on a fibers data file. |
| PREPARE | This command can be used to prepare and execute a mesh or parametric study. It will use one or more raw FEB files, include all properties in a given<property> folder, inlude all loads in a <load> property, extract geometry data, compute fibers data and add them to the given feb files. Next, it will run all feb files in the saved directory. For now, it does not allow for skipping steps, but will add such functionality in the future. |
| RUN_FEB | This command is used to run all FEB files in sub-folders of a given directory. Will add functionality to run all feb files in a single directory. |
| CREATE_STORAGE_FOLDER | This command can be used to set up a storage folder with the main folders of a study storage. |
| CALCULATE_RESULTS | ndy |
| MODIFY_PARAMETER | This command can be used to modify parameters of one or more feb file. |
| PREPARE_PARAMETER_STUDY | Prepares a parametric study. |
| MAKE_PICKLE | Makes a pickle from a colection of result files. |

### List of Inputs


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
