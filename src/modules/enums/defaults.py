
from os.path import join
from .possible_commands import POSSIBLE_COMMANDS, POSSIBLE_INPUTS, INPUT_TYPES_ENUM, INPUT_TYPES
import pathlib

import os
from .. sys_functions.read_files import read_json


dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

CONFIG = read_json(join(dir_path,"config.json"))
DEBUG = eval(CONFIG['DEBUG'])

DIRECTORIES = CONFIG['DIRECTORIES']
ID = CONFIG['INPUT_DEFAULTS']

PATH_TO_FEBIOPYTHON = DIRECTORIES['FEBIO_PYTHON']

PATH_TO_README = join(PATH_TO_FEBIOPYTHON, "README.md")
JOIN_DIRS = eval(CONFIG['JOIN_DIRS'])
JOIN_MATLAB_FOLDER = eval(CONFIG['JOIN_MATLAB_FOLDER'])

if JOIN_DIRS == True:
    PATH_TO_STORAGE = join(DIRECTORIES['CORE'], DIRECTORIES['WORKING'], DIRECTORIES['STORAGE'])

else:
    PATH_TO_STORAGE = DIRECTORIES['PATH_TO_STORAGE']


def set_input_defaults():
    input_defaults = {}
    for cmd in CONFIG['INPUT_DEFAULTS']:
        for inp in CONFIG['INPUT_DEFAULTS'][cmd]:
            if INPUT_TYPES[POSSIBLE_INPUTS[inp]] == INPUT_TYPES_ENUM.PATH:
                    if JOIN_DIRS == True:
                        if POSSIBLE_INPUTS[inp] == POSSIBLE_INPUTS.PATH_TO_MATLAB_FOLDER:
                            inp_val = join(PATH_TO_FEBIOPYTHON, ID[cmd][inp])
                        else:
                            inp_val = join(PATH_TO_STORAGE, ID[cmd][inp])
                    
            else:
                inp_val = ID[cmd][inp]

            if POSSIBLE_COMMANDS[cmd] not in input_defaults:
                input_defaults[POSSIBLE_COMMANDS[cmd]] = {
                    POSSIBLE_INPUTS[inp]: inp_val
                }
            else:
                input_defaults[POSSIBLE_COMMANDS[cmd]][POSSIBLE_INPUTS[inp]] = inp_val

    return input_defaults

INPUT_DEFAULTS = set_input_defaults()

# INPUT_DEFAULTS = {
#     POSSIBLE_COMMANDS.ADD_PROPERTIES: {
#         POSSIBLE_INPUTS.INPUT_FOLDER:      join(PATH_TO_STORAGE, ID['ADD_PROPERTIES']['INPUT_FOLDER']),
#         POSSIBLE_INPUTS.PROPERTIES_FOLDER: join(PATH_TO_STORAGE, "properties"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
#         POSSIBLE_INPUTS.SELECTED_PROPERTIES: "all"
#     },
#     POSSIBLE_COMMANDS.CREATE_LOADCURVE: {
#         POSSIBLE_INPUTS.CURVE_FOLDER: join(PATH_TO_STORAGE, "loads"),
#         POSSIBLE_INPUTS.CURVE_TYPE: "smooth",
#     },
#     POSSIBLE_COMMANDS.ADD_LOAD: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_load"),
#         POSSIBLE_INPUTS.LOAD_FOLDER: join(PATH_TO_STORAGE, "loads"),
#         POSSIBLE_INPUTS.LOAD_NAME: "endocardio",
#         POSSIBLE_INPUTS.LOAD_ATTRS: None,
#     },
#     POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "raw"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "geometry_data"),
#     },
#     POSSIBLE_COMMANDS.CALCULATE_FIBERS: {
#         POSSIBLE_INPUTS.FEB_NAME: "all",
#         POSSIBLE_INPUTS.GEOMETRY_DATA_FOLDER: join(PATH_TO_STORAGE, "geometry_data"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "fibers_data"),
#         POSSIBLE_INPUTS.PATH_TO_MATLAB_FOLDER: join(PATH_TO_FEBIOPYTHON, "matlab_functions"),
#         POSSIBLE_INPUTS.MATLAB_PARAMS: "{'endo':45,'epi':75}",
#     },
#     POSSIBLE_COMMANDS.ADD_FIBERS: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
#         POSSIBLE_INPUTS.FIBERS_DATA_FOLDER: join(PATH_TO_STORAGE, "fibers_data"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers")
#     },
#     POSSIBLE_COMMANDS.ADD_FIBERS2: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_properties"),
#         POSSIBLE_INPUTS.FIBERS_DATA_FOLDER: join(PATH_TO_STORAGE, "fibers_data"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers")
#     },
#     POSSIBLE_COMMANDS.PREPARE: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "raw"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers")
#     },
#     POSSIBLE_COMMANDS.RUN_FEB: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "with_fibers"),
#     },
#     POSSIBLE_COMMANDS.CREATE_STORAGE_FOLDER: {
#         POSSIBLE_INPUTS.PATH_TO_STORAGE: join(WORKING_DIR, "Active"),
#     },
#     POSSIBLE_COMMANDS.MODIFY_PARAMETER: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "raw"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "raw"),
#         POSSIBLE_INPUTS.SAVE_AS_NEW: False,
#     },
#     POSSIBLE_COMMANDS.PREPARE_PARAMETER_STUDY: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "raw"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "study2"),
#     },
#     POSSIBLE_COMMANDS.MAKE_PICKLE: {
#         POSSIBLE_INPUTS.INPUT_FOLDER: join(PATH_TO_STORAGE, "study2"),
#         POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE, "study2"),
#     }
# }
