#to convert nested dict back to pandas dataframe in standardised format

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


	df_sum = dict_to_df.groupby('level_2')[sample_cols].sum()
	#print df_sum
	#print dict_to_df
	#print df_sum

	#TOBECOMPLETED