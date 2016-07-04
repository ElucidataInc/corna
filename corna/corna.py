import os
import sys
import warnings
import pandas as pd
from itertools import product

import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import algorithms as algo
import double_tracer as dbt
import sequential_algo as sqalgo
import postprocess as postpro
import output as out
import config
import numpy as np



warnings.simplefilter(action = "ignore")

# Maven
def read_maven(path):
    maven_output = hl.read_file(path)
    return maven_output

def read_mvn_metadata(path):
    mvn_metadata = hl.read_file(path)
    return mvn_metadata

# Multiquant
def read_multiquant(dir_path):
    #mq_df = hl.concat_txts_into_df(data_dir + '/')
    mq_df = hl.concat_txts_into_df(dir_path)
    return mq_df

def read_multiquant_metadata(path):
    #mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')
    mq_metdata = hl.read_file(path)

    return mq_metdata

# Merge input + metadata files

# Maven
def merge_mvn_metadata(mv_df, metadata):
    merged_data = fp.maven_merge_dfs(mv_df, metadata)
    return merged_data


# Multiquant
def merge_mq_metadata(mq_df, metdata):
    merged_data = fp.mq_merge_dfs(mq_df, metdata)
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


# NA correction
# Multiquant
def na_correction_mimosa(preprocessed_output, all=False, decimals=2):
    if all:
        na_corrected_out = {}
        for key, value in preprocessed_output.iteritems():
            na_corrected_out[key] = algo.na_correction_mimosa_by_fragment(value, decimals)
    else:
        na_corrected_out = algo.na_correction_mimosa_by_fragment(preprocessed_output, decimals)
    return na_corrected_out


