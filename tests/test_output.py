import pytest
import pandas as pd
import numpy as np
import numpy.testing as npt
import corna.config as conf
import corna.output as out
from corna.isotopomer import Infopacket


fragment_dict = {('Acetic', 'H4C2O2'): {'C13_2': {'sample_1': np.array([ 0])},
'C13_1': {'sample_1': np.array([ 1])}}}


fragment_dict = {'Acetic_C13_1': Infopacket(frag='H4C2O2', data={'sample_1': np.array([1])}, unlabeled=False, name='Acetic'), 'Acetic_C13_2': Infopacket(frag='H4C2O2', data={'sample_1': np.array([0])}, unlabeled=False, name='Acetic')}

df = pd.DataFrame({'Sample Name': {0: 'sample_1', 1: 'sample_1'}, \
					'Label': {0: 'C13_2', 1: 'C13_1'}, \
					'Intensity': {0: 0, 1: 1}, \
					'Name': {0: 'Acetic', 1: 'Acetic'}, \
					'Formula': {0: 'H4C2O2', 1: 'H4C2O2'}})


def test_convert_to_df():
	out_df =  out.convert_dict_df(fragment_dict)
	out_df = out_df[['Formula', 'Intensity', 'Label', 'Name', 'Sample Name']]
	npt.assert_array_equal(out_df, df)
