import corna

# path to directory where multiquant text data files are present
#path_dir = '/Users/raa/OneDrive/Elucidata_Sini/NA_correction/Demo/data_yale/'
path_dir = '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/data_yale/'

# read multiquant data files and combine them
mq_files = corna.read_multiquant(path_dir + 'tca_data_mq/')


# read multiquant metadata file
mq_metadata = corna.read_multiquant_metadata(path_dir + 'mq_metadata.xlsx')
mq_sample_metadata = corna.read_multiquant_metadata(path_dir + 'metadata_samples.xlsx')

# merge multiquant files and metadata files
merge_mq_metdata, list_of_replicates, sample_background = corna.merge_mq_metadata(mq_files, mq_metadata, mq_sample_metadata)
save_dfs = corna.save_to_csv(merge_mq_metdata, path_dir + 'merged_input_data.csv')
# filter merged data as per requirement
#citrate_G7 = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Name",
#                                 list_col1_vals=['Citrate 196/71', 'Citrate 191/67', 'Citrate 197/71' ], col2="Glucose Conc", list_col2_vals=["G7"])
#
# # filter by two columns
# filtered_data = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Time",
#                                 list_col1_vals=['0min','30min'], col2="Glucose Concentration", list_col2_vals=["G7"])
#
background_corr_dict = corna.mq_df_to_fragmentdict(merge_mq_metdata)

background_corr = corna.met_background_correction(background_corr_dict, list_of_replicates, sample_background)
# # background noise correction on filtered data
# #background_corr = corna.met_background_correction_all(filtered_data, 'Q. [13C-glc] G7 0min')
#
# # background noise correction for all labels of a fragmnent
# #background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min')
#
# # background noise correction by list of given samples
# list_of_samples = ['Q. [13C-glc] G7 0min', 'R. [13C-glc] G7 5min', 'S. [13C-glc] G7 15min']
# #background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min', list_of_samples, all_samples=False)
#
# # convert background noise corrected dictionary to dataframe
background_corr_df = corna.convert_to_df(background_corr, True, colname='Background correction')

print background_corr_df

#postprocessed_out_df =corna.merge_multiple_dfs([merge_mq_metdata, background_corr_df])
#
# # NA correction method on background noise corrected data
nacorr_dict = corna.na_correction_mimosa(background_corr)
#
na_corr_df = corna.convert_to_df(nacorr_dict, True, colname='NA corrected')
# print na_corr_df
# # Replace negative values by zero on NA corrected data - optional
postprocessed_out = corna.replace_negatives(nacorr_dict)
# print postprocessed_out
postprocessed_out_df = corna.convert_to_df(postprocessed_out, True, colname='Replaced negatives')
#
# # calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(postprocessed_out)
frac_enr_df = corna.convert_to_df(frac_enrichment, True, colname='Frac Enrichment')
#
# # save any dataframe at given path
save_dfs = corna.save_to_csv(frac_enr_df, path_dir + 'frac_enrichment.csv')
