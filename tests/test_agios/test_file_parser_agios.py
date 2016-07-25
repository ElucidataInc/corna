import pytest
import pandas as pd
import corna.corna_agios.file_parser_agios as fp




def test_mvn_merge_dfs():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], 'Formula': [1,2,3], 'sample': [1,2,3]})
		df2 = pd.DataFrame({'Name': [1,2,3], 'Info': [1,2,3], 'sample': [5,6,7]})
		longform = fp.maven_merge_dfs(df1, df2)

# def test_frag_keys():
# 	with pytest.raises(KeyError):
# 		df1 = pd.DataFrame({'Name': [1,2,3], 'Formula': [1,2,3]})
# 		fragkey_col = fp.frag_key(df1)