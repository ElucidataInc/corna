import corna


path_dir = '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/data/'

mq_files = corna.read_multiquant(path_dir)

mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)

list_of_samples = ['A. [13C-glc] G9 0min', 'B. [13C-glc] G9 5min', 'C. [13C-glc] G9 15min']

background_corr = corna.met_background_correction('Succinate 117/73', merge_mq_metdata,
                                                  'A. [13C-glc] G9 0min', list_of_samples, all=False)

background_corr_df = corna.convert_to_df(background_corr)


# import corna
#
#
# path_dir = '/Users/raaisa/OneDrive/Elucidata/NA_Correction/Demo/data/splitfilesmq/'
#
# mq_files = corna.read_multiquant(path_dir)
#
# mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')
#
# merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)
#
# filtered_df = corna.filter_df(merge_mq_metdata, 'Parent', 'Citrate 191/67')
#
#
# citrate_G9 = corna.filter_df(filtered_df, 'Glucose Concentration', 'G9')
# citrate_G9_197_71 = corna.filter_df(citrate_G9, 'Name', ['Citrate 197/71','Citrate 191/67'])
#
# background_corr = corna.met_background_correction('Citrate 191/67', \
#                     filtered_df, 'A. [13C-glc] G9 0min')
#
#
# list_of_samples = ['A. [13C-glc] G9 0min', 'B. [13C-glc] G9 5min', 'C. [13C-glc] G9 15min']
#
# background_corr = corna.met_background_correction('Citrate 191/67', \
#                     filtered_df, 'A. [13C-glc] G9 0min', list_of_samples, all=False)
#
# background_corr_df = corna.convert_to_df(background_corr)
#
# na_correction = corna.na_correction_mimosa(background_corr)
# na_corr_df = corna.convert_to_df(na_correction)
#
# post_processing = corna.replace_negatives(na_correction)
# post_pro_df = corna.convert_to_df(post_processing)
#
# fractional_enr = corna.fractional_enrichment(post_processing)
# fractional_enr_df = corna.convert_to_df(fractional_enr)
#
# #save_dfs = corna.save_to_csv(fractional_enr_df, path)
#
#
#
