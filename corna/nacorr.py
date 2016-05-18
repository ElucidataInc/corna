import os
import sys
import warnings

import numpy as np
import pandas as pd


import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import algorithms as algo
import postprocess as postpro
import output as out



warnings.simplefilter(action = "ignore")
# setting relative path
basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))


# Maven

# read files

input_data = hl.read_file(data_dir + '/maven_output.csv')



#print input_data
metadata = hl.read_file(data_dir + '/metadata.csv')
#print metadata
# merge data file and metadata
merged_df = fp.maven_merge_dfs(input_data, metadata)
#print merged_df
# filter df if reqd , given example
filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')

# std model maven
std_model_mvn = fp.standard_model(merged_df, parent = False)



# MultiQuant

# read files
mq_df = hl.concat_txts_into_df(data_dir + '/')
#mq_df = hl.concat_txts_into_df('/Users/sininagpal/OneDrive/Elucidata_Sini/Na_corr_demo/data/')
#print mq_df
mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')


# merge mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)
#print merged_data[(merged_data['Name'].isin(['Citrate 197/71','Citrate 191/67'])) & (merged_data['Sample Name'].isin(['A. [13C-glc] G2.5 0min', 'B. [13C-glc] G2.5 5min']))]
#merged_data.to_csv(data_dir + '/merged_mq.csv')

# standard model mq
std_model_mq = fp.standard_model(merged_data, parent = True)


# integrating isotopomer and parser (input is standardised model in form of nested dictionaries)
fragments_dict = {}
for frag_name, label_dict in std_model_mq.iteritems():
    if frag_name[2] == 'Citrate 191/67':
        new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
        fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True, number=False, mode=None))


#preprocessing for a given metabolite
preprocessed_dict = preproc.bulk_background_correction(fragments_dict, ['A. [13C-glc] G2.5 0min', 'B. [13C-glc] G2.5 5min',

                                                     'C. [13C-glc] G2.5 15min', 'D. [13C-glc] G2.5 30min',
                                                     'E. [13C-glc] G2.5 60min', 'F. [13C-glc] G2.5 120min',
                                                     'G. [13C-glc] G2.5 240min', 'H. [6,6-DD-glc] G2.5 240min'],
                                    'A. [13C-glc] G2.5 0min')

# na correction
na_corrected_dict = algo.na_correction_mimosa_by_fragment(preprocessed_dict)
na_corr_dict_std_model =  iso.fragment_dict_to_std_model(na_corrected_dict,mass=True,number=False)

# post processing - replace negative values by zero
# tested on std_model_mvn and std_model_mq - same data format as output from algorithm.py
#post_processed_dict = postpro.replace_negative_to_zero(na_corr_dict_std_model, replace_negative = True)


frac_enrichment = postpro.enrichment(preprocessed_dict)
frac_enr_dict_std_model =  iso.fragment_dict_to_std_model(frac_enrichment,mass=True,number=False)


dict_to_df = out.convert_dict_df(frac_enr_dict_std_model, parent = True)

