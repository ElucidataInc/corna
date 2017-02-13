from corna.custom_exception import FileExtensionError,FileEmptyError
from corna.custom_exception import MissingRequiredColumnError,FileExistError
from corna.custom_exception import DataFrameEmptyError
from corna.input_validation import check_if_file_exist,check_file_empty
import pytest
import os


def test_check_if_file_exist():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_not_exist_path = os.path.join(dir_path, "test_input_validation_data", "maven_data.py")

    with pytest.raises(FileExistError) as e:
        check_if_file_exist(file_not_exist_path)

    assert e.value.message == 'The file does not exist. Check again.'


def test_check_file_empty():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    empty_file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.txt")

    with pytest.raises(FileEmptyError) as e:
        check_file_empty(empty_file_path)

    assert e.value.message=='The file is empty. No data to process.'