import six
import textwrap
from pyfiglet import figlet_format
from ..enums.defaults import DEBUG

# from clint.textui import puts, colored, indent
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None
try:
    from termcolor import colored
except ImportError:
    print("colored from termcolor could not be loaded.")
    colored = None


# DEBUG = True

def _indent(text, amount, ch=' '):
  return textwrap.indent(' ' + text, amount * ch)


def log(message, color="white", indent=-1, ind_ch=' ', bold=False, font="slant", figlet=False):
  if indent > -1:
    message = _indent(message, indent, ind_ch)

  if colored:
    if not figlet:
      if not bold:
        six.print_(colored(message, color))
      else:
        six.print_(colored(message, color, attrs=['bold']))
    else:
      six.print_(colored(figlet_format(
            message, font=font), color))
  else:
    six.print_(message)

def log_error_header(message, indent=-1, ind_ch=' '):
  log(message, 'red', indent=indent, ind_ch=ind_ch, bold=True)

def log_error(message, indent=-1, ind_ch=' '):
  log(message, 'red', indent=indent, ind_ch=ind_ch, )

def log_warning_header(message, indent=-1, ind_ch=' '):
  log(message, 'yellow', bold=True, indent=indent, ind_ch=ind_ch, )

def log_warning(message, indent=-1, ind_ch=' '):
  log(message, 'yellow', bold=True, indent=indent, ind_ch=ind_ch, )

def log_step(message, bold=False, indent=-1, ind_ch=' '):
  log(message, 'green', bold=False, indent=indent, ind_ch=ind_ch)

def log_substep(message, bold=False, indent=-1, ind_ch=' '):
  prefix = "\n--> " if DEBUG == True else "--> "
  log(prefix + message, 'green', bold=False, indent=indent, ind_ch=ind_ch)

def log_message(message, bold=False, indent=-1, ind_ch=' '):
  if DEBUG == True:
    log(message, 'white', bold=False, indent=indent, ind_ch=ind_ch)