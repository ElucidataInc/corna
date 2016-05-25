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
malate = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Parent",
                                list_col1_vals=['Malate 133/115'],
                            col2="Glucose Concentration", list_col2_vals=["G9"])
corna.save_to_csv(malate, '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/malate_in.csv')
glutamate = corna.filtering_df(merge_mq_metdata, num_col=1, col1="Parent",
                                list_col1_vals=['Glutamate 146/128'],
                               col2="Glucose Concentration", list_col2_vals=["G7"])

background_corr_malate = corna.met_background_correction('Malate 133/115', malate, 'A. [13C-glc] G9 0min')
postprocessed_out_malate = corna.replace_negatives(background_corr_malate, all=False)
background_corr_df_malate = corna.convert_to_df(postprocessed_out_malate, all = False, colname = 'Background correction')

#output file
background_corr_out = pd.read_excel(path_dir + '/test_demo_output.xlsx', 'BackgroundCorrection')
background_corr_out_malate = corna.filtering_df(background_corr_out, num_col=1, col1='name',
                                                list_col1_vals=['Malate 133/115', 'Malate 134/116',
                                                                'Malate 135/117', 'Malate 136/118',
                                                                'Malate 137/119'])

corna.save_to_csv(background_corr_df_malate, path_dir + '/our_out_malate_bg.csv')
corna.save_to_csv(background_corr_out_malate, path_dir + '/excel_out_malate_bg.csv')

na_corr_out = pd.read_excel(path_dir + '/test_demo_output.xlsx', 'NACorrection')
na_corr_out_malate = corna.filtering_df(na_corr_out, num_col=1, col1='name',
                                                list_col1_vals=['Malate 133/115', 'Malate 134/116',
                                                                'Malate 135/117', 'Malate 136/118',
                                                                'Malate 137/119'])

# NA correction method on background noise corrected data
nacorr_dict = corna.na_correction_mimosa(postprocessed_out_malate, all = False)
na_postprocessed_out_malate = corna.replace_negatives(nacorr_dict, all=False)
na_corr_df_malate = corna.convert_to_df(na_postprocessed_out_malate, all=False, colname = 'NA corrected')


corna.save_to_csv(na_corr_df_malate, path_dir + '/our_out_malate_na.csv')
corna.save_to_csv(na_corr_out_malate, path_dir + '/excel_out_malate_na.csv')


# # calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(na_postprocessed_out_malate, all=False)
frac_enr_df_malate = corna.convert_to_df(frac_enrichment, all = False, colname = 'Frac Enrichment')

frac_enr_out = pd.read_excel(path_dir + '/test_demo_output.xlsx', 'FractionalEnrichment')
frac_enr_out_malate = corna.filtering_df(frac_enr_out, num_col=1, col1='name',
                                                list_col1_vals=['Malate 133/115', 'Malate 134/116',
                                                                'Malate 135/117', 'Malate 136/118',
                                                                'Malate 137/119'])

corna.save_to_csv(frac_enr_df_malate, path_dir + '/our_out_malate_ape.csv')
corna.save_to_csv(frac_enr_out_malate, path_dir + '/excel_out_malate_ape.csv')
