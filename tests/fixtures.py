import os
import pandas as pd
import pytest

from tests import constants


@pytest.fixture()
def read_csv(path):
    return pd.read_csv(path)


@pytest.fixture()
def get_maven_df():
    return read_csv(constants.MAVEN_FILE)


@pytest.fixture()
def get_metadata_df():
    return read_csv(constants.METADATA_FILE)


@pytest.fixture()
def get_mergedf_all_correct():
    return read_csv(constants.TEST_DF_PATH_ALL_CORRECT)


@pytest.fixture()
def get_mergedf_no_metadata():
    return read_csv(constants.TEST_DF_PATH_NO_METADATA)


@pytest.fixture()
def get_mergedf_warning():
    return read_csv(constants.TEST_DF_PATH_WARNING)


@pytest.fixture()
def get_maven_file_intensity_incorrect():
    return read_csv(constants.MAVEN_FILE_INTENSITY_INCORRECT)


@pytest.fixture()
def get_maven_file_empty_intersection():
    return read_csv(constants.MAVEN_FILE_PATH_EMPTY_INTERSECTION)


@pytest.fixture()
def get_maven_file_extra_sample():
    return read_csv(constants.MAVEN_FILE_PATH_EXTRA_SAMPLE)


