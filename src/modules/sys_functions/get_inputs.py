from .. enums import POSSIBLE_INPUTS, POSSIBLE_COMMANDS
from .. enums import INPUT_DEFAULTS
from .find_files_in_folder import find_files
from .. logger import console_log as log
from os.path import basename

def get_path_to_FEB_files(inputs):
  """ Gets the path to FEB file given the RA inputs"""
  if POSSIBLE_INPUTS.INPUT_FILE in inputs and inputs[POSSIBLE_INPUTS.INPUT_FILE] != None:
      path_to_feb = inputs[POSSIBLE_INPUTS.INPUT_FILE]
      path_feb_files = [(path_to_feb, basename(path_to_feb), feb_filename[:-4])]
  elif POSSIBLE_INPUTS.FEB_FILE in inputs and inputs[POSSIBLE_INPUTS.FEB_FILE] != None:
      path_to_feb = inputs[POSSIBLE_INPUTS.INPUT_FILE]
      path_feb_files = [(path_to_feb, basename(path_to_feb), feb_filename[:-4])]
  else:
      path_feb_files = find_files(inputs[POSSIBLE_INPUTS.INPUT_FOLDER], ("fileFormat", "feb"))
  return path_feb_files

def get_optional_input(inputs, input_type, action_type):
  inp_val = None
  
  if POSSIBLE_INPUTS[input_type] in inputs and inputs[POSSIBLE_INPUTS[input_type]] != None:
      inp_val = inputs[POSSIBLE_INPUTS[input_type]]
  else:
    if POSSIBLE_INPUTS[input_type] in INPUT_DEFAULTS[POSSIBLE_COMMANDS[action_type]]:
      inp_val = INPUT_DEFAULTS[POSSIBLE_COMMANDS[action_type]][POSSIBLE_INPUTS[input_type]]
      log.log_warning("Using default input <{inp}>: {val}".format(inp=input_type, val=inp_val))
    else:
      log.log_error_header("Error: failed to load default input <{inp}>. Might cause issues.".format(inp=input_type))
      log.log_error("Error caused during getting default value for the given input. Please, make sure that default value exists or try again specifying its value. \nTry: running [COMMAND] --{inp} <value>".format(inp=input_type))
    
  return inp_val

def get_required_input(inputs, input_type, action_type):
  inp_val = None
  
  if inputs[POSSIBLE_INPUTS[input_type]] != None:
    inp_val = inputs[POSSIBLE_INPUTS[input_type]]

  return inp_val