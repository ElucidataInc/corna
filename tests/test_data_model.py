import pytest
import numpy as np
import pandas as pd

import corna.data_model as fp
from corna.inputs.maven_parser import MavenKey, frag_key


def test_std_model():
    merged_df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
	    'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
        'Label': {0: 'C13_0', 1: 'C13_1', 2: 'C13_2'},
		'INTENSITY_COL': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995},
		'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'},
		'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})
    df = frag_key(merged_df)
    std_model = {MavenKey(name='Acetic', formula='H4C2O2'): {'C13_2': {'sample_1': 0.59724999999999995},
															 'C13_1': {'sample_1': 0.040349999999999997}, 'C13_0': {'sample_1': 0.3624}}}
    std_model_out = fp.standard_model(df, intensity_col='INTENSITY_COL')
    assert std_model_out == std_model


def test_to_float():
	np_array = np.array([1, 2])
	assert fp._to_float(np_array) == 1 






