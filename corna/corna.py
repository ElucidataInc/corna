
import warnings
import pandas as pd

import helpers as hl
import file_parser as fp
import isotopomer as iso
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

def get_na_value_dict():
    na_mass_dict =  hl.ISOTOPE_NA_MASS
    NA = na_mass_dict['NA']
    elements = na_mass_dict['Element']
    out_dict = {}
    chemical_elements = list(set(elements.values()))
    for e in chemical_elements:
        isotope_dict = {k: v for k, v in elements.iteritems() if v == e}
        isotope_list = isotope_dict.keys()
        na_correction = [NA[x] for x in isotope_list]
        na_correction.sort(reverse=True)
        out_dict[e] = na_correction
    return out_dict

# NA correction
def na_correction(merged_df, iso_tracers, eleme_corr, na_dict):
    eleme_corr_invalid_entry(iso_tracers, eleme_corr)
    hl.convert_labels_to_std(merged_df, iso_tracers)

    metabolite_dict = algo.fragmentsdict_model(merged_df)
    na_corr_dict = {}
    for metabolite, fragments_dict in metabolite_dict.iteritems():
        na_corr_dict[metabolite] = nacorr.na_correction(fragments_dict, iso_tracers, eleme_corr, na_dict)

    return na_corr_dict


def eleme_corr_invalid_entry(iso_tracers, eleme_corr):
    for key, value in eleme_corr.iteritems():
        for el in algo.get_atoms_from_tracers(iso_tracers):
            if el in value:
                raise KeyError('An iso tracer cannot be an Indistinguishable element (' + el + ') , invalid input in eleme_corr dictionary')

# Post processing: Replacing negatives by zero
def replace_negatives(na_corr_dict, replace_negative = True):
    post_processed_dict = {}
    for metabolite, fragment_dict in na_corr_dict.iteritems():
        post_processed_dict[metabolite] = postpro.replace_negative_to_zero(fragment_dict, replace_negative)

    return post_processed_dict

# Fractional Enrichment
def fractional_enrichment(post_processed_out, decimals=4):
    frac_enrichment_dict = {}
    for metabolite, fragment_dict in post_processed_out.iteritems():
        frac_enrichment_dict[metabolite] = postpro.enrichment(fragment_dict, decimals)
    return frac_enrichment_dict

# Convert nested dict to dataframe for visualization
def convert_to_df(dict_output, colname = 'col_name'):
    df_list = []
    for metabolite, fragment_dict in dict_output.iteritems():

        std_model = iso.fragment_dict_to_std_model(fragment_dict)
        model_to_df = out.convert_dict_df(std_model, parent=False)
        df_list.append(model_to_df)

        model_to_df = hl.concatentate_dataframes_by_col(df_list)

    model_to_df.rename(columns={"Intensity": str(colname)}, inplace=True)

    return model_to_df


# Save any dataframe to csv
def save_to_csv(df, path):
    df.to_csv(path)



