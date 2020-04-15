
from .. functions.add_properties_to_feb import add_properties_to_feb
from .. functions.create_loadcurve_xml import create_load_curve_xml
from .. functions.add_loadcurve_to_feb import add_loadcurve_to_feb
from .. functions.extract_geometry_data_from_feb import extract_geometry_data_from_feb

from .possible_commands import POSSIBLE_COMMANDS


COMMAND_FUNCTION = {
	POSSIBLE_COMMANDS.ADD_PROPERTIES: add_properties_to_feb,
	POSSIBLE_COMMANDS.CREATE_LOADCURVE: create_load_curve_xml,
	POSSIBLE_COMMANDS.ADD_LOAD: add_loadcurve_to_feb,
	POSSIBLE_COMMANDS.EXTRACT_GEOMETRY_DATA: extract_geometry_data_from_feb
}
