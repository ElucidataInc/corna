import os

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

from corna.inputs.multiquant_parser import concat_txts_into_df


dir_path = os.path.dirname(os.path.realpath(__file__))


def test_concat_txts_into_df_single():
    mq_dir = os.path.join(dir_path,"test_mq_one_file")
    known_df = pd.read_excel(os.path.join(dir_path,"txt_to_df_test_one_df.xls"))
    test_df = concat_txts_into_df(mq_dir)
    assert_frame_equal(known_df.sort_index(axis=1), test_df.sort_index(axis=1), check_names=True)

def test_concat_txts_into_df_multiple():
    mq_dir = os.path.join(dir_path, "test_mq_two_files")
    known_df = pd.read_excel(os.path.join(dir_path, "txt_to_df_test_two_df.xlsx"))
    test_df = concat_txts_into_df(mq_dir)
    assert_frame_equal(known_df.sort_index(axis=1), test_df.sort_index(axis=1), check_names=True)

def test_concat_txts_into_df_req_col():
    mq_dir = os.path.join(dir_path,"test_mq_req_cols_exception")
    with pytest.raises(AssertionError):
         concat_txts_into_df(mq_dir)
