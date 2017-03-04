import os
import pytest
import pandas as pd

from pandas.util.testing import assert_frame_equal

from corna.inputs import maven_parser

dir_path = os.path.dirname(os.path.abspath(__file__))
maven_file = os.path.join(dir_path, "test_input_validation_data", "test_maven_upload_acetic.csv")
metadatafile = os.path.join(dir_path, "test_input_validation_data", "metadata_sample_test_maven.csv")


@pytest.fixture()
def read_csv(path):
    return pd.read_csv(path)



def test_read_input_file_all_correct():
    test_df_path = os.path.join(dir_path, "test_input_validation_data", "test_mergedf_all_correct.csv")
    result_df, result_log, _ = maven_parser.read_maven_file(maven_file, metadatafile)
    test_df = read_csv(test_df_path)
    test_log = {'warning': {'action': [], 'message': []}, 'errors': []}
    assert result_log == test_log
    assert result_df.equals(test_df)


def test_read_input_file_no_metadata():
    test_df_path = os.path.join(dir_path, "test_input_validation_data", "test_mergedf_no_metadata.csv")
    test_df = read_csv(test_df_path)
    test_log = {'warning': {'action': [], 'message': []}, 'errors': []}
    result_df, result_log, _ = maven_parser.read_maven_file(maven_file, None)
    assert result_log == test_log
    assert result_df.equals(test_df)


def test_read_input_file_error_in_maven_file():
    maven_file_path = os.path.join(dir_path, "test_input_validation_data",
                                   "test_maven_upload_acetic_intensity_incorrect.csv")
    result_df, result_log, _ = maven_parser.read_maven_file(maven_file_path, metadatafile)

    test_log = {'warning': {'action': [], 'message': []},
                'errors': ['Row Number <b>0</b> : column <b>sample_1</b> has <b>negative</b> value',
                 'Row Number <b>1</b> : column <b>Label</b> has <b>label_not_in_formula</b> value , '
                 'column <b>sample_1</b> has <b>invalid_intensity_value</b> value']}
    assert result_log == test_log
    assert result_df.empty


def test_read_input_file_warning_in_maven():
    test_df_path = os.path.join(dir_path, "test_input_validation_data", "test_mergedf_warning.csv")
    maven_file_path = os.path.join(dir_path, "test_input_validation_data",
                                   "test_maven_upload_duplicate_entry.csv")
    result_df, result_log,_= maven_parser.read_maven_file(maven_file_path, metadatafile)
    test_log = {'warning': {'action': ['Row is Dropped', 'Row is Dropped'], 'message':
        ['Row Number <b>3</b> : column <b>Name-Label</b> has <b>duplicate</b> value',
         'Row Number <b>4</b> : column <b>Name-Label</b> has <b>duplicate</b> value']}, 'errors': []}
    test_df = read_csv(test_df_path)
    assert result_log == test_log
    assert result_df.equals(test_df)


def test_filtered_data_frame():
    maven_file_path = os.path.join(dir_path, "test_input_validation_data",
                                   "test_maven_upload_acetic_extra_sample.csv")
    maven_df = read_csv(maven_file_path)
    metadata_df = read_csv(metadatafile)
    test_df = read_csv(maven_file)
    result_df = maven_parser.filtered_data_frame(maven_df, metadata_df)

    assert_frame_equal(result_df.sort(axis=1), test_df.sort(axis=1), check_names=True)


def test_get_df_empty():
    test_df = maven_parser.get_df_frm_path()
    assert test_df.empty


def test_get_df_path():
    test_df = maven_parser.get_df_frm_path(maven_file)
    assert test_df.empty == False


def test_basic_validation():
    assert maven_parser.check_basic_validation(maven_file) == True


def test_get_intersection():
    test_set_1 = set([1,2,3])
    test_set_2 = set([3,4,5])
    test_intersection = [3]

    assert maven_parser.get_intersection(test_set_1,test_set_2) == test_intersection


def test_check_df_empty():
    assert maven_parser.check_df_empty(pd.DataFrame())


def test_check_error_present():

    logs = {'errors':['There is one erroe'],'warning':[]}
    assert maven_parser.check_error_present(logs)
