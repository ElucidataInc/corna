import os

import pandas as pd

import corna

basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath) + "/test_data")


# path to directory where multiquant text data files are present
path_dir = data_dir

# read multiquant data files and combine them
mq_files = corna.read_multiquant(path_dir + '/')

# read multiquant metadata file
mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

# merge multiquant files and metadata files
merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)


# filter merged data as per requirement
malate = corna.filtering_df(merge_mq_metdata, num_col=1, col1="Parent",
                                list_col1_vals=['Malate 133/115'])

glutamate = corna.filtering_df(merge_mq_metdata, num_col=1, col1="Parent",
                                list_col1_vals=['Glutamate 146/128'])

background_corr_malate = corna.met_background_correction('Malate 133/115', malate, 'A. [13C-glc] G9 0min')
postprocessed_out_malate = corna.replace_negatives(background_corr_malate, all=False)
background_corr_df_malate = corna.convert_to_df(postprocessed_out_malate, all = False, colname = 'Background correction')

#output file
background_corr_out = pd.read_excel(path_dir + '/test_demo_output.xlsx', 'BackgroundCorrection')
background_corr_out_malate = corna.filtering_df(background_corr_out, num_col=1, col1='name',
                                                list_col1_vals=['Malate 133/115'])

print background_corr_df_malate.equals(background_corr_out_malate)

corna.save_to_csv(background_corr_df_malate, '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/our_out.csv')
corna.save_to_csv(background_corr_out_malate, '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/excel_out.csv')
# background noise correction on filtered data
# background_corr = corna.met_background_correction_all(filtered_data, 'Q. [13C-glc] G7 0min')
#
# # background noise correction for all labels of a fragmnent
# background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min')
#
# # background noise correction by list of given samples
# list_of_samples = ['Q. [13C-glc] G7 0min', 'R. [13C-glc] G7 5min', 'S. [13C-glc] G7 15min']
# background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min', list_of_samples, all_samples=False)
#
# # convert background noise corrected dictionary to dataframe
# background_corr_df = corna.convert_to_df(background_corr, all = True, colname = 'Background correction')
#
#
# # NA correction method on background noise corrected data
# nacorr_dict = corna.na_correction_mimosa(background_corr, all = True)
# na_corr_df = corna.convert_to_df(nacorr_dict, all=True, colname = 'NA corrected')
#
# # Replace negative values by zero on NA corrected data - optional
# postprocessed_out = corna.replace_negatives(nacorr_dict, all=True)
# postprocessed_out_df = corna.convert_to_df(postprocessed_out, all = True, colname =  'Replaced negatives')
#
# # calculate fractional enrichment on post processed data
# frac_enrichment = corna.fractional_enrichment(postprocessed_out, all=True)
# frac_enr_df = corna.convert_to_df(frac_enrichment, all = True, colname = 'Frac Enrichment')
#
# # save any dataframe at given path
# save_dfs = corna.save_to_csv(frac_enr_df, path_dir + 'frac_enrichment.csv')
