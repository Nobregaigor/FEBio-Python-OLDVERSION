from copy import copy

from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS
from .. enums import INPUT_DEFAULTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. sys_functions.get_inputs import *

from .. classes import FEBio_soup
from .. classes import FEBio_xml_parser
from .. logger import console_log as log


from os.path import basename

def add_properties_to_feb(inputs):
    function_name = 'ADD_PROPERTIES'
    log.log_step("\n== {} ==\n".format(function_name))
    

    # GET RA Inputs
    path_feb_files = get_path_to_FEB_files(inputs)
    
    # Get optional Inputs
    path_p_folder = get_optional_input(inputs, 'PROPERTIES_FOLDER', function_name)
    selected_prop = get_optional_input(inputs, 'SELECTED_PROPERTIES', function_name)
    exclude_props = get_optional_input(inputs, 'EXCLUDE_PROPERTIES', function_name)
    path_o_folder = get_optional_input(inputs, 'OUTPUT_FOLDER', function_name)

    if selected_prop != None:
        selected_prop = selected_prop.lower()
    if exclude_props != None:
        exclude_props = exclude_props.lower()

    # Determine which properties should include
    excluded_files = []
    selected_files = []
    if exclude_props != None:
        add_all = False
        excluded_files = exclude_props.split("-")
    
    if selected_prop == "all":
        add_all = True
    else:
        add_all = False
        selected_files = selected_prop.split("-")

    # Get prop files avaiable
    properties_files = find_files(path_p_folder, ("fileFormat", "xml"))
    
    for path_feb_file in path_feb_files:
        # Create FEBio_soup instace
        log.log_substep("Adding properties to: {}".format(path_feb_file[2]))
        febio_soup = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])
        # Insert properties as tags for each selected property
        for file in properties_files:
            if add_all == True and excluded_files == None:
                febio_soup.add_tag(file[0])
            else:
                if len(excluded_files) > 0 and file[2] in excluded_files:
                    continue
                if len(selected_files) > 0 and file in selected_files:
                    febio_soup.add_tag(file[0])
                else:
                    febio_soup.add_tag(file[0])
                

        # Write new feb file at given folder
        febio_soup.write_feb(path_o_folder, path_feb_file[1])
