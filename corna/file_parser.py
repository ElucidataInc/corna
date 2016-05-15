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
    #subset problem
    merged_df[merged_df['Sample Name'].str.contains("std") == False]

    #combine 2 cols to label colum - problem
    #merged_df['Label'] = '%s_%s' % (merged_df['Isotopic Tracer'], merged_df['Mass Info'])

    merged_df.rename(columns={"Component Name":"Name", "Area":"Intensity"}, inplace=True)


    return merged_df















