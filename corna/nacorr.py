import file_parser as fp
import os
import sys

# maven
# path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
# path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
# input_data = read_input_data(path_input)
# metadata = read_metadata(path_metadata)
# merged_df = maven_merge_dfs(input_data, metadata)
# filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')

basepath = os.path.dirname(__file__)
dir_path = os.path.dirname(os.path.realpath(__file__))
mq_dir = os.path.abspath(os.path.join(basepath, "..", "data/mq", "/"))

#mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_txt_files = fp.get_mq_txts(mq_dir)
mq_df = fp.concat_mq_txts(mq_dir, mq_txt_files)
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = fp.read_input_data(mq_met_path)
mq_df.to_csv(mq_dir + 'mq.csv')
