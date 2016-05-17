import corna


path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data/'

mq_files = corna.read_multiquant(path_dir)

mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)

filtered_df = corna.filter_df(merge_mq_metdata, 'Parent', 'Citrate 191/111')


list_of_samples = ['A. [13C-glc] G2.5 0min', 'B. [13C-glc] G2.5 5min', 'C. [13C-glc] G2.5 15min', 'D. [13C-glc] G2.5 30min',\
'E. [13C-glc] G2.5 60min', 'F. [13C-glc] G2.5 120min', 'G. [13C-glc] G2.5 240min', 'H. [6,6-DD-glc] G2.5 240min']

background_corr = corna.met_background_correction('Citrate 191/111', \
					filtered_df, 'A. [13C-glc] G2.5 0min', list_of_samples)
background_corr_df = corna.convert_to_df(background_corr)

na_correction = corna.na_correction_mimosa(background_corr)
na_corr_df = corna.convert_to_df(na_correction)

post_processing = corna.replace_negatives(na_correction)
post_pro_df = corna.convert_to_df(post_processing)

fractional_enr = fractional_enrichment(post_processing)
fractional_enr_df = corna.convert_to_df(fractional_enr)

#save_dfs = corna.save_to_csv(fractional_enr_df, path)



