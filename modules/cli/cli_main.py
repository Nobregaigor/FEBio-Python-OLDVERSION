

import click
import webbrowser
from ..enums.possible_commands import POSSIBLE_COMMANDS, POSSIBLE_INPUTS, COMMAND_INPUT, INPUT_FLAG
from ..enums.defaults import INPUT_DEFAULTS
from .. sys_functions import update_readme

from .. import COMMAND_FUNCTION
# from ..cli import console_log as log
from ..logger import console_log as log

import json

# Load help texts
PATH_TO_HELP_TEXT = './jsons/helptexts.json'
with open(PATH_TO_HELP_TEXT) as f:
  json_data = json.load(f)
  IO_HELP_TEXTS = json_data['INPUT-OPTIONS']
  CM_HELP_TEXTS = json_data['COMMANDS']


def interface_pi_with_cli(pi):
    return '--{}'.format(pi.name)

CLI_INPUTS = {pi: interface_pi_with_cli(pi) for pi in POSSIBLE_INPUTS}

def map_cli_inputs_to_pi(inputs_dict):
    """ Maps returned kargs list to POSIIBLE_INPUTS payload"""
    return {POSSIBLE_INPUTS[ka.upper()]: inputs_dict[ka] for ka in inputs_dict}

def set_check_requirements(command):
    required = [v[1] for v in COMMAND_INPUT[command] if v[0] == INPUT_FLAG.R]
    alternative = [v[1] for v in COMMAND_INPUT[command] if v[0] == INPUT_FLAG.RA]
    return required, alternative

def assert_payload(action, payload):
    """ Asserts that function has at least the proper file or foler inputs """
    # fail = True
    failed_by_required = True
    failed_by_alternative = True

    required, alternative = set_check_requirements(action)
    
    # Check for required inputs (does not have a default value)
    if len(required) > 0:
        for v in required:
            if v not in payload:
                failed_by_required = True
            else:
                failed_by_required = False if payload[v] != None else True
    else:
        failed_by_required = False

    # Check for alternative inputs (if not supplied, might have a default value)
    if len(alternative) > 0:
        for v in alternative:
            if v in payload:
                if payload[v] != None:
                    failed_by_alternative = False
    else:
        failed_by_alternative = False

    # If user did not supply an alternative value, check for defaults
    if failed_by_alternative == True:
        log.log_warning_header("Warning: one of the required alternatives is missing. Will try to apply defaults.")
        for v in alternative:
            if v in INPUT_DEFAULTS[action]:
                log.log_warning("Default found: Payload <{p}> will be replaced by default value: '{v}'.".format(p=v.name, v=INPUT_DEFAULTS[action][v]), indent=2, ind_ch='>')
                payload[v] = INPUT_DEFAULTS[action][v]
                failed_by_alternative = False
    
    # Check for fail type
    fail = True if failed_by_alternative == True or failed_by_required == True else False

    # If errors are present, log error and return error message
    if fail == True:
        err_reason = ""

        if failed_by_required:
            err_reason += "input required {}".format([v.name for v in required])
        
        if failed_by_alternative:
            if failed_by_required == True:
                err_reason += ", and "
            err_reason += "input required one from alternatives {}".format([v.name for v in alternative])
        
        fail_message = "Does not contain: {}".format(err_reason)
    else:
        fail_message = None

    return payload, (fail, fail_message)

#! run command function
def run_command(action, kargs):
    # set payload
    payload = map_cli_inputs_to_pi(kargs)

    # Perform a low level payload check
    payload, (fail, fail_message) = assert_payload(action, payload)
    if fail == True:
        log.log_error_header("Failed at low level check of action payload")
        log.log_error(fail_message, indent=2, ind_ch=">")
        return -1
    else:
        return COMMAND_FUNCTION[action](payload)

#! =========================================
#! Setting up click
#! =========================================

#! - - - - - - - - - - - - - - - - - - - - -
#! Main click group
@click.group()
def main():
    pass

#! - - - - - - - - - - - - - - - - - - - - -
#! run command -> click sub group
@main.group(short_help="Executes a given command. Ask 'run --help' to learn more.", help="Executes one of the commands listed below.")
def run():
    pass

