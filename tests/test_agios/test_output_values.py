import pandas as pd
import pytest

from corna.algorithms.matrix_nacorr import na_correction
from corna.output import convert_to_df

single_tracers = ['C13']
multi_tracers = ['C13', 'N15']
na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}


def test_na_corr_single_tracer():

	df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	 'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
	  'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}, \
	   'Intensity': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995}, \
	    'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'}, \
	    'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'}, \
	     'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})

	eleme_corr = {}

	na_corr_dict = na_correction(df, single_tracers, eleme_corr, na_dict)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [0.59613019390581723, 0.0023185595567866008, 0.40155124653739621]

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

	na_corr_dict = na_correction(df, single_tracers, eleme_corr, na_dict)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [0.2783720710600131, 0.52118757080316813, 0.3026855833807266]

	assert na_corr_df['NA corrected'].tolist() == output_list

def test_na_corr_multi_trac():

	df = pd.DataFrame({'Name': {0: 'L-Methionine', 1: 'L-Methionine', 2: 'L-Methionine', 3: 'L-Methionine',
		4: 'L-Methionine', 5: 'L-Methionine', 6: 'L-Methionine', 7: 'L-Methionine',
		8: 'L-Methionine', 9: 'L-Methionine', 10: 'L-Methionine', 11: 'L-Methionine'},
		'Parent': {0: 'L-Methionine', 1: 'L-Methionine', 2: 'L-Methionine', 3: 'L-Methionine',
		4: 'L-Methionine', 5: 'L-Methionine', 6: 'L-Methionine', 7: 'L-Methionine', 8: 'L-Methionine',
		9: 'L-Methionine', 10: 'L-Methionine', 11: 'L-Methionine'}, 'Label': {0: 'C12 PARENT',
		1: 'C13-label-1', 2: 'C13-label-2', 3: 'C13-label-3', 4: 'C13-label-4', 5: 'C13-label-5',
		6: 'N15-label-1', 7: 'C13N15-label-1-1', 8: 'C13N15-label-2-1', 9: 'C13N15-label-3-1',
		10: 'C13N15-label-4-1', 11: 'C13N15-label-5-1'},
		'Intensity': {0: 0.24560000000000001, 1: 0.066650000000000001, 2: 0.0071000000000000004,
		3: 0.00029999999999999997, 4: 0.0, 5: 0.0, 6: 0.061899999999999997, 7: 0.016400000000000001,
		8: 0.0015, 9: 0.0001, 10: 0.0, 11: 0.60045000000000004},
		'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S',
		2: 'C5H10NO2S', 3: 'C5H10NO2S', 4: 'C5H10NO2S', 5: 'C5H10NO2S', 6: 'C5H10NO2S',
		7: 'C5H10NO2S', 8: 'C5H10NO2S', 9: 'C5H10NO2S', 10: 'C5H10NO2S', 11: 'C5H10NO2S'},
		'Sample': {0: 'sample_1', 1: 'sample_1',
		2: 'sample_1', 3: 'sample_1', 4: 'sample_1', 5: 'sample_1', 6: 'sample_1',
		7: 'sample_1', 8: 'sample_1', 9: 'sample_1', 10: 'sample_1', 11: 'sample_1'}})

	eleme_corr = {}

	na_corr_dict = na_correction(df, multi_tracers, eleme_corr, na_dict)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [0.00064617771744998609, 0.3967531185142435, -9.8844997716120012e-05,
	7.0170861504082293e-05, -0.00024013579424740682, -0.00018698767698716368,
	0.0030976144330255844, -0.00048382556594077245, -2.6604348209106283e-06,
	-4.9943479640610513e-06, 2.6016225533332996e-07, 0.60045010712919833]

	assert na_corr_df['NA corrected'].tolist() == output_list


def test_na_corr_multi_trac_indist():

	df = pd.DataFrame({'Name': {0: 'L-Methionine', 1: 'L-Methionine', 2: 'L-Methionine', 3: 'L-Methionine',
		4: 'L-Methionine', 5: 'L-Methionine', 6: 'L-Methionine', 7: 'L-Methionine', 8: 'L-Methionine',
		9: 'L-Methionine', 10: 'L-Methionine', 11: 'L-Methionine'}, 'Parent': {0: 'L-Methionine',
		1: 'L-Methionine', 2: 'L-Methionine', 3: 'L-Methionine', 4: 'L-Methionine', 5: 'L-Methionine',
		6: 'L-Methionine', 7: 'L-Methionine', 8: 'L-Methionine', 9: 'L-Methionine', 10: 'L-Methionine',
		11: 'L-Methionine'}, 'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2',
		3: 'C13-label-3', 4: 'C13-label-4', 5: 'C13-label-5', 6: 'N15-label-1', 7: 'C13N15-label-1-1',
		8: 'C13N15-label-2-1', 9: 'C13N15-label-3-1', 10: 'C13N15-label-4-1', 11: 'C13N15-label-5-1'},
		'Intensity': {0: 0.203405, 1: 0.050069999999999996, 2: 0.093910000000000007, 3: 0.02402,
		4: 0.02051, 5: 0.0051600000000000005, 6: 0.0028300000000000001, 7: 0.00065499999999999998,
		8: 0.00022499999999999999, 9: 8.4999999999999993e-05, 10: 5.0000000000000004e-06,
		11: 0.48973500000000003},
		'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S', 2: 'C5H10NO2S', 3: 'C5H10NO2S', 4: 'C5H10NO2S',
		5: 'C5H10NO2S', 6: 'C5H10NO2S', 7: 'C5H10NO2S', 8: 'C5H10NO2S', 9: 'C5H10NO2S', 10: 'C5H10NO2S',
		11: 'C5H10NO2S'}, 'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1',
		 3: 'sample_1', 4: 'sample_1', 5: 'sample_1', 6: 'sample_1', 7: 'sample_1', 8: 'sample_1',
		 9: 'sample_1', 10: 'sample_1', 11: 'sample_1'}})

	eleme_corr = {'C': ['H']}

	na_corr_dict = na_correction(df, multi_tracers, eleme_corr, na_dict)
	na_corr_df = convert_to_df(na_corr_dict, False, colname='NA corrected')

	output_list = [-0.075954704287110375, 0.40215442709008198, 0.016489750088414929, -0.0032216908381774477,
	-0.031526293342053771, 0.15881269215932281, -0.0064943180078375707,
	0.0011640245763342482, 0.030179296768192233, -0.0060388880912154832,
	 0.0063239074820523374, 0.59811258028877923]

	assert na_corr_df['NA corrected'].tolist() == output_list



