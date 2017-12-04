import os

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

# from corna.inputs.multiquant_parser import concat_txts_into_df
from corna.inputs import multiquant_parser
# from olmonk import basic_validation, data_validation

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MQ_FILE_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "raw_mq.txt")
MQ_METADATA_PATH = os.path.join(DIR_PATH, 'test_input_validation_data', "metadata_mq.xlsx")
MQ_SAMPLE_METADATA_PATH = os.path.join \
    (DIR_PATH, 'test_input_validation_data', "metadata_sample.xlsx")

INPUT_FILES = {"mq_file_path": MQ_FILE_PATH, \
                   "mq_metadata_path": MQ_METADATA_PATH, \
                   "mq_sample_metadata_path": MQ_SAMPLE_METADATA_PATH \
                   }
INPUT_FILES_WITHOUT_METADATA = {"mq_file_path": MQ_FILE_PATH,
                                "mq_metadata_path": MQ_METADATA_PATH,
                                "mq_sample_metadata_path": ''}

# TODO : fixtures can be defined for many constants
def test_get_instance():
    """checks if this function returns instance of correct class

    get_instance function takes input_files, validates all files,
    and returns the instances of class having these files as output.
    So, it test if returns instance is correct or not.
    """
    # :TODO: add more extensive testing for this function
    raw_mq, metadata_mq, sample_metadata_mq = multiquant_parser.\
                                                get_basic_validation_instance(INPUT_FILES)

    assert isinstance(raw_mq, basic_validation.BasicValidator)
    assert not isinstance(raw_mq, data_validation.DataValidator)


def test_get_set_from_df_column():
    df = pd.read_table(MQ_FILE_PATH)
    assert type(multiquant_parser.get_set_from_df_column(df, 'Area')) == set
    assert len(multiquant_parser.get_set_from_df_column(df, 'Area')) == 7236


def test_get_validated_df_and_logs():
    # TODO: update test case as per the new params

    raw_mq, metadata_mq, sample_metadata_mq, summary = multiquant_parser.\
                                                get_validated_df_and_logs(INPUT_FILES)

    assert len(raw_mq.logs['warnings']['message']) == 3126
    assert len(metadata_mq.logs['warnings']['message']) == 0
    assert raw_mq.df.shape == (11252, 6)
    assert metadata_mq.df.shape == (75, 5)
    assert sample_metadata_mq.df.shape == (96, 9)
    assert summary == {'SampleData': {'summary': [{'value': u'Original Filename, Metadata, Sampletype, Glucose Conc, Gln/Glc, Activator, Time, Background Sample, Sample Name',
                                                   'label': 'Fields in metadata'},
                                                  {'value': 12, 'label': 'Number of background samples'}],
                                      'title': 'SampleData'},
                       'InputData': {'summary': [{'value': 116, 'label': 'Number of samples'},
                                                 {'value': 11252, 'label': 'Number of rows'},
                                                 {'value': 97, 'label': 'Number of metabolites'},
                                                 {'value': 26, 'label': 'Number of cohorts'}],
                                     'title': 'InputData'},
                       'MetaData': {'summary': [{'value': u'C13', 'label': 'isotopic tracer'},
                                                {'value': 75, 'label': 'Number of fragments'},
                                                {'value': 12, 'label': 'Number of unlabeled fragments'}],
                                    'title': 'MetaData'}}


def test_get_validated_df_logs_without_sample_metadata():
    # TODO: update test case as per the new params

    raw_mq, metadata_mq, sample_metadata_mq, summary = multiquant_parser. \
        get_validated_df_and_logs(INPUT_FILES_WITHOUT_METADATA)

    assert len(raw_mq.logs['warnings']['message']) == 3126
    assert len(metadata_mq.logs['warnings']['message']) == 0
    assert raw_mq.df.shape == (11252, 6)
    assert metadata_mq.df.shape == (75, 5)
    assert sample_metadata_mq == None


def test_filtered_raw_mq_df():
    raw_mq = basic_validation.BasicValidator(MQ_FILE_PATH)
    sample_metadata = basic_validation.BasicValidator(MQ_SAMPLE_METADATA_PATH)
    with pytest.raises(Exception) as e:
        multiquant_parser.get_filtered_raw_mq_df(raw_mq, sample_metadata)
