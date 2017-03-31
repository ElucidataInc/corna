"""This module helps to do validation using validation package olmonk"""

from corna.olmonk import basic_validation

def get_validation_df(path, required_columns=None):
	"""takes path of the file, validates it and returns result

	Using path of the file, it instantiates the validation class
	and use its methods to validate file and returns result of
	that. If file not passes the validation checks, then it will
	raise an error, otherwise it will returns validated df.
	Args:
		path: file path for which validation is needed

	Returns: validated df
	"""
	try:
		basic_validator = get_class_inst(basic_validation.BasicValidator, path, required_columns)
		basic_validation_result(basic_validator)
		return basic_validator
	except Exception as e:
		raise

def get_class_inst(validator_class, file_path, required_columns):
	"""Instantiates class with its argument and returns its instance"""

	return validator_class(file_path, required_columns)

def basic_validation_result(basic_validator):
	"""Takes instance of class, do basic validation and raise error
	if any check fails
	"""

	try:
		basic_validator.check_path_exist()
		basic_validator.check_file_empty()
		basic_validator.check_if_convert_to_df()
	except Exception as e:
		raise


