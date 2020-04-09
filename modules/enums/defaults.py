
from os.path import join
from .possible_commands import POSSIBLE_COMMANDS, POSSIBLE_INPUTS
import pathlib

OUTPUT_FOLDER_DEFAULT_KEY = hash("OUTPUT_FOLDER")

STORAGE_DIR = join("Active","setup_feb_files")
WORKING_DIR = pathlib.Path().absolute()

PATH_TO_STORAGE = join(WORKING_DIR.parents[0], STORAGE_DIR)


INPUT_DEFAULTS = {
	POSSIBLE_COMMANDS.ADD_PROPERTIES: {
		POSSIBLE_INPUTS.PROPERTIES_FOLDER: join(PATH_TO_STORAGE,"Properties"),
		POSSIBLE_INPUTS.OUTPUT_FOLDER: join(PATH_TO_STORAGE,"with_properties"),
		POSSIBLE_INPUTS.SELECTED_PROPERTIES: "all"
	}
}



