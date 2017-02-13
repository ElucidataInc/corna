from corna.custom_exception import FileExtensionError,FileEmptyError
from corna.custom_exception import MissingRequiredColumnError,FileExistError
from corna.custom_exception import DataFrameEmptyError
from corna.input_validation import check_if_file_exist,check_file_empty
from corna.input_validation import read_input_file,check_data_frame_empty
from corna.input_validation import validate_input_file
import pytest
import os
import pandas as pd

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

def test_read_input_file():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    other_extension_file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.pdf")

    with pytest.raises(FileExtensionError) as e:
        read_input_file(other_extension_file_path)

    assert e.value.message=='Only CSV , TXT , XLS ,XLSX file extension are allowed.'

def test_data_frame_empty():
    data_frame=pd.DataFrame()

    with pytest.raises(DataFrameEmptyError) as e:
        check_data_frame_empty(data_frame)

    assert e.value.message=='There is no data to process.'

def test_required_column_missing():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.xlsx")
    test_required_column=('NaMe','LABEl','Formula','XYZ')

    with pytest.raises(MissingRequiredColumnError) as e:
        validate_input_file(file_path,test_required_column)

    assert e.value.message=='The required column XYZ are not present'
