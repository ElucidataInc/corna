import pytest
import numpy as np
import corna.postprocess as pp
import corna.config as conf


corrected_dict = {'Acetic_C13_0': ['H4C2O2', {'sample_1': np.array([ -0.63865507])}, True, 'Acetic'], \
'Acetic_C13_1': ['H4C2O2', {'sample_1': np.array([ 0.63865507])}, False, 'Acetic']}

replaced_neg =  {'Acetic_C13_0': ['H4C2O2', {'sample_1': np.array([ 0])}, True, 'Acetic'], \
'Acetic_C13_1': ['H4C2O2', {'sample_1': np.array([ 0.63865507])}, False, 'Acetic']}


def test_replace_negatives():
	assert pp.replace_negative_to_zero(corrected_dict, replace_negative = True) == replaced_neg

def test_frac_enrch():
	with pytest.raises(ValueError):
		frac_enr = pp.enrichment(corrected_dict, decimals = 4)









