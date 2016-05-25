import corna

# path to directory where multiquant text data files are present
path_dir = '/Users/raaisa/OneDrive/Elucidata/NA_correction/Demo/data/'

# read multiquant data files and combine them
mq_files = corna.read_multiquant(path_dir)

# read multiquant metadata file
mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

# merge multiquant files and metadata files
merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)


# filter merged data as per requirement
citrate_G7 = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Name",
                                list_col1_vals=['Citrate 196/71', 'Citrate 191/67', 'Citrate 197/71' ], col2="Glucose Concentration", list_col2_vals=["G7"])

# filter by two columns
filtered_data = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Time",
                                list_col1_vals=['0min','30min'], col2="Glucose Concentration", list_col2_vals=["G7"])

background_corr = corna.met_background_correction_all(citrate_G7, 'Q. [13C-glc] G7 0min')

# background noise correction on filtered data
background_corr = corna.met_background_correction_all(filtered_data, 'Q. [13C-glc] G7 0min')

# background noise correction for all labels of a fragmnent
background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min')

# background noise correction by list of given samples
list_of_samples = ['Q. [13C-glc] G7 0min', 'R. [13C-glc] G7 5min', 'S. [13C-glc] G7 15min']
background_corr = corna.met_background_correction('Citrate 191/67', merge_mq_metdata, 'Q. [13C-glc] G7 0min', list_of_samples, all_samples=False)

# convert background noise corrected dictionary to dataframe
background_corr_df = corna.convert_to_df(background_corr, all = True, colname = 'Background correction')


# NA correction method on background noise corrected data
nacorr_dict = corna.na_correction_mimosa(background_corr, all = True)
na_corr_df = corna.convert_to_df(nacorr_dict, all=True, colname = 'NA corrected')

# Replace negative values by zero on NA corrected data - optional
postprocessed_out = corna.replace_negatives(nacorr_dict, all=True)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, all = True, colname =  'Replaced negatives')

# calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(postprocessed_out, all=True)
frac_enr_df = corna.convert_to_df(frac_enrichment, all = True, colname = 'Frac Enrichment')

# save any dataframe at given path
save_dfs = corna.save_to_csv(frac_enr_df, path_dir + 'frac_enrichment.csv')
