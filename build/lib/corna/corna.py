import os
import sys
import warnings
import numpy as np
import pandas as pd

import config
import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import algorithms as algo
import postprocess as postpro
import na_correction as nacorr
import output as out


warnings.simplefilter(action = "ignore")

# Maven
def read_maven(path):
    maven_output = hl.read_file(path)
    return maven_output

def read_mvn_metadata(path):
    mvn_metadata = hl.read_file(path)
    return mvn_metadata

# Maven input + metadata
def merge_mvn_metadata(mv_df, metadata):
    merged_data = fp.maven_merge_dfs(mv_df, metadata)
    return merged_data

def convert_inputdata_to_stdfrom(input_df):
    id = ["Name", "Formula", "Label"]
    value = [x for x in input_df.columns.tolist() if x not in id]
    long_form = pd.melt(input_df, id_vars=id, value_vars=value)
    long_form['Parent'] = long_form['Name']
    long_form.rename(columns={"variable":"Sample Name", "value":"Intensity"}, inplace=True)
    return long_form

def convert_json_to_df(json_input):
    df = hl.json_to_df(json_input)
    return df

def merge_dfs(df_list):
    combined_dfs = reduce(lambda left,right: pd.merge(left,right, on= ['Label', 'Sample Name', 'Name', 'Formula']), df_list)
    #combined_dfs = reduce(lambda left,right: pd.merge(left,right), df_list)
    #on= ['Name', 'Formula', 'Label', 'Sample Name']
    return combined_dfs


# Filtering data
def filtering_df(df, num_col = 3, col1 = 'col1', list_col1_vals = [], col2 = 'col2', list_col2_vals = [], col3 = 'col3', list_col3_vals = []):
	filtered_df = hl.filtering_df(df, num_col, col1, list_col1_vals, col2, list_col2_vals, col3, list_col3_vals)
	return filtered_df


def get_na_dict(isotracers, eleme_corr):
    ele_list = algo.get_atoms_from_tracers(isotracers)
    for key, value in eleme_corr.iteritems():
        ele_list.append(key)
        for ele in value:
            ele_list.append(ele)
    ele_list = list(set(ele_list))
    return hl.get_sub_na_dict(ele_list)

# NA correction
def na_correction(merged_df, iso_tracers, eleme_corr, na_dict):

    invalid_eleme_corr = eleme_corr_invalid_entry(iso_tracers, eleme_corr)

    na_corr_dict = nacorr.na_correction(merged_df, iso_tracers, eleme_corr, na_dict)

    return na_corr_dict


def eleme_corr_invalid_entry(iso_tracers, eleme_corr):
    for key, value in eleme_corr.iteritems():
        for el in algo.get_atoms_from_tracers(iso_tracers):
            if el in value:
                raise KeyError('An iso tracer cannot be an Indistinguishable element (' + el + ') , invalid input in eleme_corr dictionary')

# Post processing: Replacing negatives by zero
def replace_negatives(na_corr_dict, replace_negative = True, all=False):
    if all:
        post_processed_dict = {}
        for metabolite, fragment_dict in na_corr_dict.iteritems():
            post_processed_dict[metabolite] = postpro.replace_negative_to_zero(fragment_dict, replace_negative = True)
    else:
        post_processed_dict = postpro.replace_negative_to_zero(na_corr_dict, replace_negative = True)
    return post_processed_dict

# Fractional Enrichment
def fractional_enrichment(post_processed_out, all=False, decimals=4):
    if all:
        frac_enrichment_dict = {}
        for metabolite, fragment_dict in post_processed_out.iteritems():
            frac_enrichment_dict[metabolite] = postpro.enrichment(fragment_dict, decimals)
    else:
        frac_enrichment_dict = postpro.enrichment(post_processed_out, decimals)
    return frac_enrichment_dict

# Convert nested dict to dataframe for visualization
def convert_to_df(dict_output, all=False, colname = 'col_name'):
    if all:
        df_list = []

        for metabolite, fragment_dict in dict_output.iteritems():
            std_model = iso.fragment_dict_to_std_model(fragment_dict, mass=False, number=True)

            model_to_df = out.convert_dict_df(std_model, parent=False)
            df_list.append(model_to_df)

        model_to_df = hl.concatentate_dataframes_by_col(df_list)

    else:

        std_model = iso.fragment_dict_to_std_model(dict_output, mass=False, number=True)

        model_to_df = out.convert_dict_df(std_model, parent=False)


    model_to_df.rename(columns={"Intensity": str(colname)}, inplace=True)

    return model_to_df


# Save any dataframe to csv
def save_to_csv(df, path):
    df.to_csv(path)




#--------------------YALE ----------------------------------------------------------

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
    merged_data = fp.mq_merge_dfs(mq_df, metdata)
    return merged_data

# Background correction for multiquant
def met_background_correction(metabolite, merged_data, background_sample, list_of_samples=[], all_samples=True, decimals=0):
    filtered_df = hl.filter_df(merged_data, "Name", metabolite)
    if all_samples:
        list_of_samples = fp.get_sample_names(filtered_df)
    else:
        list_of_samples = list_of_samples
    std_model_mq = fp.standard_model(merged_data, parent = True)
    fragments_dict = {}
    for frag_name, label_dict in std_model_mq.iteritems():
        if frag_name[2] == metabolite:
            new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
            fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True, number=False, mode=None))
    preprocessed_dict = preproc.bulk_background_correction(fragments_dict, list_of_samples, background_sample, decimals)

    return preprocessed_dict


def met_background_correction_all(merged_data, background_sample, list_of_samples=[], all_samples=True, decimals=0):
    if all_samples:
        list_of_samples = fp.get_sample_names(merged_data)
    else:
        list_of_samples = list_of_samples
    metab_names = hl.get_unique_values(merged_data, "Parent")
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


def get_na_dictionary():
    na_mass_dict =  hl.ISOTOPE_NA_MASS
    df = pd.DataFrame(na_mass_dict)
    f = lambda x: x.sort('amu', ascending=True)
    sort_df = df.groupby('Element', sort=False).apply(f)
    sort2.set_index('Element').T.to_dict('list')
    # ele_list = algo.get_atoms_from_tracers(isotracers)
    # for key, value in eleme_corr.iteritems():
    #     ele_list.append(key)
    #     for ele in value:
    #         ele_list.append(ele)
    # ele_list = list(set(ele_list))
    # return hl.get_sub_na_dict(ele_list)

