import pytest
import pandas as pd
import corna.file_parser as fp
import corna.config as conf



def test_mvn_merge_dfs():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], 'Formula': [1,2,3], 'sample': [1,2,3]})
		df2 = pd.DataFrame({'Name': [1,2,3], 'Info': [1,2,3], 'sample': [5,6,7]})
		longform = fp.maven_merge_dfs(df1, df2)


def test_mq_merge_dfs():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], 'abc': [1,2,3], 'Fragment': [1,2,3]})
		df2 = pd.DataFrame({'Name': [1,2,3], 'xyz': [1,2,3], 'Fragment': [5,6,7]})
		longform = fp.mq_merge_dfs(df1, df2)

def test_unq_sample():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], 'abc': [1,2,3], 'Fragment': [1,2,3]})
		unique_samps = fp.get_sample_names(df1)


def test_mq_stds():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], conf.SAMPLE_COL: [1,2,3]})
		rmv_std_df = fp.remove_mq_stds(df1)


def test_frag_keys():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], conf.FORMULA: [1,2,3]})
		fragkey_col = fp.frag_key(df, parent = True)



