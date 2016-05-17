import os
import sys

import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import algorithms as algo
import postprocess as postpro




# setting relative path
#basepath = os.path.dirname(__file__)
#data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))


# Maven

# read files
#input_data = hl.read_file(data_dir + '/maven_output.csv')



#print input_data
# metadata = hl.read_file(data_dir + '/metadata.csv')
# #print metadata
# # merge data file and metadata
# merged_df = fp.maven_merge_dfs(input_data, metadata)
# #print merged_df
# # filter df if reqd , given example
# filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')

# # std model maven
# std_model_mvn = fp.standard_model(merged_df, parent = False)



# # MultiQuant

# # read files
def read_multiquant(dir_path):
	#mq_df = hl.concat_txts_into_df(data_dir + '/')
	mq_df = hl.concat_txts_into_df(dir_path)
	return mq_df

def read_multiquant_metadata(path):
	#mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')
	mq_metdata = hl.read_file(path)

	return mq_metdata


def merge_mq_metadata(mq_df, metdata):
	merged_data = fp.mq_merge_dfs(mq_df, metdata)
	return merged_data


def filter_df(merged_data, colname, colvalue):
	filtered_df = hl.filter_df(merged_data, colname, colvalue)
	return filtered_df


# # standard model mq
def std_data_model(dataframe):
	std_model_mq = fp.standard_model(dataframe, parent = True)
	return std_model_mq


def met_background_correction(metabolite, merged_data, background_sample, list_of_samples):
    std_model_mq = fp.standard_model(merged_data, parent = True)
    fragments_dict = {}
    for frag_name, label_dict in std_model_mq.iteritems():
        if frag_name[2] == metabolite:
        	new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
        	fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True, number=False, mode=None))
    preprocessed_dict = preproc.bulk_background_correction(fragments_dict, list_of_samples, background_sample)
    return preprocessed_dict


def na_correction_mimosa(preprocessed_output):
    na_corrected_out = algo.na_correction_mimosa_by_fragment(preprocessed_output)
    return na_corrected_out

# # na correction
# na_corrected_dict = algo.na_correction_mimosa_by_fragment(preprocessed_dict)
# print na_corrected_dict
# #print na_corrected_dict[(193.0, 68.0)][1]['F. [13C-glc] G2.5 120min']

# # post processing - replace negative values by zero
# # tested on std_model_mvn and std_model_mq - same data format as output from algorithm.py

# post_processed_dict = postpro.replace_negative_to_zero(std_model_mvn, replace_negative = True)


# # calculate mean_enrichment
# mean_enrich_df = postpro.convert_dict_df(std_model_mvn)


# # output data frame with added metadat columns












