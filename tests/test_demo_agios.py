import pytest
import corna.corna as corna
import Demo.demo_agios as demo




single_tracers = ['C13']
na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}


def test_na_corr_single_tracer():
	df = {'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'},\
	 'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	 'sample_1': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995}, \
	 'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}}
	eleme_corr = {}
	na_corr_dict = corna.na_correction(df, single_tracers, eleme_corr, na_dict, optimization = False)
	na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
	assert na_corr_df['NA corrected'] == [0.596130, 0.002319, 0.401551]
#def test_na_corr_single_trac_indist():


#def test_na_corr_double_tracer():
#def test_na_corr_double_trac_indist()

