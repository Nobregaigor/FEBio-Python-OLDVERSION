
from .. functions.add_properties_to_feb import add_properties_to_feb
from .. functions.create_loadcurve_xml import create_load_curve_xml
from .. functions.add_loadcurve_to_feb import add_loadcurve_to_feb
from .. functions.extract_geometry_data_from_feb import extract_geometry_data_from_feb
from .. functions.calculate_fibers import calculate_fibers
from .. functions.add_fibers_to_feb import add_fibers_to_feb
from .. functions.add_fibers_to_feb2 import add_fibers_to_feb2
from .. functions.prepare_feb import prepare_feb
from .. functions.run_feb import run_feb
from .. functions.create_storage_folder import create_storage_folder
from .. functions.modify_parameter import modify_parameter
from .. functions.prepare_parameter_study import prepare_parameter_study
from .. functions.make_ml_dataset import make_ml_dataset

from .possible_commands import POSSIBLE_COMMANDS


COMMAND_FUNCTION = {
	POSSIBLE_COMMANDS.ADD_PROPERTIES: add_properties_to_feb,
	POSSIBLE_COMMANDS.CREATE_LOADCURVE: create_load_curve_xml,
	POSSIBLE_COMMANDS.ADD_LOAD: add_loadcurve_to_feb,
	POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA: extract_geometry_data_from_feb,
	POSSIBLE_COMMANDS.CALCULATE_FIBERS: calculate_fibers,
	POSSIBLE_COMMANDS.ADD_FIBERS: add_fibers_to_feb,
	POSSIBLE_COMMANDS.ADD_FIBERS2: add_fibers_to_feb2,
	POSSIBLE_COMMANDS.PREPARE: prepare_feb,
	POSSIBLE_COMMANDS.RUN_FEB: run_feb,
	POSSIBLE_COMMANDS.CREATE_STORAGE_FOLDER: create_storage_folder,
	POSSIBLE_COMMANDS.MODIFY_PARAMETER: modify_parameter,
	POSSIBLE_COMMANDS.PREPARE_PARAMETER_STUDY: prepare_parameter_study,
	POSSIBLE_COMMANDS.MAKE_ML_DATASET: make_ml_dataset,
}
