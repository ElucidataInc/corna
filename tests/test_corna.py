import pytest
import pandas as pd
import corna.corna as corna



single_tracers = ['C13']
double_tracers = ['C13', 'N15']
na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}


def test_na_corr_single_tracer():
	df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	 'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	  'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}, \
	   'Intensity': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995}, \
	    'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'}, \
	    'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'}, \
	     'Sample Name': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})
	eleme_corr = {}
	na_corr_dict = corna.na_correction(df, single_tracers, eleme_corr, na_dict, optimization = False)
	na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
	output_list = [0.59613019390581723, 0.0023185595567866008, 0.40155124653739621]
	assert na_corr_df['NA corrected'].tolist() == output_list

def test_na_corr_single_trac_indist():
	df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	 'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	  'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}, \
	   'Intensity': {0: 0.2274, 1: 0.4361, 2: 0.25405}, \
	    'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'}, \
	    'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'}, \
	     'Sample Name': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})
	eleme_corr = {'C': ['H', 'O']}
	na_corr_dict = corna.na_correction(df, single_tracers, eleme_corr, na_dict, optimization = False)
	na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
	output_list = [0.20455050180955123, 0.49128964787331614, 0.30268558338072632]
	assert na_corr_df['NA corrected'].tolist() == output_list


