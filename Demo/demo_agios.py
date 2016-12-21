import os
import corna

from corna import config


config.NAME_COL = 'Name'

# path to directory where data files are present - give the path the file
# as this path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data/'
path_dir = os.path.join(os.path.dirname(__file__), 'data_agios')


# read maven data
maven_data = corna.read_file(path_dir + '/testfiles/nacorr_test_1.xlsx')
merge_mv_metdata = corna.convert_inputdata_to_stdfrom(maven_data)

#print maven_data
#test_m0_2.csv

# For json input, use this funtion:
#json_input = json.dumps(maven_data.to_dict())
#maven_data = corna.convert_json_to_df(json_input)

# read maven metadata file
#maven_metadata = corna.read_file(path_dir + '/metadata.csv')

# merge maven files and metadata files
#merge_mv_metdata = corna.maven_merge_dfs(maven_data, maven_metadata)
# isotopic tracers
#iso_tracers = ['H2']
iso_tracers = ['C13']

# element to be corrected
# in case of no indistinguishable elements, eleme corr is empty dictionary
eleme_corr = {}
# in case of indistinguishable elements

#eleme_corr = {'C': ['H']}


# NA values dict
na_dict = corna.get_na_value_dict()

# edit na values
#na_dict['H'][0] = 0.989

# NA correction
na_corr_dict = corna.na_correction(merge_mv_metdata, iso_tracers, eleme_corr, na_dict)
na_corr_df = corna.convert_to_df(na_corr_dict, parent=False, colname='NA corrected')
#working till this point


# Replace negative values by zero on NA corrected data - optional
print 'before post processed'
postprocessed_out = corna.replace_negatives(na_corr_dict)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, parent=False, colname='CorrIntensities-Replaced_negatives')
print 'postprocessed_out_df'

# calculate fractional enrichment on post processed data
print 'before frac'
frac_enrichment = corna.fractional_enrichment(postprocessed_out)
print 'frac'
frac_enr_df = corna.convert_to_df(frac_enrichment, parent=False, colname='Frac Enrichment')
print 'frac comp'
# # combine results - dataframe with na correction column, frac enrichment column and post processed column
df_list = [na_corr_df, frac_enr_df, postprocessed_out_df, merge_mv_metdata]
merged_results_df = corna.merge_multiple_dfs(df_list)
print merged_results_df
# # filter any dataframe as per requirement.
# # any number of columns and column values can be filtered
# col_rename = {'Name': ['L-Methionine'], "Sample": ['sample_1', 'sample_2']}
# filtered_data = corna.filter_df(merged_results_df, col_rename)
# # save any dataframe at given path
# save_dfs = corna.save_to_csv(merged_results_df, path_dir + 'results.csv')
#
