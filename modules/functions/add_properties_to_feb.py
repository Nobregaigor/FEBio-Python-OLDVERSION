from copy import copy

from .. enums import POSSIBLE_INPUTS
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup
from .. classes import FEBio_xml_parser


def add_properties_to_feb(inputs):
    print("\n== Adding properties ==")

    # Get inputs
    if POSSIBLE_INPUTS.FEB_FILE in inputs:
        path_to_feb = inputs[POSSIBLE_INPUTS.FEB_FILE]
        feb_filename = path_to_feb.split("\\")[-1]
        path_feb_files = [(path_to_feb, feb_filename, feb_filename[:-4])]
    else:
        path_feb_files = find_files(
            inputs[POSSIBLE_INPUTS.INPUT_FOLDER], ("fileFormat", "feb"))

    # path_feb_file = inputs[POSSIBLE_INPUTS.FEB_FILE]
    path_p_folder = inputs[POSSIBLE_INPUTS.PROPERTIES_FOLDER]
    path_o_folder = inputs[POSSIBLE_INPUTS.OUTPUT_FOLDER]
    selected_prop = inputs[POSSIBLE_INPUTS.SELECTED_PROPERTIES].lower()

    # Determine which properties should include
    excluded_files = []
    selected_files = []
    if selected_prop.find("except") != -1:
        add_all = False
        excluded_files = selected_prop.strip("except").split("-")
        print("*** Warning: The following properties will be excluded:", excluded_files)
    elif selected_prop == "all":
        add_all = True
    else:
        add_all = False
        selected_files = selected_prop.split()

    # Get prop files avaiable
    properties_files = find_files(path_p_folder, ("fileFormat", "xml"))
    # filder found files
    # Create a dict with avaiable props if they are in selected props
    properties = []
    # for file in properties_files:
    #     if function_type == "all":
    #         properties.append((file[2], read_xml(file[0])))
    #     elif function_type == "except":
    #         if file[2] not in excluded_files:
    #             properties.append((file[2], read_xml(file[0])))
    #     else:
    #         if file[2] in selected_files:
    #             properties.append((file[2], read_xml(file[0])))

    for path_feb_file in path_feb_files:
        # Create FEBio_soup instace
        print("\n--> Adding properties to:", path_feb_file[2])
        febio_soup = FEBio_xml_parser.FEBio_xml_parser(path_feb_file[0])
        # Insert properties as tags for each selected property
        for file in properties_files:
            if add_all == True:
                febio_soup.add_tag(file[0])
            else:
                if len(excluded_files) > 0 and file[2] in excluded_files:
                    pass
                if len(selected_files) > 0 and file in selected_files:
                    febio_soup.add_tag(file[0])
                else:
                    febio_soup.add_tag(file[0])
                

        # Write new feb file at given folder
        febio_soup.write_feb(path_o_folder, path_feb_file[1])
