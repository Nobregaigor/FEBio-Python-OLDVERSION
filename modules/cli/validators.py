import os
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt, style_from_dict)

class EmptyValidator(Validator):
  def validate(self, value):
    if len(value.text):
      return True
    else:
        raise ValidationError(
          message="Sorry, you can't leave this blank",
          cursor_position=len(value.text))


class FilePathValidator(Validator):
  def validate(self, value):
    if len(value.text):
      if os.path.isfile(value.text):
        return True
      else:
          raise ValidationError(
            message="File not found",
            cursor_position=len(value.text))
    else:
      raise ValidationError(
          message="Sorry, you can't leave this blank",
          cursor_position=len(value.text))


class DirPathValidator(Validator):
  def validate(self, value):
    if len(value.text):
      if os.path.isdir(value.text):
        return True
      else:
          raise ValidationError(
            message="Directory not found",
            cursor_position=len(value.text))
    else:
      raise ValidationError(
          message="Sorry, you can't leave this blank",
          cursor_position=len(value.text))
