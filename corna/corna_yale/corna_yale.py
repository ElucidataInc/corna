
from .. import helpers as hl
from .. import file_parser as fp

from . import file_parser_yale as fpy
from .. import isotopomer as iso
from . import algorithms_yale as algo
from . import preprocess as preproc





# Multiquant
def read_multiquant(dir_path):
    #mq_df = hl.concat_txts_into_df(data_dir + '/')
    mq_df = hl.concat_txts_into_df(dir_path)
    return mq_df

def read_multiquant_metadata(path):
    #mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')
    mq_metdata = hl.read_file(path)

    return mq_metdata

# Multiquant
def merge_mq_metadata(mq_df, metdata):
    merged_data = fpy.mq_merge_dfs(mq_df, metdata)
    return merged_data

# Background correction for multiquant
def met_background_correction(metabolite, merged_data, background_sample, list_of_samples=[], all_samples=True, decimals=0):
    filtered_df = hl.filter_df(merged_data, "Name", metabolite)
    if all_samples:
        list_of_samples = fp.get_sample_names(filtered_df)
    else:
        list_of_samples = list_of_samples
    frag_key_df = fpy.frag_key(merged_data)
    std_model_mq = fp.standard_model(frag_key_df)
    fragments_dict = {}
    for frag_name, label_dict in std_model_mq.iteritems():
        if frag_name[2] == metabolite:
            new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
            fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True))
    preprocessed_dict = preproc.bulk_background_correction(fragments_dict, list_of_samples, background_sample, decimals)

    return preprocessed_dict


def met_background_correction_all(merged_data, background_sample, list_of_samples=[], all_samples=True, decimals=0):
    if all_samples:
        list_of_samples = fp.get_sample_names(merged_data)
    else:
        list_of_samples = list_of_samples
    metab_names = hl.get_unique_values(merged_data, 'Unlabeled Fragment')
    preprocessed_output_dict = {}
    for metabolite in metab_names:
        preprocessed_output_dict[metabolite] = met_background_correction(metabolite, merged_data,
                                                                         background_sample, list_of_samples, all_samples, decimals)
    return preprocessed_output_dict


#NA correction Multiquant
def na_correction_mimosa(preprocessed_output, all=False, decimals=2):
    if all:
        na_corrected_out = {}
        for key, value in preprocessed_output.iteritems():
            na_corrected_out[key] = algo.na_correction_mimosa_by_fragment(value, decimals)
    else:
        na_corrected_out = algo.na_correction_mimosa_by_fragment(preprocessed_output, decimals)
    return na_corrected_out


