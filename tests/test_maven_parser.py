import os
import pytest
import pandas as pd

from pandas.util.testing import assert_frame_equal

from corna import custom_exception
from corna.inputs import maven_parser
import constants
from fixtures import *


def test_read_input_file_all_correct(get_mergedf_all_correct):
    result_df, result_log, _, _, summary = maven_parser.read_maven_file(constants.MAVEN_FILE, constants.METADATA_FILE)
    test_df = get_mergedf_all_correct
    test_log = {constants.VALIDATION_WARNING: {constants.VALIDATION_ACTION: [],
                                               constants.VALIDATION_MESSAGE: []},
                constants.VALIDATION_ERROR: []}
    assert result_log == test_log
    assert result_df.equals(test_df)
    assert summary == {'Input_Data': {'summary': [{'value': 1, 'label': 'Number of metabolites'},
                                                  {'value': 0, 'label': 'Number of blank intensity cells'},
                                                  {'value': 3, 'label': 'Number of rows'},
                                                  {'value': 1, 'label': 'Number of samples'}],
                                      'title': 'Input_Data'},
                       'Meta_Data': {'summary': [{'value': 'Sample, info1, info2', 'label': 'Fields in metadata'},
                                                 {'value': 12, 'label': 'Number of rows in metadata'}],
                                     'title': 'Meta_Data'}}


def test_read_input_file_no_metadata(get_mergedf_no_metadata):
    test_df = get_mergedf_no_metadata
    test_log = {constants.VALIDATION_WARNING: {constants.VALIDATION_ACTION: [],
                                               constants.VALIDATION_MESSAGE: []},
                constants.VALIDATION_ERROR: []}
    result_df, result_log, _, _, _ = maven_parser.read_maven_file(constants.MAVEN_FILE, None)
    assert result_log == test_log
    assert result_df.equals(test_df)


def test_read_input_file_error_in_maven_file():
    maven_file_path = constants.MAVEN_FILE_INTENSITY_INCORRECT
    result_df, result_log, _, _, _ = maven_parser.read_maven_file(maven_file_path, constants.METADATA_FILE)

    test_log = {constants.VALIDATION_WARNING: {
                constants.VALIDATION_ACTION: [], constants.VALIDATION_MESSAGE: []},
                constants.VALIDATION_ERROR: ['Row Number <b>0</b> : column <b>sample_1</b>'
                                             ' has <b>negative</b> value',
                           'Row Number <b>1</b> : column <b>Label</b> has <b>label_not_in_formula</b> value , '
                           'column <b>sample_1</b> has <b>invalid_intensity_value</b> value']}
    assert result_log == test_log
    assert result_df.empty


def test_read_input_file_warning_in_maven(get_mergedf_warning):
    maven_file_path = constants.MAVEN_FILE_PATH_DUPLICATE_ENTRY
    result_df, result_log, _, _, _ = maven_parser.read_maven_file(maven_file_path, constants.METADATA_FILE)
    test_log = {constants.VALIDATION_WARNING: {constants.VALIDATION_ACTION:
                                                   ['Row is Dropped', 'Row is Dropped'],
                                               constants.VALIDATION_MESSAGE:
        ['Row Number <b>3</b> : column <b>Name-Label</b> has <b>duplicate</b> value',
         'Row Number <b>4</b> : column <b>Name-Label</b> has <b>duplicate</b> value']}, 'errors': []}
    test_df = get_mergedf_warning
    assert result_log == test_log
    assert result_df.equals(test_df)


def test_filtered_data_frame(get_maven_file_extra_sample, get_metadata_df, get_maven_df):
    maven_df = get_maven_file_extra_sample
    metadata_df = get_metadata_df
    test_df = get_maven_df
    result_df = maven_parser.filtered_data_frame(maven_df, metadata_df)

    assert_frame_equal(result_df.sort(axis=1), test_df.sort(axis=1), check_names=True)


