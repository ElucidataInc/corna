import corna.constants as constant
import os
import pandas as pd
import pytest

from corna import custom_exception
from corna import dataframe_validator
from corna import input_validation



def test_check_if_file_exist():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_not_exist_path = os.path.join(dir_path, "test_input_validation_data", "maven_data.py")
    assert dataframe_validator.check_if_file_exist(file_not_exist_path) == False


def test_check_file_empty():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    empty_file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.txt")
    assert dataframe_validator.check_file_empty(empty_file_path) == True

def test_read_input_file():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    other_extension_file_path = os.path.join(dir_path, "test_input_validation_data", "nacorr_test_1.pdf")

    with pytest.raises(custom_exception.FileExtensionError) as e:
        dataframe_validator.read_input_file(other_extension_file_path)

    assert e.value.message == 'Only CSV , TXT , XLS ,XLSX file extension are allowed.'

def test_data_frame_empty():
    data_frame=pd.DataFrame()
    assert dataframe_validator.check_df_empty(data_frame) == True

def test_required_column_missing():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "test_input_validation_data", "test_maven_upload_acetic.csv")
    df = pd.read_csv(file_path)
    test_required_column = ['NaMe','LABEl','Formula','XYZ']

    assert dataframe_validator.check_required_column(df,*test_required_column)[0] == False



def test_check_positive_numerical_value():

    assert input_validation.check_intensity_value(14) == constant.VALID_STATE
    assert input_validation.check_intensity_value(-19) == constant.INTENSITY_STATE_NEGATIVE
    assert input_validation.check_intensity_value('test123') == constant.INTENSITY_STATE_INVALID


def test_check_label_column_format():

    assert input_validation.check_label_column_format('C12 PARENT') == constant.VALID_STATE
    assert input_validation.check_label_column_format('C13-label-2') == constant.VALID_STATE
    assert input_validation.check_label_column_format('C13-2') == constant.LABEL_STATE_INVALID
    assert input_validation.check_label_column_format('C13-label-a') == constant.LABEL_STATE_INVALID
    assert input_validation.check_label_column_format('C11-N15-label-1-2') == constant.LABEL_STATE_INVALID


def test_label_in_formula():

    assert input_validation.check_label_in_formula('C13-label-2','C10H12N5O6P') == constant.VALID_STATE
    assert input_validation.check_label_in_formula('C13-label-6', 'C5H12N5O6P') == constant.LABEL_STATE_NUMBER_MORE_FORMULA
    assert input_validation.check_label_in_formula('C13-label-6', 'H12N5O6P') == \
                                                                    constant.LABEL_STATE_NOT_FORMULA


def test_get_label():

    assert input_validation.get_label('C12 PARENT') == {'C': 0, 'N': 0}
    assert input_validation.get_label('C13-label-6') == {'C': 6}
    assert input_validation.get_label('C13N15-label-4-5') == {'C': 4, 'N': 5}


def test_check_formula_is_correct():

    assert input_validation.check_formula_is_correct('C5H12N5O6P') == constant.VALID_STATE
    assert input_validation.check_formula_is_correct('C5H12N5O6PLO') == constant.FORMULA_STATE_INVALID


def test_check_duplicate():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_correct_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                          "test_maven_upload_acetic.csv")
    maven_df_correct = pd.read_csv(maven_correct_raw_file)
    maven_duplicate_entry_file=os.path.join(dir_path, "test_input_validation_data",
                                            "test_maven_upload_duplicate_entry.csv")
    maven_df_duplicate_entry=pd.read_csv(maven_duplicate_entry_file)

    print input_validation.check_duplicate(maven_df_duplicate_entry,0,[['Name','Label']])
    print input_validation.check_duplicate(maven_df_correct,0,[['Name','Label']]).empty


def test_check_missing():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_missing_entry_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                "test_maven_upload_missing_entry.csv")
    maven_missing_entry_df = pd.read_csv(maven_missing_entry_raw_file)
    assert len(input_validation.check_missing(maven_missing_entry_df)) == 2

def test_validator_for_two_column():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_raw_label_not_in_formula_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                "test_maven_upload_acetic_label_incorrect.csv")
    maven_df = pd.read_csv(maven_raw_label_not_in_formula_raw_file)

    result_df = input_validation.validator_for_two_column(maven_df,constant.LABEL_COL,constant.FORMULA_COL,
                                                          input_validation.check_label_in_formula)

    assert result_df.iloc[0]['row_number'] == 1

def test_validator_column_wise():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    maven_raw_intensity_not_correct_raw_file = os.path.join(dir_path, "test_input_validation_data",
                                                           "test_maven_upload_acetic_intensity_incorrect.csv")
    maven_df = pd.read_csv(maven_raw_intensity_not_correct_raw_file)

    result_df = input_validation.validator_column_wise(maven_df,0,['sample_1'],
                                                       [input_validation.check_intensity_value])
    assert result_df.iloc[0]['state'] == 'negative'
    assert result_df.iloc[1]['state'] == 'invalid_intensity_value'


def test_get_isotope_name():

    assert input_validation.get_isotope_name(['C13','N15']) == ['C','N']


def test_get_istopes_name_and_number():
    label = 'C13N15-label-1-2'
    label_isotopes,label_number = input_validation.get_isotopes_name_and_number(label)

    assert label_isotopes == ['C','N']
    assert label_number == [1,2]

def test_get_split_isotopes():
    joined_isotopes = 'C13N15'

    assert input_validation.get_split_isotopes(joined_isotopes) == ['C13','N15']