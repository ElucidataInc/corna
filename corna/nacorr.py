import file_parser as fp
import helpers as hl
import os
import sys


# maven
# add relative path
path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
input_data = hl.read_file(path_input)
metadata = hl.read_file(path_metadata)
merged_df = maven_merge_dfs(input_data, metadata)
filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')
met_name = mvn_met_names(filter_df, col_name = 'Name')
met_formula = mvn_met_formula(filter_df, col_name = 'Formula')



#mq
mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_df = hl.concat_txts_into_df(mq_dir)
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = read_input_data(mq_met_path)
merged_df.to_csv(mq_dir + 'mvn.csv')
mq_df.to_csv(mq_dir + 'mq.csv')

#basepath = os.path.dirname(__file__)
#dir_path = os.path.dirname(os.path.realpath(__file__))
#mq_dir = os.path.abspath(os.path.join(basepath, "..", "data", "mq"))


# mq
#read mq files
mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_df = fp.concat_mq_txts(mq_dir)

# read metadata files
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = hl.read_file(mq_met_path)

#combine data

#filter data
#filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')

