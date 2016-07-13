import corna
from corna import config

config.NAME_COL = 'Name'
# path to directory where multiquant text data files are present
path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data_agios/'
#path_dir = '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/data_agios/testfiles'
# read maven data
#single tracer data
maven_data = corna.read_maven(path_dir + '/aceticacid.csv')

# single tracer indistinguishable
#maven_data = corna.read_maven(path_dir + '/aceticacid_indist.csv')

#double tracer
#maven_data = corna.read_maven(path_dir + '/double_trac_test.csv')
#print maven_data


# For json input, use this funtion:
#json_input = json.dumps(maven_data.to_dict())
#maven_data = corna.convert_json_to_df(json_input)

# read maven metadata file
maven_metadata = corna.read_mvn_metadata(path_dir + '/metadata.csv')

# merge maven files and metadata files
merge_mv_metdata = corna.merge_mvn_metadata(maven_data, maven_metadata)
#print merge_mv_metdata

# tracer isotopes
iso_tracers = ['C13']
#iso_tracers = ['C13', 'N15']

#element to be corrected
#eleme_corr = {'C': ['H']}
# In case of no indistinguishable elements, eleme corr is empty dictionary
eleme_corr = {}


# NA values dict
na_dict = corna.get_na_dict(iso_tracers, eleme_corr)

# edit na values
#na_dict['H'][0] = 0.989

#double_trac_indist = corna.na_double_trac_indist(iso_tracers, eleme_corr, merge_mv_metdata, na_dict)
#print 'kron matrix'
#print corna.convert_to_df(double_trac_indist, colname = 'NA corrected')

# NA correction
na_corr_dict = corna.na_correction(merge_mv_metdata, iso_tracers, eleme_corr, na_dict)
na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
print maven_data
print na_corr_df


# Replace negative values by zero on NA corrected data - optional
postprocessed_out = corna.replace_negatives(na_corr_dict, replace_negative = True)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, colname =  'CorrIntensities-Replaced_negatives')

# calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(postprocessed_out,)
frac_enr_df = corna.convert_to_df(frac_enrichment, colname = 'Frac Enrichment')

# combine results - dataframe with na correction column, frac enrichment column and post processed column
df_list = [na_corr_df, frac_enr_df, postprocessed_out_df, merge_mv_metdata]
merged_results_df = corna.merge_dfs(df_list)

# filter any dataframe as per requirement and save it to csv
# filter by one column - sample name
sample_1_data = corna.filtering_df(frac_enr_df, num_col=1, col1="Sample Name",
                                list_col1_vals=['sample_1'])

# filter by two columns - metabolite name and label
filtered_data = corna.filtering_df(frac_enr_df, num_col=2, col1="Name",
                                list_col1_vals=['L-Methionine'], col2="Sample Name", list_col2_vals=['sample_1', 'sample_2'])


filtered_data = corna.filtering_df(frac_enr_df, num_col=3, col1="Name",
                                list_col1_vals=['L-Methionine'], col2="Sample Name", list_col2_vals=['sample_1', 'sample_2'],\
                                col3="Label", list_col3_vals = ['C13_1_N15_0', 'C13_2_N15_0'])

# save any dataframe at given path
save_dfs = corna.save_to_csv(merged_results_df, path_dir + 'results.csv')


