from copy import copy
from os.path import join
import numpy as np
from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS, INPUT_DEFAULTS, PATH_TO_STORAGE
from .. sys_functions.find_files_in_folder import find_files
from .. sys_functions.read_files import read_xml
from .. classes import FEBio_soup


from .add_properties_to_feb import add_properties_to_feb
from .create_loadcurve_xml import create_load_curve_xml
from .add_loadcurve_to_feb import add_loadcurve_to_feb
from .extract_geometry_data_from_feb import extract_geometry_data_from_feb
from .calculate_fibers import calculate_fibers
from .add_fibers_to_feb import add_fibers_to_feb
from .add_fibers_to_feb2 import add_fibers_to_feb2
from .run_feb import run_feb

from .. sys_functions.get_inputs import get_path_to_FEB_files, get_optional_input
from .. logger import console_log as log

def prepare_feb(inputs):

    # Raw -> with_properties -> with_load
    # Raw -> geometry_data -> fibers_data
    # fibers_data -> with_properties
    # fibers_data -> with_load

    # Set commands in order to be executed

    # Set fiber variations:

    # fibers_variations = [45, 50, 55, 60, 65, 70, 75, 80, 85]
    #endo_range = [np.linspace(-80, -40, 5)]
    #epid_range= -endo_range

    epid_range = [ 42,  47,  54,  58,  63,  69,  71,  78]
    endo_range = [-51, -44, -72, -56, -40, -61, -68, -75]

    fibers_variations = []

    # for endo in endo_range:
    #     for epid in epid_range:
    #         fibers_variations.append((endo, epid))

    for endo, epid in zip(endo_range, epid_range):
        fibers_variations.append((endo, epid))

    #########################################
    # Set order of functions to be executed
    #########################################

    # Part 1: prepare to calculate fibers
    to_execute_1 = [
        # add_properties_to_feb,
        # add_loadcurve_to_feb,
        extract_geometry_data_from_feb,
    ]

    # Part 2: calculate fibers
    to_execute_2 = [calculate_fibers] * len(fibers_variations)

    # Part 3: add fibers
    to_execute_3 = [
        # add_fibers_to_feb,
        add_fibers_to_feb,
    ]

    # Par 4: run feb
    to_execute_4 = [
        run_feb
    ]

    #########################################
    # Set inputs of functions to be executed
    #########################################

    to_input_1 = [
        # INPUT_DEFAULTS[POSSIBLE_COMMANDS.ADD_PROPERTIES],
        # INPUT_DEFAULTS[POSSIBLE_COMMANDS.ADD_LOAD],
        INPUT_DEFAULTS[POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA],
    ]

    to_input_2 = []
    for i, fib_dir in enumerate(fibers_variations):
        print(fib_dir)
        to_input_2.append(
            copy(INPUT_DEFAULTS[POSSIBLE_COMMANDS.CALCULATE_FIBERS]))
        to_input_2[i][POSSIBLE_INPUTS.MATLAB_PARAMS] = "{'endo':" + \
            str(fib_dir[0]) + ",'epi':" + str(fib_dir[1]) + "}"
        # to_input_2[i][POSSIBLE_INPUTS.MATLAB_PARAMS] = "{'endo':" + str(-fib_dir) +",'epi':" + str(fib_dir) + "}"

    to_input_3 = [
        # {
        #     POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
        #     POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers"),
        #     POSSIBLE_INPUTS.FIBERS_DATA_FOLDER: join(PATH_TO_STORAGE, "fibers_data"),
        # },
        {
            POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "raw"), # CHANGE TO WITH LOAD
            POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers"),
            POSSIBLE_INPUTS.FIBERS_DATA_FOLDER: join(PATH_TO_STORAGE, "fibers_data"),
        },
    ]

    to_input_4 = [
        INPUT_DEFAULTS[POSSIBLE_COMMANDS.RUN_FEB],
    ]

    #########################################
    # Combine actions
    #########################################

    to_execute = []
    to_execute.extend(to_execute_1)
    to_execute.extend(to_execute_2)
    to_execute.extend(to_execute_3)
    # to_execute.extend(to_execute_4)

    to_input = []
    to_input.extend(to_input_1)
    to_input.extend(to_input_2)
    to_input.extend(to_input_3)
    # to_input.extend(to_input_4)

    # Execute commands with given inputs

    for i, command in enumerate(to_execute):
        command(to_input[i])


def execute_prepare_feb(inputs):
    prepare_feb(inputs)
