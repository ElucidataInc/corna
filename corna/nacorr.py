import file_parser as fp
import helpers as hl
import os
import sys


# setting relative path
basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))


# Maven

# read files
input_data = hl.read_file(data_dir + '/maven_output.csv')
metadata = hl.read_file(data_dir + '/metadata.csv')

# merge data file and metadata
merged_df = fp.maven_merge_dfs(input_data, metadata)

# std model maven
std_model = fp.standard_model(merged_df, parent = 'False')

# filter df
filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')


# MultiQuant

# read files
mq_df = hl.concat_txts_into_df(data_dir)
mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')

# merge mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)

# standard model mq
std_model_mq = fp.standard_model(merged_data, parent = 'true')



