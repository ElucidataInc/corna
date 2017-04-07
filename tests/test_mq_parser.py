import os

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

# from corna.inputs.multiquant_parser import concat_txts_into_df
from corna.inputs import multiquant_parser
from olmonk import basic_validation, data_validation

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MQ_FILE_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "raw_mq.txt")
MQ_METADATA_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "metadata_mq.xlsx")
MQ_SAMPLE_METADATA_PATH = os.path.join \
    (DIR_PATH, 'test_input_validation_data', "metadata_sample.xlsx")


def test_get_instance():
    """checks if this function returns instance of correct class

    get_instance function takes input_files, validates all files,
    and returns the instances of class having these files as output.
    So, it test if returns instance is correct or not.
    """
    # :TODO: add more extensive testing for this function
    input_files = {"mq_file_path": MQ_FILE_PATH, \
                   "mq_metadata_path": MQ_METADATA_PATH, \
                   "mq_sample_metadata_path": MQ_SAMPLE_METADATA_PATH \
                   }

    raw_mq, metadata_mq, sample_metadata_mq = multiquant_parser.get_instance(input_files)

    assert isinstance(raw_mq, basic_validation.BasicValidator)
    assert not isinstance(raw_mq, data_validation.DataValidator)


def test_get_set_from_df_column():
    df = pd.read_table(MQ_FILE_PATH)
    print type(multiquant_parser.get_set_from_df_column(df, 'Area'))
    print len(multiquant_parser.get_set_from_df_column(df, 'Area'))