import numpy as np
from matplotlib import pyplot as plt
from ast import literal_eval
from bs4 import BeautifulSoup
from prettierfier import prettify_xml
from os.path import join

from .. enums import POSSIBLE_INPUTS


def calculate_polynomial(coeff,t_initial,t_final,resolution,plot=False):
	
	coeff.reverse()
	intervals = np.linspace(t_initial,t_final,resolution)
	ys = np.linspace(t_initial,t_final,resolution)

	r_exp = range(len(coeff))
	r_intervals = range(len(intervals))

	for i in r_intervals:
		y = 0
		x = intervals[i]
		for exp in r_exp:
			y += coeff[exp] * (x ** exp)

		ys[i] = y

	if plot:
		plt.plot(intervals,ys)
		plt.show()

	return intervals, ys

POSSIBLE_CURVES = {
	"POLYNOMIAL": calculate_polynomial
}

def create_load_curve_xml(inputs):
	print("\n== Creating load curve ==")
	curve_name  = inputs[POSSIBLE_INPUTS.CURVE_NAME]
	curve_model = inputs[POSSIBLE_INPUTS.CURVE_MODEL].upper()
	curve_type  = inputs[POSSIBLE_INPUTS.CURVE_TYPE].lower()
	curve_folder = inputs[POSSIBLE_INPUTS.CURVE_FOLDER]

	# Check if curve params are correctly inputed
	try:
		curve_params = literal_eval(inputs[POSSIBLE_INPUTS.CURVE_PARAMS])
	except SyntaxError:
		raise(ValueError("Curve params was not properly inputed. Please, make sure it can be decoded into a python dictionary."))

	# Check if model was alredy implemented. If it is, assign the proper curve_function
	if curve_model in POSSIBLE_CURVES:
		curve_function = POSSIBLE_CURVES[curve_model]
	else:
		raise(AssertionError("Curve model provided does not exist or was not properly implemented yet."))

	# Calculate the values for x and y (all curve functions should return xs, ys)
	print("Calculating loadcurve.")
	xs, ys = curve_function(**curve_params)

	# create locarcurve soup
	print("Preparing loadcurve xml")
	loadcurve_template = '<loadcurve id="1">  </loadcurve>'
	point_template = '<point></point>'

	loadcurve_soup = BeautifulSoup(loadcurve_template, "xml")
	loadcurve_soup.loadcurve['type'] = curve_type

	for i, x in enumerate(xs):
		y = ys[i]
		new_tag = loadcurve_soup.new_tag("point")
		new_tag.string = str(x) + "," + str(y)
		loadcurve_soup.loadcurve.insert(i,new_tag)


	with open(join(curve_folder,curve_name + ".xml"), 'w') as file:
		print("Writing loadcurve")
		file.write(prettify_xml(loadcurve_soup.prettify()))
