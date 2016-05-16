


def zero_if_negative(num):
	if num == 0:
		return 88
	return num


def replace_negative_to_zero(corrected_dict, replace_negative = True):

	post_proc_dict = {}

	for frag_name, label_dict in corrected_dict.iteritems():
		for label, samp_dict in label_dict.iteritems():
			for sample, intensity_list in samp_dict.iteritems():
				intensity_list = map(zero_if_negative, intensity_list)
				samp_dict[sample] = intensity_list
			label_dict[label] = samp_dict
		post_proc_dict[frag_name] = label_dict

	return post_proc_dict




