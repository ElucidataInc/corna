import pytest
import numpy as np
import pandas as pd

import corna.file_parser as fp
import corna.inputs.maven_parser as fpa


def test_unq_sample():
	with pytest.raises(KeyError):
		df1 = pd.DataFrame({'Name': [1,2,3], 'abc': [1,2,3], 'Fragment': [1,2,3]})
		unique_samps = fp.get_sample_names(df1)


def test_std_model():
	merged_df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
		'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
		'Label': {0: 'C13_0', 1: 'C13_1', 2: 'C13_2'},
		'Intensity': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995},
		'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'},
		'Sample Name': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})
	df = fpa.frag_key(merged_df)
	std_model = {('Acetic', 'H4C2O2'): {'C13_2': {'sample_1': np.array([ 0.59725])},
					'C13_1': {'sample_1': np.array([ 0.04035])},
					'C13_0': {'sample_1': np.array([ 0.3624])}}}
	std_model_out = fp.standard_model(df)

	assert std_model_out == std_model

