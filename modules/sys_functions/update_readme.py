from .. enums import PATH_TO_README
from os.path import join
import json
from .. enums import COMMAND_INPUT, POSSIBLE_COMMANDS

PATH_TO_HELP_TEXT = './jsons/helptexts.json'

h_symb = '###'
sb_symb = '#####'


with open(PATH_TO_HELP_TEXT) as f:
  json_data = json.load(f)
  IO_HELP_TEXTS = json_data['INPUT-OPTIONS']
  CM_HELP_TEXTS = json_data['COMMANDS']

# re
with open(PATH_TO_README, 'r') as f:
  README = f.readlines()



def print_readme():
  for line in README:
    print(line)

def format_input_options(input_options):
  return [[inp, input_options[inp]] for inp in input_options]

def format_commands_long(commands):
  return [[cmd, commands[cmd]['long']] for cmd in commands]

def format_commands_short(commands):
  table = [[cmd, commands[cmd]['short']] for cmd in commands]
  for row in table:
    cmd = row[0]
    inputs = ["<li>{inp} ({req}).</li>".format(req=v[0].name, inp=v[1].name) for v in COMMAND_INPUT[POSSIBLE_COMMANDS[cmd]]]
    row.append("<ul>" + "".join(inputs) + "</ul>")

  return table



def write_table(headers, content):
  # write header
  string = "|".join(headers) + "\n"
  string += "|".join(["-".join("" for i in word) for word in headers]) + "\n"
  # write content
  string += "\n".join(["|".join(col for col in row) for row in content]) 
  return string

def update_input_descriptions():
  input_options = format_input_options(IO_HELP_TEXTS)
  inputs_table  = write_table(['Inputs', 'Description'], input_options)
  readme = README

  # search for headers
  # headers = [(header.split(h_symb), i) for i, header in enumerate(README) if header[:5].find(h_symb) != -1 ]
  subheaders = [(header.replace(sb_symb, ""), i) for (i,header) in enumerate(readme) if header[:5].find(sb_symb) != -1]

  for elem in subheaders:
    if elem[0].find("List of Inputs") != -1:
      index_to_write = elem[1] + 1
      break

  readme.insert(index_to_write, inputs_table)
  with open(PATH_TO_README, 'w') as f:
    f.writelines(readme)

def update_command_descriptions():
  command_options = format_commands_long(CM_HELP_TEXTS)
  command_tables  = write_table(['Commands', 'Description'], command_options)
  readme = README

  # search for headers
  # headers = [(header.split(h_symb), i) for i, header in enumerate(README) if header[:5].find(h_symb) != -1 ]
  subheaders = [(header.replace(sb_symb, ""), i) for (i,header) in enumerate(readme) if header[:5].find(sb_symb) != -1]

  for elem in subheaders:
    if elem[0].find("List of Commands") != -1:
      index_to_write = elem[1] + 1
      break

  readme.insert(index_to_write, command_tables)
  with open(PATH_TO_README, 'w') as f:
    f.writelines(readme)

def update_reference_list():
  command_options = format_commands_short(CM_HELP_TEXTS)
  command_tables  = write_table(['Commands', 'Description', 'Inputs'], command_options)
  readme = README

  # search for headers
  # headers = [(header.split(h_symb), i) for i, header in enumerate(README) if header[:5].find(h_symb) != -1 ]
  subheaders = [(header.replace(sb_symb, ""), i) for (i,header) in enumerate(readme) if header[:5].find(sb_symb) != -1]

  for elem in subheaders:
    if elem[0].find("Reference list") != -1:
      index_to_write = elem[1] + 1
      break

  readme.insert(index_to_write, command_tables)
  with open(PATH_TO_README, 'w') as f:
    f.writelines(readme)






