import pytest
import corna.corna as corna



single_tracers = ['C13']
na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}


def test_na_corr_single_tracer():

	eleme_corr = {}
	na_corr_dict = corna.na_correction(df, single_tracers, eleme_corr, na_dict, optimization = False)
	na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
	assert na_corr_df['NA corrected'] == [0.596130, 0.002319, 0.401551]