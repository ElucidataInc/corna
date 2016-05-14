import os
import json
import pandas as pd
import helpers as hl




def maven_merge_dfs(df1, df2, left_on="variable", right_on="sample"):
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

    merged_df = pd.merge(long_form, df2, how="left", left_on=left_on,
                             right_on=right_on)

    merged_df.drop(right_on, axis=1, inplace=True)

    merged_df.rename(columns={"variable":"sample_name"}, inplace=True)

    return merged_df


def mvn_met_names(filtered_df, col_name = 'Name'):

    met_names = hl.get_unique_values(filtered_df, col_name)

    return met_names

def mvn_met_formula(filtered_df, col_name = 'Formula'):

    met_formula = hl.get_unique_values(filtered_df, col_name)

    return met_formula















