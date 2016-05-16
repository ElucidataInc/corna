import os
import sys

import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import postprocess as postpro

import pandas as pd


# setting relative path
basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))


# Maven

# read files
input_data = hl.read_file(data_dir + '/maven_output.csv')
metadata = hl.read_file(data_dir + '/metadata.csv')

# merge data file and metadata
merged_df = fp.maven_merge_dfs(input_data, metadata)

# filter df if reqd , given example
filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')

# std model maven
std_model_mvn = fp.standard_model(merged_df, parent = False)



# MultiQuant

# read files
mq_df = hl.concat_txts_into_df(data_dir + '/')
mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')

# merge mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)
merged_data.to_csv(data_dir + '/merged_mq.csv')

# standard model mq
std_model_mq = fp.standard_model(merged_data, parent = True)

# integrating isotopomer and parser (input is standardised model in form of nested dictionaries)
fragments_dict = {}
for frag_name, label_dict in std_model_mq.iteritems():
	 fragments_dict.update(iso.bulk_insert_data_to_fragment(frag_name, label_dict, mass=True, number=False, mode=None))

# preprocessing : correction for background noise
preprocess_data = preproc.background('A. [13C-glc] G2.5 0min', fragments_dict[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')],\
 fragments_dict[('Glutamate 146/41_146.0', 'Glutamate 146/41_41.0')])


# na correction
#code from algorithm.py

# post processing - replace negative values by zero
# tested on std_model_mvn and std_model_mq - same data format as output from algorithm.py
post_processed_dict = postpro.replace_negative_to_zero(std_model_mvn, replace_negative = True)


# output: convert nested dictionary to pandas data frame and add columns from merged df

output_df = pd.DataFrame()

#output_df['Name'] = std_model_mvn.ke

name = []
formula = []
lab = []
samp = []

#for frag_name, label_dict in std_model_mvn.iteritems():
	#name.append(frag_name[0])
	#formula.append(frag_name[1])
	#for label, samp_dict in label_dict.iteritems():
		#lab.append(label)
		#df_t = pd.DataFrame(samp_dict).transpose()
		#df_t['label'] =label
		#for sample, intensity_list in samp_dict.iteritems():

#print df_t
#print pd.DataFrame(std_model_mvn)
frames = []
labels = []
for frag_name, label_dict in std_model_mvn.iteritems():
	name.append(frag_name)
	frames.append(pd.DataFrame.from_dict(label_dict, orient='index'))
	#for label, samp_dict in label_dict.iteritems():
		#labels.append(label)
		#frames.append(pd.DataFrame.from_dict(samp_dict, orient='index'))

#print frames
print pd.concat(frames, keys=name).reset_index()











