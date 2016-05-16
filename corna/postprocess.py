


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




