

Sample commands:

## ADD_PROPERTIES

The function ADD_PROPERTIES can be used to insert properties saved in xml formats in a given folder.

The inputs are:
	-> FEB_FILE
		- Flag: R1
		- Value: Absolute or local path to feb file
		- Executes: Adds attributes to given feb file
	-> INPUT_FOLDER
		- Flag: O1
		- Value: Absolute or local path to folder containing feb files
		- Executes: Adds attributes to all feb files found in given folder
		- Default: local path to "raw" folder
	-> PROPERTIES_FOLDER
		- Flag: O
		- Value: Absolute or local path to folder containing xml properties files
		- Default: local path to "properties" folder
	-> OUTPUT_FOLDER
		- Flag: O
		- Value: Absolute or local path to desired output folder
		- Default: local path to "with_properties" folder
	-> SELECTED_PROPERTIES
		- Flag: O
		- Value: String used to select properties to be added. Can be:
			-- "all": adds all properties found
			-- "except": excludes all props-separated-by-dash
			-- "props-separated-by-dash": adds only the selected props
		- Default: "all"

# Examples:
	- main.py ADD_PROPERTIES FEB_FILE raw\myo_tet_4_coarse_1.feb
		--> add properties to given feb file with default props
	- main.py ADD_PROPERTIES FEB_FILE raw\myo_tet_4_coarse_1.feb SELECTED_PROPERTIES except-loads
		--> add properties to given feb file with default props but excludes the "loads" property
	- main.py ADD_PROPERTIES
		--> add properties to all files found in default INPUT_FOLDER
	- main.py ADD_PROPERTIES
		--> add properties to all files found in default INPUT_FOLDER but excludes the "loads" property