import os
import json
import pandas as pd
import helpers as hl




def maven_merge_dfs(df1, df2):
    """
    This function combines the input file dataframe and the metadata
    file dataframe

    Args:
        input_data : input data in form of pandas dataframe

        metadata : metadata in the form of pandas dataframe

    Returns:
        combined_data : dataframe with input data and metadata combined
    """
    id = ["Name", "Formula", "Label"] #column names to go in config

    # put in functions - combinig dfs
    value = [x for x in df1.columns.tolist() if x not in id]

    long_form = pd.melt(df1, id_vars=id, value_vars=value)

    merged_df = hl.merge_dfs(long_form, df2, how = 'left', left_on = 'variable', right_on = 'sample')

    merged_df['Parent'] = merged_df['Name']
    merged_df.rename(columns={"variable":"sample_name", "value":"Intensity"}, inplace=True)

    return merged_df


def mvn_met_names(filtered_df, col_name = 'Name'):

    met_names = hl.get_unique_values(filtered_df, col_name)

    return met_names

def mvn_met_formula(filtered_df, col_name = 'Formula'):

    met_formula = hl.get_unique_values(filtered_df, col_name)

    return met_formula


def mq_merge_dfs(df1, df2):
    merged_df = hl.merge_dfs(df1, df2, how= 'inner', left_on = 'Component Name', right_on = 'Fragment')
    remove_stds = merged_df[merged_df['Sample Name'].str.contains("std") == False]
    remove_stds['Label'] = remove_stds['Isotopic Tracer'] + "_" + remove_stds['Mass Info']
    remove_stds.pop('Mass Info')
    remove_stds.pop('Isotopic Tracer')
    remove_stds.rename(columns={"Component Name":"Name", "Area":"Intensity"}, inplace=True)
    return remove_stds

def standard_model(df):
    df["tups"] = df.apply(lambda x : tuple([x["Name"], x["Formula"], x["Parent"]]), axis=1)
    unq_tups = df["tups"].unique().tolist()
    outer_dict = {}

    for tups in unq_tups:
        df_subset = df[df["tups"] == tups]
        unq_labels = df_subset["Label"].unique().tolist()
        tup_dict = {}
        for label in unq_labels:
            df_subset_on_labels = df_subset[df_subset["Label"] == label]
            label_frame = df_subset_on_labels.groupby("sample_name")["Intensity"].apply(lambda x: x.tolist())
            label_dict = label_frame.to_dict()
            tup_dict[label] = label_dict
        outer_dict[tups] = tup_dict

    return outer_dict

















