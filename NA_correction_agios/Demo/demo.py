import corna

# path to directory where multiquant text data files are present
path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data_agios/'

# read maven data
maven_data = corna.read_maven(path_dir + '/maven_output.csv')

# read maven metadata file
maven_metadata = corna.read_mvn_metadata(path_dir + '/metadata.csv')

# merge maven files and metadata files
merge_mv_metdata = corna.merge_mvn_metadata(maven_data, maven_metadata)

# filter merged data as per requirement
# filter by one column - sample name
sample_1_data = corna.filtering_df(merge_mv_metdata, num_col=1, col1="Sample Name",
                                list_col1_vals=['sample_1'])

# filter by two columns - metabolite name and label
filtered_data = corna.filtering_df(merge_mv_metdata, num_col=2, col1="Name",
                                list_col1_vals=['L-Methionine'], col2="Label", list_col2_vals=['C13-label-1', 'C13-label-2'])



# NA correction method on background noise corrected data
#nacorr_dict = corna.na_correction_mimosa(background_corr, all = True)
#na_corr_df = corna.convert_to_df(nacorr_dict, all=True, colname = 'NA corrected')

# Replace negative values by zero on NA corrected data - optional
#postprocessed_out = corna.replace_negatives(nacorr_dict, all=True)
#postprocessed_out_df = corna.convert_to_df(postprocessed_out, all = True, colname =  'Replaced negatives')

# calculate fractional enrichment on post processed data
#frac_enrichment = corna.fractional_enrichment(postprocessed_out, all=True)
#frac_enr_df = corna.convert_to_df(frac_enrichment, all = True, colname = 'Frac Enrichment')

# save any dataframe at given path
#save_dfs = corna.save_to_csv(frac_enr_df, path_dir + 'frac_enrichment.csv')
