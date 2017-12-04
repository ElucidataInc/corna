import os

import pandas as pd
import pytest

from corna.inputs import validation
from olmonk import data_validation

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MQ_FILE_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "raw_mq.txt")
MQ_METADATA_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "metadata_mq.xlsx")
MQ_SAMPLE_METADATA_PATH = os.path.join \
    (DIR_PATH, 'test_input_validation_data', "metadata_sample.xlsx")


def test_get_class_inst():
    validation_class = basic_validation.BasicValidator
    required_column = None

    class_inst = validation.get_class_inst(validation_class, MQ_FILE_PATH, required_column)

    assert isinstance(class_inst, basic_validation.BasicValidator)
    assert not isinstance(class_inst, data_validation.DataValidator)


def test_data_validation_raw_df():
    df = pd.read_table(MQ_FILE_PATH)
    validation_class_inst_raw_mq = validation.data_validation_raw_df(df)

    assert isinstance(validation_class_inst_raw_mq, data_validation.DataValidator)
    assert len(validation_class_inst_raw_mq.logs['warnings']['message']) == 3126


def test_data_validation_raw_df_exception():
    df = 'some string'

    with pytest.raises(Exception) as e_info:
        validation.data_validation_raw_df(df)


def test_data_validation_metadata_df():
    df = pd.read_excel(MQ_METADATA_PATH)
    validation_class_inst_metadata_mq = validation.data_validation_metadata_df(df)

    assert isinstance(validation_class_inst_metadata_mq, data_validation.DataValidator)
    assert len(validation_class_inst_metadata_mq.logs['warnings']['message']) == 0


def test_data_validation_metadata_df_exception():
    df = 'some string'

    with pytest.raises(Exception) as e_info:
        validation.data_validation_metadata_df(df)


def test_basic_validation_result():
    # TODO: This case will fail
    basic_valid_class = basic_validation.BasicValidator('some_invalid_path')
    with pytest.raises(Exception) as e_info:
        validation.basic_validation_result(basic_valid_class)
