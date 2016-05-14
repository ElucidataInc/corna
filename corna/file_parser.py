import os
import helpers as hl
import pandas as pd
import json






def read_input_data(path):
    """
    This function reads the input data file. The file can be
    csv or xlsx

    Args:
        path to input data file

    Returns:
        input data in the form of pandas dataframe
    """

    input_data = hl.read_file(path)

    return input_data


def read_metadata(path):
    """
    This function reads the metadata file. The file can be
    csv or xlsx

    Args:
        path to metadata file

    Returns:
        metadata in the form of pandas dataframe
    """

    metadata = hl.read_file(path)

    return metadata


def json_to_df(json_input):
    """
    This function takes input data in the form of json format and converts
    it in pandas dataframe

    Args:
        json_input : input data in form of json format

    Returns:
        json_to_df : pandas dataframe

    """
    #this should be the format of json input
    json_input = json.dumps(input_data.to_dict())

    json_df = pd.read_json(json_input)

    return json_df



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

    value = [x for x in df1.columns.tolist() if x not in id]

    long_form = pd.melt(df1, id_vars=id, value_vars=value)

    merged_df = pd.merge(long_form, df2, how="left", left_on=left_on,
                             right_on=right_on)

    merged_df.drop(right_on, axis=1, inplace=True)

    merged_df.rename(columns={"variable":"sample_name"}, inplace=True)

    return merged_df



def concat_mq_txts(mq_dir):

    mq_txt_files = []

    mq_txt_files += [each for each in os.listdir(mq_dir) if each.endswith('.txt')]

    df_list= []

    for files in mq_txt_files:
        df_list.append(read_input_data(mq_dir + files))

    mq_df = pd.concat(df_list)

    return mq_df


# get values from filtered maven df
def mvn_met_names(filtered_df, col_name = 'Name'):

    met_names = hl.get_unique_values(filtered_df, col_name)

    return met_names

def mvn_met_formula(filtered_df, col_name = 'Formula'):

    met_formula = hl.get_unique_values(filtered_df, col_name)

    return met_formula


# label_dict = {C13:1, N15: 1}

# get values from filtered mq df






# maven
path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
input_data = read_input_data(path_input)
metadata = read_metadata(path_metadata)
merged_df = maven_merge_dfs(input_data, metadata)
filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')
met_name = mvn_met_names(filter_df, col_name = 'Name')
met_formula = mvn_met_formula(filter_df, col_name = 'Formula')







#mq:
mq_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/data/mq/'
mq_df = concat_mq_txts(mq_dir)
mq_met_path = mq_dir + 'metadata.xlsx'
mq_metdata = read_input_data(mq_met_path)
merged_df.to_csv(mq_dir + 'mvn.csv')
mq_df.to_csv(mq_dir + 'mq.csv')

#get name, formula from df






