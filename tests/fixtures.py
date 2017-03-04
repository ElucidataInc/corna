import os
import pandas as pd
import pytest

from tests import constants


@pytest.fixture()
def read_csv(path):
    return pd.read_csv(path)


@pytest.fixture()
def get_maven_df():
    return read_csv(constants.maven_file)


@pytest.fixture()
def get_metadata_df():
    return read_csv(constants.metadata_file)


@pytest.fixture()
def get_mergedf_all_correct():
    return read_csv(constants.test_df_path_all_correct)


@pytest.fixture()
def get_mergedf_no_metadata():
    return read_csv(constants.test_df_path_no_metadata)


@pytest.fixture()
def get_mergedf_warning():
    return read_csv(constants.test_df_path_warning)


@pytest.fixture()
def get_maven_file_intensity_incorrect():
    return read_csv(constants.maven_file_intensity_incorrect)


@pytest.fixture()
def get_maven_file_empty_intersection():
    return read_csv(constants.maven_file_path_empty_intersection)


@pytest.fixture()
def get_maven_file_extra_sample():
    return read_csv(constants.maven_file_path_extra_sample)


