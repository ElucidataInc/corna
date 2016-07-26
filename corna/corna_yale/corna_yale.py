
from .. import helpers
from .. import file_parser as fp

from .file_parser_yale import get_replicates, get_background_samples, frag_key, mq_merge_dfs
from .algorithms_yale import na_correction_mimosa_by_fragment
from .preprocess import bulk_background_correction
from ..isotopomer import bulk_insert_data_to_fragment


import config_yale




# Multiquant
def read_multiquant(dir_path):
    #mq_df = hl.concat_txts_into_df(data_dir + '/')
    mq_df = helpers.concat_txts_into_df(dir_path)
    return mq_df

def read_multiquant_metadata(path):
    #mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')
    mq_metdata = helpers.read_file(path)
    return mq_metdata

# Multiquants
def merge_mq_metadata(mq_df, metdata, sample_metdata):
    merged_data = mq_merge_dfs(mq_df, metdata, sample_metdata)
    merged_data.fillna(0, inplace = True)
    list_of_replicates = get_replicates(sample_metdata, config_yale.MQ_SAMPLE_NAME, config_yale.COHORT_COL, config_yale.BACKGROUND_COL)
    sample_background = get_background_samples(sample_metdata, config_yale.MQ_SAMPLE_NAME, config_yale.BACKGROUND_COL)
    return merged_data, list_of_replicates, sample_background

def met_background_correction(metabolite, merged_data, list_of_replicates, sample_background, decimals=0):
    frag_key_df = frag_key(merged_data)
    std_model_mq = fp.standard_model(frag_key_df)
    fragments_dict = {}
    for frag_name, label_dict in std_model_mq.iteritems():
        if frag_name[2] == metabolite:
            new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
            fragments_dict.update(bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True))
    preprocessed_dict = bulk_background_correction(fragments_dict, list_of_replicates, sample_background, decimals)
    return preprocessed_dict


def met_background_correction_all(merged_data, list_of_replicates, sample_background, decimals=0):
    metab_names = helpers.get_unique_values(merged_data, 'Unlabeled Fragment')
    preprocessed_output_dict = {}
    for metabolite in metab_names:
        preprocessed_output_dict[metabolite] = met_background_correction(metabolite, merged_data,
                                                                         list_of_replicates, sample_background, decimals)
    return preprocessed_output_dict


#NA correction Multiquant
def na_correction_mimosa(preprocessed_output, all=False, decimals=2):
    if all:
        na_corrected_out = {}
        for key, value in preprocessed_output.iteritems():
            na_corrected_out[key] = na_correction_mimosa_by_fragment(value, decimals)
    else:
        na_corrected_out = na_correction_mimosa_by_fragment(preprocessed_output, decimals)
    return na_corrected_out