def test_get_df_empty():
    test_df = maven_parser.get_df_frm_path()
    assert test_df.empty


def test_get_df_path():
    test_df = maven_parser.get_df_frm_path(constants.MAVEN_FILE)
    assert test_df.empty == False


def test_basic_validation():
    assert maven_parser.check_basic_validation(constants.MAVEN_FILE) == True


def test_get_intersection():
    test_set_1 = set([1, 2, 3])
    test_set_2 = set([3, 4, 5])
    test_intersection = [3]
    assert maven_parser.get_intersection(test_set_1, test_set_2) == test_intersection


def test_get_intersection_empty():
    test_set_1 = set([1, 2, 3])
    test_set_2 = set([6, 4, 5])
    test_intersection = []
    assert maven_parser.get_intersection(test_set_1, test_set_2) == test_intersection


def test_check_df_empty():
    assert maven_parser.check_df_empty(pd.DataFrame())


def test_check_error_present():
    logs = {constants.VALIDATION_ERROR: ['There is one erroe'],
            constants.VALIDATION_WARNING: []}
    assert maven_parser.check_error_present(logs)


def test_basic_validation():
    maven_file_path = constants.MAVEN_FILE_INTENSITY_INCORRECT
    assert maven_parser.check_basic_validation(maven_file_path)


def test_column_name_set(get_maven_df):
    maven_df = get_maven_df
    assert maven_parser.get_column_names_set(maven_df) == set(['Formula',
                                                               'Name', 'sample_1', 'Label'])


def test_unique_column_value(get_maven_df):
    maven_df = get_maven_df
    assert maven_parser.get_unique_column_value(maven_df, 'Name') == set(['Acetic'])


def test_drop_duplicates(get_maven_df):
    maven_df = get_maven_df
    test_df = pd.DataFrame({'Name': ['Acetic'], 'Formula': ['H4C2O2N'],
                            'Label': ['C12 PARENT'], 'sample_1': [0.2274]})
    result_df = maven_parser.drop_duplicate_rows(maven_df, 'Name')
    assert_frame_equal(result_df.sort(axis=1), test_df.sort(axis=1), check_names=True)


def test_get_metadata_df(get_metadata_df):
    test_df = get_metadata_df
    result_df = maven_parser.get_metadata_df(constants.METADATA_FILE)
    assert_frame_equal(result_df.sort(axis=1), test_df.sort(axis=1), check_names=True)


def test_get_sample_column(get_maven_df):
    maven_df = get_maven_df
    assert maven_parser.get_sample_column(maven_df) == ['sample_1']


def test_get_validation_fn_lst():
    assert len(maven_parser.get_validation_fn_lst()) == 6


def test_get_extracted_isotracer():
    assert maven_parser.get_extracted_isotracer('C13-label-1') == 'C13'
    assert maven_parser.get_extracted_isotracer('C12 PARENT') == 'C12 PARENT'


def test_get_extraced_isotracer_df(get_maven_df):
    maven_df = get_maven_df
    test_assert = ['C12 PARENT', 'C13', 'C13']
    assert list(maven_parser.get_extraced_isotracer_df(maven_df)) == test_assert


def test_isotracer_dict(get_maven_df):
    maven_df = get_maven_df
    assert maven_parser.get_isotracer_dict(maven_df) == {'C13': 2, 'C12 PARENT': 1}


def test_get_extracted_element():

    assert maven_parser.get_extracted_element('C3H2O6') == {'H': 2, 'C': 3, 'O': 6}
    assert maven_parser.get_extracted_element('SiH2O6') == {'H': 2, 'Si': 1, 'O': 6}
    assert maven_parser.get_extracted_element('C3H2KFe') == {'H': 2, 'C': 3, 'K': 1, 'Fe': 1}


def test_get_element_list():
    input_df = read_csv(constants.MAVEN_FILE)
    assert maven_parser.get_element_list(input_df) == ['C', 'H', 'O', 'N']

