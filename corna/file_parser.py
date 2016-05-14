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






# get values from filtered maven df
def mvn_met_names(filtered_df, col_name = 'Name'):

    met_names = hl.get_unique_values(filtered_df, col_name)

    return met_names

def mvn_met_formula(filtered_df, col_name = 'Formula'):

    met_formula = hl.get_unique_values(filtered_df, col_name)

    return met_formula


# label_dict = {C13:1, N15: 1}

# get values from filtered mq df





#mq:
mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_df = concat_mq_txts(mq_dir)
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = read_input_data(mq_met_path)
merged_df.to_csv(mq_dir + 'mvn.csv')
mq_df.to_csv(mq_dir + 'mq.csv')

#get name, formula from df






