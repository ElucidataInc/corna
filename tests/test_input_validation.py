import corna.constants as constant
from corna.custom_exception import DataFrameEmptyError
from corna.custom_exception import FileExtensionError,FileEmptyError
from corna.custom_exception import MissingRequiredColumnError,FileExistError
from corna.dataframe_validator import check_if_file_exist,check_file_empty
from corna.dataframe_validator import read_input_file,check_data_frame_empty
from corna.input_validation import check_duplicate,get_label,check_label_in_formula
from corna.input_validation import check_formula_is_correct,validator_for_two_column
from corna.input_validation import check_postive_numerical_value,check_label_column_format
from corna.input_validation import validator_column_wise
from corna.input_validation import validate_input_file,check_missing
import os
import pandas as pd
import pytest



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

    assert e.value.message == 'The file is empty. No data to process.'

def test_read_input_file():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    other_extension_file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.pdf")

    with pytest.raises(FileExtensionError) as e:
        read_input_file(other_extension_file_path)

    assert e.value.message == 'Only CSV , TXT , XLS ,XLSX file extension are allowed.'

def test_data_frame_empty():
    data_frame=pd.DataFrame()

    with pytest.raises(DataFrameEmptyError) as e:
        check_data_frame_empty(data_frame)

    assert e.value.message == 'There is no data to process.'

def test_required_column_missing():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.xlsx")
    test_required_column = ('NaMe','LABEl','Formula','XYZ')

    with pytest.raises(MissingRequiredColumnError) as e:
        validate_input_file(file_path,test_required_column)

    assert e.value.message == 'The required column XYZ are not present'


def test_check_positive_numerical_value():

    assert check_postive_numerical_value(14) == constant.VALID_STATE
    assert check_postive_numerical_value(-19) == constant.INTENSITY_STATE_NEGATIVE
    assert check_postive_numerical_value('test123') == constant.INTENSITY_STATE_INVALID


def test_check_label_column_format():

    assert check_label_column_format('C12 PARENT') == constant.VALID_STATE
    assert check_label_column_format('C13-label-2') == constant.VALID_STATE
    assert check_label_column_format('C13-2') == constant.LABEL_STATE_INVALID
    assert check_label_column_format('C13-label-a') == constant.LABEL_STATE_INVALID
    assert check_label_column_format('C11-N15-label-1-2') == constant.LABEL_STATE_INVALID


def test_label_in_formula():

    assert check_label_in_formula('C13-label-2','C10H12N5O6P') == constant.VALID_STATE
    assert check_label_in_formula('C13-label-6', 'C5H12N5O6P') == constant.LABEL_STATE_NUMBER_MORE_FORMULA
    assert check_label_in_formula('C13-label-6', 'H12N5O6P') == constant.LABEL_STATE_NOT_FORMULA


def test_get_label():

    assert get_label('C12 PARENT') == {'C': 0, 'N': 0}
    assert get_label('C13-label-6') == {'C': 6}
    assert get_label('C13N15-label-4-5') == {'C': 4, 'N': 5}


def test_check_formula_is_correct():

    assert check_formula_is_correct('C5H12N5O6P') == constant.VALID_STATE
    assert check_formula_is_correct('C5H12N5O6PLO') == constant.FORMULA_STATE_INVALID


def test_check_duplicate():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_correct_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                          "test_maven_upload_acetic.csv")
    maven_df_correct = pd.read_csv(maven_correct_raw_file)
    maven_duplicate_entry_file=os.path.join(dir_path, "test_input_validation_data",
                                            "test_maven_upload_duplicate_entry.csv")
    maven_df_duplicate_entry=pd.read_csv(maven_duplicate_entry_file)

    assert len(check_duplicate(maven_df_duplicate_entry,0,[['Name','Label']])) == 2
    assert check_duplicate(maven_df_correct,0,[['Name','Label']]).empty


def test_check_missing():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_missing_entry_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                "test_maven_upload_missing_entry.csv")
    maven_missing_entry_df = pd.read_csv(maven_missing_entry_raw_file)
    assert len(check_missing(maven_missing_entry_df)) == 2

def test_validator_for_two_column():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_raw_label_not_in_formula_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                "test_maven_upload_acetic_label_incorrect.csv")
    maven_df = pd.read_csv(maven_raw_label_not_in_formula_raw_file)

    result_df = validator_for_two_column(maven_df,constant.LABEL_COL,constant.FORMULA_COL,
                                check_label_in_formula)

    assert result_df.iloc[0]['row_number'] == 1

def test_validator_column_wise():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_raw_intensity_not_correct_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                           "test_maven_upload_acetic_intensity_incorrect.csv")
    maven_df = pd.read_csv(maven_raw_intensity_not_correct_raw_file)

    result_df = validator_column_wise(maven_df,0,['sample_1'],[check_postive_numerical_value])
    assert result_df.iloc[0]['state'] == 'negative'
    assert result_df.iloc[1]['state'] == 'invalid_intensity_value'

