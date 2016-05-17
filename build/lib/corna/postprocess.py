import pandas as pd


def zero_if_negative(num):
	"""
	This function replaces negative numbers by zero_if_negative

	Args:
		num : any int value

	Return:
		1. zero if num is negative
		2. number itself if num is non negative
	"""
	if num < 0:
		return 0
	return num


def replace_negative_to_zero(corrected_dict, replace_negative = True):
	"""
	This function replaces negative intensity values by zero from list of intensity
	in the standardised model dictionary

	Args:
		corrected_dict : nested dictionary (std model) with NA corrected intensity values
		replace_negative :
						  1. if True, replaces negative values and updates the dictionary
						  2. if False, return the nested dictionary with corrected values
						     as it is
	Returns:
		post_proc_dict : returns nested dictionary with negative values replaced

	"""

	if replace_negative == True:

		post_proc_dict = {}

		for frag_name, label_dict in corrected_dict.iteritems():
			for label, samp_dict in label_dict.iteritems():
				for sample, intensity_list in samp_dict.iteritems():
					intensity_list = map(zero_if_negative, intensity_list)
					samp_dict[sample] = intensity_list
				label_dict[label] = samp_dict
			post_proc_dict[frag_name] = label_dict

		return post_proc_dict

	elif replace_negative == False:

		return corrected_dict


def convert_dict_df(nest_dict):
	frames = []
	labels = []
	name = []
	for frag_name, label_dict in nest_dict.iteritems():
		name.append(frag_name)
		frames.append(pd.DataFrame.from_dict(label_dict, orient='index'))

		#for label, samp_dict in label_dict.iteritems():
			#labels.append(label)
			#frames.append(pd.DataFrame.from_dict(samp_dict, orient='index'))

	#print frames
	dict_to_df = pd.concat(frames, keys=name).reset_index()
	#print dict_to_df.sum()
	all_cols = dict_to_df.columns.tolist()
	level_cols = ['level_0', 'level_1', 'level_2']
	sample_cols = []
	for cols in all_cols:
		if not cols in level_cols:
			sample_cols.append(cols)

	#df_sum = dict_to_df.groupby('level_1')[sample_cols].apply(lambda x :
	#print dict_to_df
	#print df_sum





