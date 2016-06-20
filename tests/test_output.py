import pytest
import pandas as pd
import numpy as np
import corna.config as conf
import corna.output as out


fragment_dict = {('Acetic', 'H4C2O2'): {'C13_2': {'sample_1': np.array([ 0])},
'C13_1': {'sample_1': np.array([ 1])}}}


df = pd.DataFrame({'Formula': {0: 'H4C2O2', 1: 'H4C2O2'}, 'Intensity': {0: 0, 1: 1}, \
	'Sample Name': {0: 'sample_1', 1: 'sample_1'}, \
	'Name': {0: 'Acetic', 1: 'Acetic'}, 'Label': {0: 'C13_2', 1: 'C13_1'}})


def test_convert_to_df():
	assert out.convert_dict_df(fragment_dict, parent = False) == df


