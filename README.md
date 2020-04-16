

## Sample commands:

#### ADD_PROPERTIES

The function ADD_PROPERTIES can be used to insert properties saved in xml formats in a given folder.

The inputs are:
1. FEB_FILE
- Flag: R1
- Value: Absolute or local path to feb file
- Executes: Adds attributes to given feb file
2. INPUT_FOLDER
- Flag: O1
- Value: Absolute or local path to folder containing feb files
- Executes: Adds attributes to all feb files found in given folder
- Default: local path to "raw" folder
3. PROPERTIES_FOLDER
- Flag: O
- Value: Absolute or local path to folder containing xml properties files
- Default: local path to "properties" folder
4. OUTPUT_FOLDER
- Flag: O
- Value: Absolute or local path to desired output folder
- Default: local path to "with_properties" folder
5. SELECTED_PROPERTIES
- Flag: O
- Value: String used to select properties to be added. Can be:
   - "all": adds all properties found
   - "except": excludes all props-separated-by-dash
   - "props-separated-by-dash": adds only the selected props
- Default: "all"

##### Examples:

Add properties to given feb file with default props:

> main.py ADD_PROPERTIES FEB_FILE raw\myo_tet_4_coarse_1.feb

Add properties to given feb file with default props but excludes the "loads" property:
> main.py ADD_PROPERTIES FEB_FILE raw\myo_tet_4_coarse_1.feb SELECTED_PROPERTIES except-loads

Add properties to all files found in default INPUT_FOLDER:
> main.py ADD_PROPERTIES

Add properties to all files found in default INPUT_FOLDER but excludes the "loads" property:
> main.py ADD_PROPERTIES

#### CREATE_LOADCURVE

> main.py CREATE_LOADCURVE CURVE_NAME teste CURVE_MODEL polynomial CURVE_PARAMS {'coeff':[-944,245,0],'t_initial':0,'t_final':0.2,'resolution':100,'plot':True}

> main.py CREATE_LOADCURVE CURVE_NAME endocardio_loadcurve CURVE_MODEL polynomial CURVE_PARAMS {'coeff':[-944,245,0],'t_initial':0,'t_final':0.2,'resolution':100,'plot':False} 


#### ADD_LOAD

> main.py ADD_LOAD FEB_FILE raw\myo_tet_4_coarse_1.feb LOAD_NAME endocardio



---
## TODO:
List of items that I need to complete (Phase 1):
- [x] Create function to capture and understand sys inputs
- [x] Create class to modify feb files
- [x] Create function ADD_PROPERTIES
- [x] Create function ADD_LOADCURVE (need to be redone in furture)
- [x] Create function ADD_FIBERS
- [x] Create function EXTRACT_NODES
- [x] Create function CREATE_LOADCURVE
- [x] Create function CALCULATE_FIBERS
- [X] Create function CALCULATE_RESULTS
- [x] Create function RUN_FEB



