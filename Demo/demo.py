import corna


path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data/splitfilesmq/'

mq_files = corna.read_multiquant(path_dir)

mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)

citrate_G7 = corna.filtering_df(merge_mq_metdata, num_col=2, col1="Name",
                                list_col1_vals=['Citrate 196/71', 'Citrate 191/67', 'Citrate 197/71' ], col2="Glucose Concentration",
                                list_col2_vals=["G7"])


background_corr = corna.met_background_correction_all(citrate_G7, 'Q. [13C-glc] G7 0min')

background_corr_df = corna.convert_to_df(background_corr, all = True, colname = 'Background correction')


nacorr_dict = corna.na_correction_mimosa(background_corr, all = True)

na_corr_df = corna.convert_to_df(nacorr_dict, all=True, colname = 'NA corrected')

postprocessed_out = corna.replace_negatives(nacorr_dict, all=True)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, all = True, colname =  'Replaced negatives')

frac_enrichment = corna.fractional_enrichment(postprocessed_out, all=True)
frac_enr_df = corna.convert_to_df(frac_enrichment, all = True, colname = 'Frac Enrichment')

save_dfs = corna.save_to_csv(frac_enr_df, path_dir + 'frac_enrichment.csv')
