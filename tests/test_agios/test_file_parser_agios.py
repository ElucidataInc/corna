import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal

import corna.inputs.maven_parser as fp

label_df = pd.DataFrame({'Name': [1,2,3,4,5], 'Formula': [1,2,3,4,5], 'sample': [1,2,3,4,5],
						 'Label': ['C13_0_N15_0', 'C13_1_N15_0', 'C13_0_N15_1', 'C13_2_N15_1', 'N15_1_C13_2']})

label_df_maven_format = pd.DataFrame({'Name': [1,2,3,4,5], 'Formula': [1,2,3,4,5], 'sample': [1,2,3,4,5],
						 'Label': ['C12 PARENT', 'C13-label-1', 'N15-label-1', 'C13N15-label-2-1', 'N15C13-label-1-2']})

def test_std_label_to_maven_label():
	assert_frame_equal(fp.convert_std_label_key_to_maven_label(label_df),label_df_maven_format)

# def test_mvn_merge_dfs():
# 	with pytest.raises(KeyError):
# 		df1 = pd.DataFrame({'Name': [1,2,3], 'Formula': [1,2,3], 'sample': [1,2,3]})
# 		df2 = pd.DataFrame({'Name': [1,2,3], 'Info': [1,2,3], 'sample': [5,6,7]})
# 		longform = fp.maven_merge_dfs(df1, df2)

# def test_frag_keys():
# 	with pytest.raises(KeyError):
# 		df1 = pd.DataFrame({'Name': [1,2,3], 'Formula': [1,2,3]})
# 		fragkey_col = fp.frag_key(df1)