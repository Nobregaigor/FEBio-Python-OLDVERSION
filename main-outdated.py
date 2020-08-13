from modules import get_input_arguments, COMMAND_FUNCTION

if __name__ == "__main__":
	command, inputs = get_input_arguments()
	COMMAND_FUNCTION[command](inputs)
