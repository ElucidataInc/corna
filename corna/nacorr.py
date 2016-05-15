import file_parser as fp
import helpers as hl
import os
import sys



# add relative path

#basepath = os.path.dirname(__file__)
#dir_path = os.path.dirname(os.path.realpath(__file__))
#mq_dir = os.path.abspath(os.path.join(basepath, "..", "data", "mq"))

# maven
path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
input_data = hl.read_file(path_input)
metadata = hl.read_file(path_metadata)
merged_df = fp.maven_merge_dfs(input_data, metadata)

std_model = fp.standard_model(merged_df)
print std_model

filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')
met_name = fp.mvn_met_names(filter_df, col_name = 'Name')
met_formula = fp.mvn_met_formula(filter_df, col_name = 'Formula')




#mq

# read concatenated mq_dfs
mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_df = hl.concat_txts_into_df(mq_dir)

# read mq metadata
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = hl.read_file(mq_met_path)

# combine mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)
std_model_mq = fp.standard_model(merged_data)
print std_model_mq
merged_data.to_csv(mq_dir + 'mq_met.csv')
merged_df.to_csv(mq_dir + 'mvn_met.csv')

#for index, row in merged_df.iterrows():




#combine data

#filter data
#filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')

