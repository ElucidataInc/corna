import pandas as pd
import pytest

from corna.algorithms.matrix_nacorr import na_correction
from corna.output import convert_to_df
from corna.constants import INTENSITY_COL

single_tracers = ['C13']
multi_tracers = ['C13', 'N15']
na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}


def test_na_corr_single_tracer():
	df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
					   'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'},
					   'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'},
					   'Intensity': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995},
					   'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'},
					   'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'},
					   'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})

	eleme_corr = {}

	na_corr_dict, corr_dct = na_correction(df, ['C13'], '', na_dict, eleme_corr, intensity_col=INTENSITY_COL,
									       autodetect=False)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [0.59613019390581734, 0.0023185595567865968, 0.4015512465373961]

	assert na_corr_df['NA corrected'].tolist() == output_list


def test_na_corr_single_trac_indist():

	df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	 'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	  'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}, \
	   'Intensity': {0: 0.2274, 1: 0.4361, 2: 0.25405}, \
	    'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'}, \
	    'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'}, \
	     'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})

	eleme_corr = {'C': ['H', 'O']}

	na_corr_dict, corr_dict = na_correction(df, ['C13'], '', na_dict, eleme_corr, intensity_col=INTENSITY_COL,
											autodetect=False)

	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [0.1961957568543734, 0.48572975053068485, 0.3035536244690365]

	assert na_corr_df['NA corrected'].tolist() == output_list

def test_na_corr_multi_trac():
	df = pd.DataFrame({'Name': {0: 'L-Methionine', 1: 'L-Methionine'},
					   'Label': {0: 'C12 PARENT', 1: 'C13-label-1'},
					   'Intensity': {0: 0.203405, 1: 0.050069999999999996},
					   'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S'},
					   'Sample': {0: 'sample_1', 1: 'sample_1'}})
	eleme_corr = {}
	na_corr_dict, corr_dict = na_correction(df, ['C13', 'N15'], '',
											na_dict, eleme_corr,
											intensity_col=INTENSITY_COL, autodetect=False)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [-0.0053063306434838163, 0.32858944654474742]
	assert na_corr_df['NA corrected'].tolist() == output_list


def test_na_corr_multi_trac_indist():
	df = pd.DataFrame({'Name': {0: 'L-Methionine', 1: 'L-Methionine'},
					   'Label': {0: 'C12 PARENT', 1: 'C13-label-1'},
					   'Intensity': {0: 0.203405, 1: 0.050069999999999996},
					   'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S'},
					   'Sample': {0: 'sample_1', 1: 'sample_1'}})
	eleme_corr = {'C': ['H']}
	na_corr_dict, corr_dict =  na_correction(df, ['C13', 'N15'],'',
														   na_dict, eleme_corr,
														   intensity_col=INTENSITY_COL,autodetect=False)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')
	output_list = [-0.045478760757226011, 0.40215440095785504]
	assert na_corr_df['NA corrected'].tolist() == output_list

def test_ppm_nacorrection():
	df = pd.DataFrame({'Name': {0: 'L-Methionine', 1: 'L-Methionine'},
					   'Label': {0: 'C12 PARENT', 1: 'C13-label-1'},
					   'Intensity': {0: 0.203405, 1: 0.050069999999999996},
					   'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S'},
					   'Sample': {0: 'sample_1', 1: 'sample_1'}})
	eleme_corr = {}
	na_corr_dict, corr_dict = na_correction(df, ['C13', 'N15'], 40, na_dict, eleme_corr, intensity_col=INTENSITY_COL,
											autodetect=True)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')
	output_list = [-0.0053063306434838163, 0.32858944654474742]
	assert list(na_corr_df['NA corrected']) == output_list
	assert corr_dict == {'L-Methionine': {'C': [], 'N': ['O17', 'O18']}}





