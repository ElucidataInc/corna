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
                                list_col1_vals=['L-Methionine'], col2="Label", list_col2_vals=['C13_2', 'C13_1'])

# isotop
iso_tracers = ['C13']

#element to be corrected
eleme_corr = {'C': ['H', 'O'], 'N': ['S']}

# NA values dict
na_dict = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205], 'N': [0.99636, 0.00364], 'S': [0.922297, 0.046832, 0.030872]}

#testing
#iso_tracers = ['C13', 'N15']
#print corna.test_sample_lab_dict(iso_tracers, merge_mv_metdata)

# na correction dictionary
#iso_tracers = ['C']
na_corr_dict = corna.na_corr_single_tracer_mvn(merge_mv_metdata, iso_tracers, eleme_corr, na_dict)
na_corr_df = corna.convert_to_df(na_corr_dict, all=False, colname = 'NA corrected')
print na_corr_df

# Replace negative values by zero on NA corrected data - optional
postprocessed_out = corna.replace_negatives(na_corr_dict, all=False)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, all = False, colname =  'Intensities Replaced negatives')


# calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(postprocessed_out, all=False)
frac_enr_df = corna.convert_to_df(frac_enrichment, all = False, colname = 'Frac Enrichment')


# save any dataframe at given path
save_dfs = corna.save_to_csv(na_corr_df, path_dir + 'frac_enrichment.csv')


