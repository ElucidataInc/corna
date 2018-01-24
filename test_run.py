# import pandas as pd
# from corna.inputs import maven_parser as mv
# from corna.output import convert_to_df, convert_to_df_nacorr
# from corna.postprocess import replace_negatives, fractional_enrichment
# from corna.helpers import merge_multiple_dfs, get_na_value_dict
# from corna.algorithms.matrix_nacorr import *
#
# df = pd.read_csv('/Users/harshit/Downloads/Demo datasets/NA Correction/LCMS/raw_intensity_file.csv')
# merge_mv_metdata = mv.convert_inputdata_to_stdfrom(df)
# na_dict = get_na_value_dict()
# na_corr_dict, ele_corr_dict = na_correction(merge_mv_metdata,['C13','N15'],23, na_dict, {},intensity_col=INTENSITY_COL,autodetect=True)
# na_corr_df = convert_to_df_nacorr(na_corr_dict, ele_corr_dict,parent=False, colname='NA corrected')
# postprocessed_out = replace_negatives(na_corr_dict)
# postprocessed_out_df = convert_to_df(postprocessed_out, parent=False, colname='CorrIntensities-Replaced_negatives')
# frac_enrichment = fractional_enrichment(postprocessed_out)
# frac_enr_df = convert_to_df(frac_enrichment, parent=False, colname='Frac Enrichment')
# df_list = [na_corr_df, frac_enr_df, postprocessed_out_df, merge_mv_metdata]
# merged_results_df = merge_multiple_dfs(df_list)
# print merged_results_df


# #######################################Run commands for LCMS/MS######################################################################
# from corna.inputs.multiquant_parser import merge_mq_metadata, mq_df_to_fragmentdict
# from corna.algorithms.mimosa_bgcorr import met_background_correction
# from corna.algorithms.mimosa_nacorr import na_correction_mimosa
# from corna.postprocess import fractional_enrichment, replace_negatives
# from corna.output import convert_to_df, convert_to_df_nacorr_MSMS
# from corna.helpers import merge_multiple_dfs
# import pandas as pd
#
# print "in ==============="

#
# sample_df = pd.read_table('../LCMS_MS/TA_SCS-ATP BCH_19May16_1June16 - TCA.txt')
# metadata_df = pd.read_excel('../LCMS_MS/metadata_mq.xlsx')
# metadata_sample = pd.read_excel('../LCMS_MS/metadata_sample.xlsx')
# merge_mq_metdata, list_of_replicates, sample_background = merge_mq_metadata(sample_df, metadata_df, metadata_sample)
# background_corr_dict = mq_df_to_fragmentdict(merge_mq_metdata)
# background_corr_dict = met_background_correction(background_corr_dict, list_of_replicates, sample_background)
# nacorrected = na_correction_mimosa(background_corr_dict)
# df1 = convert_to_df_nacorr_MSMS(nacorrected,parent=True, colname='nacorrection')
# postprocessed_out = replace_negatives(nacorrected)
# # for metabolite, fragment_dict in postprocessed_out.iteritems():
# # print postprocessed_out
# # frac_enrichment =fractional_enrichment(postprocessed_out)
# frac_enrichment = fraq_wrapper(postprocessed_out)
# # print frac_enrichment
# df = convert_to_df(frac_enrichment,parent=True, colname='Frac Enrichment')
# list1 = [df1, df]
# dfm = merge_multiple_dfs(list1)
# print dfm

import os

from corna.inputs import maven_parser as mp
from corna.inputs import multiquant_parser as mq
import pandas as pd


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MQ_FILE_PATH = os.path.join(DIR_PATH, 'tests/test_input_validation_data', "raw_mq.txt")
MQ_METADATA_PATH = os.path.join(DIR_PATH, 'tests/test_input_validation_data', "metadata_mq.xlsx")
MQ_SAMPLE_METADATA_PATH = os.path.join \
    (DIR_PATH, 'tests/test_input_validation_data', "metadata_sample.xlsx")

INPUT_FILES = {"mq_file_path": "/Users/harshit/Downloads/demo_datasets/0.2_release_demo_dataset/NA_Correction/LC-MSMS/Test_raw_file.csv",
                   "mq_metadata_path": "/Users/harshit/Downloads/metadata_dania.csv",
                   "mq_sample_metadata_path": ""
                   }
INPUT_FILES_WITHOUT_METADATA = {"mq_file_path": MQ_FILE_PATH,
                                "mq_metadata_path": MQ_METADATA_PATH,
                                "mq_sample_metadata_path": ''}


c =  mq.get_validated_df_and_logs(INPUT_FILES, 0, [])
print c[0].df
# print  "================"
# print c[1]

# print mq.mq_merge_meta()

# print mp.read_maven_file('/Users/harshit/elucidata/corna/corna/tests/test_input_validation_data/test_maven_upload_acetic.csv',
# '/Users/harshit/elucidata/corna/corna/tests/test_input_validation_data/metadata_sample_test_maven.csv')

# merge_data, logs, iso_tracer_data, element_list, summary = mp.read_maven_file('/Users/harshit/Downloads/demo_datasets/NA_Correction/LCMS/raw_intensity_file.csv', None)
# merge_data, logs, iso_tracer_data, element_list, summary = mp.read_maven_file('/Users/harshit/Downloads/EIC_Output.csv', None)
# a[0].to_csv('c2.csv')
# print iso_tracer_data


# if __name__ == '__main__':
#     import timeit
#     print timeit.timeit("fraq_wrapper(postprocessed_out)", setup= "from __main__ import fraq_wrapper", number=10)