#NA correction maven
def na_corr_single_tracer_mvn(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    for key, value in eleme_corr.iteritems():
        for el in algo.get_atoms_from_tracers(iso_tracers):
            if el in value:
                raise KeyError('An iso tracer cannot be an Indistinguishable element (' + el + ') , invalid input in eleme_corr dictionary')
    labels_std = hl.convert_labels_to_std(merged_df, iso_tracers)
    merged_df['Label'] = labels_std
    na_corr_model = algo.na_corrected_output(merged_df, iso_tracers, eleme_corr, na_dict)
    return na_corr_model

def na_corr_double_tracer(iso_tracers, merged_df, na_dict):
    labels_std = hl.convert_labels_to_std(merged_df, iso_tracers)
    merged_df['Label'] = labels_std
    sample_label_dict = algo.samp_label_dcit(iso_tracers, merged_df)
    formula_dict = algo.formuladict(merged_df)
    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    fragments_dict = algo.fragmentsdict_model(merged_df)
    corr_intensities_dict = {}
    for samp_name, lab_dict in sample_label_dict.iteritems():
        intens_idx_dict = {}
        no_atom_tracer1 = formula_dict[trac_atoms[0]]
        no_atom_tracer2 = formula_dict[trac_atoms[1]]
        na1 = na_dict[trac_atoms[0]][-1]
        na2 = na_dict[trac_atoms[1]][-1]
        sorted_keys = lab_dict.keys()
        sorted_keys.sort(key = lambda x: (x[0], x[1]))

        inten = []
        for tups in sorted_keys:
            inten.append(lab_dict[tups])
        corr_x=dbt.double_label_NA_corr(inten,no_atom_tracer1,no_atom_tracer2,na1,na2)
        corr_x = [x[0] for x in corr_x]

        for i in range(0,len(corr_x)):
            intens_idx_dict[sorted_keys[i]] = corr_x[i]
        corr_intensities_dict[samp_name] = intens_idx_dict

    sample_list = algo.check_samples_ouputdict(corr_intensities_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = algo.label_sample_dict(sample_list, corr_intensities_dict)

    nacorr_dict_model = algo.fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model


def na_double_trac_indist(iso_tracers, eleme_corr, merged_df, na_dict):

    labels_std = hl.convert_labels_to_std(merged_df, iso_tracers)
    merged_df['Label'] = labels_std
    sample_label_dict = algo.samp_label_dcit(iso_tracers, merged_df)
    formula_dict = algo.formuladict(merged_df)
    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    fragments_dict = algo.fragmentsdict_model(merged_df)

    #formula_dict = {'C': 5, 'H': 10, 'N':1, 'O':2, 'S':1}
    eleme_corr = {'C': ['H']}

    eleme_corr_list = ['C', 'H', 'N']


    no_atom_tracers = []
    for i in eleme_corr_list:
        no_atom_tracers.append(formula_dict[i])

    for samp_name, lab_dict in sample_label_dict.iteritems():

        l = [np.arange(x+1) for x in no_atom_tracers]
        tup_list = list(product(*l))

        indist_sp = sum(eleme_corr.values(),[])
        tup_pos = [i for i, e in enumerate(eleme_corr_list) if e in indist_sp]
        #ft = filter_tuples(tup_list, tup_pos)
        intensities_list = filter_tuples(tup_list, lab_dict, tup_pos)


        icorr = dbt.double_na_correc(na_dict, formula_dict, eleme_corr_list, intensities_list)
        print icorr
    return intens_idx_dict




def filter_tuples(tuple_list, value_dict, positions):
    result_tuples = []
    for tuples in tuple_list:
        tuple_l = list(tuples)
        filtered_tuple = [tuple_l[x] for x in positions]
        if sum(filtered_tuple) == 0:
            rqrd_pos = [tuple_l[x] for x in range(0,len(tuple_l)) if x not in positions]
            rqrd_tup = tuple(rqrd_pos)
            if rqrd_tup in value_dict.keys():
                result_tuples.append(value_dict[rqrd_tup][0])
            else:
                result_tuples.append(0)
        else:
            result_tuples.append(0)
    return result_tuples
# def intensities_list(formula_dict,eleme_corr_list):
#
#     dbt.intensities_list(formula_dict,eleme_corr_list)


# def na_corr_double_trac_indist():
#     na_dict = {'C':[0.95,0.05],
#            'H':[0.98,0.01,0.01], 'N':[0.8,0.2],
#            'O':[0.95,0.03,0.02],
#            'S': [0.8,0.05,0.15]}

#     formula_dict = {'C': 5, 'H': 10, 'N':1, 'O':2, 'S':1}

#     correction_vector = [1.]

#     #eleme_corr ={'C':['H','O'], 'N':['S']}
#     eleme_corr_list = ['C', 'H', 'N']
#     #idx=list(product(np.arange(6),np.arange(11), np.arange(3), np.arange(2), np.arange(2)))

#     matx = [1.]
#     for trac in eleme_corr_list:
#         no_atom_tracer = formula_dict[trac]
#         eleme_corr = {}
#         mat_tracer = algo.corr_matrix(str(trac), formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)
#         matx = np.kron(matx, mat_tracer)
#         print matx

#     return matx




def na_corr_multiple_tracer(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):

    for key, value in eleme_corr.iteritems():
        for el in algo.get_atoms_from_tracers(iso_tracers):
            if el in value:
                raise KeyError('An iso tracer cannot be an Indistinguishable element (' + el + ') , invalid input in eleme_corr dictionary')
    labels_std = hl.convert_labels_to_std(merged_df, iso_tracers)
    merged_df['Label'] = labels_std
    nacorr_multiple_model = sqalgo.correction_tracer2(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False)
    return nacorr_multiple_model

def na_correction(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    if len(iso_tracers) == 1:
        na_corr_dict = na_corr_single_tracer_mvn(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False)

    elif len(iso_tracers) == 2:
        na_corr_dict = na_corr_double_tracer(iso_tracers, merged_df, na_dict)
    else:
        na_corr_dict = na_corr_multiple_tracer(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False)
    return na_corr_dict



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


def get_na_dict(isotracers, eleme_corr):
    ele_list = algo.get_atoms_from_tracers(isotracers)
    for key, value in eleme_corr.iteritems():
        ele_list.append(key)
        for ele in value:
            ele_list.append(ele)
    ele_list = list(set(ele_list))
    return hl.get_sub_na_dict(ele_list)