#! ADD_PROPERTIES
@run.command(short_help=CM_HELP_TEXTS['ADD_PROPERTIES']['short'], help=CM_HELP_TEXTS['ADD_PROPERTIES']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.PROPERTIES_FOLDER], '-pf', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['PROPERTIES_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.SELECTED_PROPERTIES], '-sp', type=click.STRING, help=IO_HELP_TEXTS['SELECTED_PROPERTIES'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.EXCLUDE_PROPERTIES], '-ep', type=click.STRING, help=IO_HELP_TEXTS['EXCLUDE_PROPERTIES'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def ADD_PROPERTIES(**kargs):
    return run_command(POSSIBLE_COMMANDS.ADD_PROPERTIES, kargs)

#! ADD_FIBERS
@run.command(short_help=CM_HELP_TEXTS['ADD_FIBERS']['short'], help=CM_HELP_TEXTS['ADD_FIBERS']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FIBERS_DATA_FOLDER], '-df', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['FIBERS_DATA_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def ADD_FIBERS(**kargs):
    return run_command(POSSIBLE_COMMANDS.ADD_FIBERS, kargs)

#! CREATE_LOADCURVE
@run.command(short_help=CM_HELP_TEXTS['CREATE_LOADCURVE']['short'], help=CM_HELP_TEXTS['CREATE_LOADCURVE']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CURVE_NAME], '-n', type=click.STRING, help=IO_HELP_TEXTS['CURVE_NAME'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CURVE_MODEL], '-m', type=click.STRING, help=IO_HELP_TEXTS['CURVE_MODEL'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CURVE_PARAMS], '-p', type=click.STRING, help=IO_HELP_TEXTS['CURVE_PARAMS'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CURVE_TYPE], '-t', type=click.STRING, help=IO_HELP_TEXTS['CURVE_TYPE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CURVE_FOLDER], '-f', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['CURVE_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def CREATE_LOADCURVE(**kargs):
    return run_command(POSSIBLE_COMMANDS.CREATE_LOADCURVE, kargs)

#! ADD_LOAD
@run.command(short_help=CM_HELP_TEXTS['ADD_LOAD']['short'], help=CM_HELP_TEXTS['ADD_LOAD']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.LOAD_FOLDER], '-lf', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['LOAD_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.LOAD_NAME], '-ln', type=click.STRING, help=IO_HELP_TEXTS['LOAD_NAME'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.LOAD_ATTRS], '-la', type=click.STRING, help=IO_HELP_TEXTS['LOAD_ATTRS'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def ADD_LOAD(**kargs):
    return run_command(POSSIBLE_COMMANDS.ADD_LOAD, kargs)

#! EXTRACT_GEOMETRY_DATA
@run.command(short_help=CM_HELP_TEXTS['EXTRACT_GEOMETRY_DATA']['short'], help=CM_HELP_TEXTS['EXTRACT_GEOMETRY_DATA']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def EXTRACT_GEOMETRY_DATA(**kargs):
    return run_command(POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA, kargs)

#! CALCULATE_FIBERS
@run.command(short_help=CM_HELP_TEXTS['CALCULATE_FIBERS']['short'], help=CM_HELP_TEXTS['CALCULATE_FIBERS']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_NAME], '-n', type=click.STRING, help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.GEOMETRY_DATA_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['GEOMETRY_DATA_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.PATH_TO_MATLAB_FOLDER], '-m', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['PATH_TO_MATLAB_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.MATLAB_PARAMS], '-p', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['MATLAB_PARAMS'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def CALCULATE_FIBERS(**kargs):
    return run_command(POSSIBLE_COMMANDS.CALCULATE_FIBERS, kargs)

#! PREPARE
@run.command(short_help=CM_HELP_TEXTS['PREPARE']['short'], help=CM_HELP_TEXTS['PREPARE']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def PREPARE(**kargs):
    return run_command(POSSIBLE_COMMANDS.PREPARE, kargs)

#! RUN_FEB
@run.command(short_help=CM_HELP_TEXTS['RUN_FEB']['short'], help=CM_HELP_TEXTS['RUN_FEB']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
def RUN_FEB(**kargs):
    return run_command(POSSIBLE_COMMANDS.RUN_FEB, kargs)

#! CREATE_STORAGE_FOLDER
@run.command(short_help=CM_HELP_TEXTS['CREATE_STORAGE_FOLDER']['short'], help=CM_HELP_TEXTS['CREATE_STORAGE_FOLDER']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.STORAGE_NAME], '-n', type=click.STRING, help=IO_HELP_TEXTS['STORAGE_NAME'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.PATH_TO_STORAGE], '-p', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['PATH_TO_STORAGE'])
def CREATE_STORAGE_FOLDER(**kargs):
    return run_command(POSSIBLE_COMMANDS.CREATE_STORAGE_FOLDER, kargs)

#! CALCULATE_RESULTS
@run.command(short_help=CM_HELP_TEXTS['CALCULATE_RESULTS']['short'], help=CM_HELP_TEXTS['CALCULATE_RESULTS']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
def CALCULATE_RESULTS(**kargs):
    return run_command(POSSIBLE_COMMANDS.CALCULATE_RESULTS, kargs)

#! MODIFY_PARAMETER
@run.command(short_help=CM_HELP_TEXTS['MODIFY_PARAMETER']['short'], help=CM_HELP_TEXTS['MODIFY_PARAMETER']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.PARAM_VALS], '-p', type=click.STRING, help=IO_HELP_TEXTS['PARAM_VALS'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.SAVE_AS_NEW], '-n', type=click.STRING, help=IO_HELP_TEXTS['SAVE_AS_NEW'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def MODIFY_PARAMETER(**kargs):
    return run_command(POSSIBLE_COMMANDS.MODIFY_PARAMETER, kargs)

#! PREPARE_PARAMETER_STUDY
@run.command(short_help=CM_HELP_TEXTS['PREPARE_PARAMETER_STUDY']['short'], help=CM_HELP_TEXTS['PREPARE_PARAMETER_STUDY']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.CONFIG_FILE], '-c', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['CONFIG_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FILE], '-i', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['INPUT_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.FEB_FILE], '-feb', type=click.Path(exists=True, dir_okay=False), help=IO_HELP_TEXTS['FEB_FILE'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def PREPARE_PARAMETER_STUDY(**kargs):
    return run_command(POSSIBLE_COMMANDS.PREPARE_PARAMETER_STUDY, kargs)

#! MAKE_PICKLE
@run.command(short_help=CM_HELP_TEXTS['MAKE_PICKLE']['short'], help=CM_HELP_TEXTS['MAKE_PICKLE']['long'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.INPUT_FOLDER], '-f', type=click.Path(exists=True, file_okay=False), help=IO_HELP_TEXTS['INPUT_FOLDER'])
@click.option(CLI_INPUTS[POSSIBLE_INPUTS.OUTPUT_FOLDER], '-o', type=click.Path(file_okay=False), help=IO_HELP_TEXTS['OUTPUT_FOLDER'])
def MAKE_PICKLE(**kargs):
    return run_command(POSSIBLE_COMMANDS.MAKE_PICKLE, kargs)


#! - - - - - - - - - - - - - - - - - - - - -
#! readme command -> click sub group
@main.group(short_help="Simple CLI to display and manage README", help="Executes one of the commands listed below.")
def readme():
    pass

@readme.command(short_help="Display README", help="Display README")
def show():
    update_readme.print_readme()

@readme.command(short_help="Update descriptions of possible inputs", help="Update descriptions of possible inputs")
def update_input_descriptions():
    update_readme.update_input_descriptions()

@readme.command(short_help="Display descriptions of possible commands", help="Display descriptions of possible commands")
def update_command_descriptions():
    update_readme.update_command_descriptions()

@readme.command(short_help="Display descriptions of possible commands", help="Display descriptions of possible commands")
def update_reference_list():
    update_readme.update_reference_list()

#! - - - - - - - - - - - - - - - - - - - - -
#! run command -> click sub group
@main.command(short_help="Open FEBio-Python in Browser")
def open_repo():
  webbrowser.open('https://github.com/Nobregaigor/FEBio-Python')
  log.log("Openning FEBio-Python in browser. Thanks for checking it out!", "cyan") 




