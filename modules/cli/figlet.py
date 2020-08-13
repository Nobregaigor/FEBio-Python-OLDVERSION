from pyfiglet import Figlet

HEADER_TEXT = "FEBio-Python"
HEADER_FIGLET = Figlet(font='slant')

def get_header():
  return HEADER_FIGLET

def print_header():
  HEADER_FIGLET.renderText(HEADER_FIGLET)