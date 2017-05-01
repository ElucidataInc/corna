import os
import pandas as pd
import pickle

import corna

path_dir = os.path.join(os.path.dirname(__file__),"test_data")
gcms_corr_merged = pickle.load(open(os.path.join(path_dir,"gcms_corr.p"),"r"))

def test_gcms_full():
    input_file = os.path.join(path_dir,"GCMS_raw.xlsx")
    maven_data = corna.read_file(input_file)
    merge_mv_metdata = corna.convert_inputdata_to_stdfrom(maven_data)
    iso_tracers = ['C13']
    eleme_corr = {'C': ['R','O','H']}
    na_dict = corna.get_na_value_dict()
    na_corr_dict = corna.na_correction(merge_mv_metdata, iso_tracers, eleme_corr, na_dict)
    na_corr_df = corna.convert_to_df(na_corr_dict, parent=False, colname='NA corrected')
    postprocessed_out = corna.replace_negatives(na_corr_dict)
    postprocessed_out_df = corna.convert_to_df(postprocessed_out, parent=False,
                                               colname='CorrIntensities-Replaced_negatives')
    frac_enrichment = corna.fractional_enrichment(postprocessed_out)
    frac_enr_df = corna.convert_to_df(frac_enrichment, parent=False, colname='Frac Enrichment')
    df_list = [na_corr_df, frac_enr_df, postprocessed_out_df, merge_mv_metdata]
    merged_results_df = corna.merge_multiple_dfs(df_list)
    assert pd.DataFrame.equals(merged_results_df, gcms_corr_merged)
