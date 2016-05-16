import numpy
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
    merged_df.rename(columns={"variable":"Sample Name", "value":"Intensity"}, inplace=True)

    return merged_df


def mvn_met_names(filtered_df, col_name = 'Name'):

    met_names = hl.get_unique_values(filtered_df, col_name)

    return met_names

def mvn_met_formula(filtered_df, col_name = 'Formula'):

    met_formula = hl.get_unique_values(filtered_df, col_name)

    return met_formula



def mq_merge_dfs(df1, df2):

    #df2['Parent_Formula'] =
    merged_df = hl.merge_dfs(df1, df2, how= 'inner', left_on = 'Component Name', right_on = 'Fragment')
    merged_df['Mass Info'] = merged_df['Mass Info'].str.replace(' / ', "_")
    remove_stds = merged_df[merged_df['Sample Name'].str.contains("std") == False]
    remove_stds['Label'] = remove_stds['Isotopic Tracer'] + "_" + remove_stds['Mass Info']

    remove_stds.pop('Mass Info')
    remove_stds.pop('Isotopic Tracer')
    remove_stds.rename(columns={"Component Name":"Name", "Area":"Intensity"}, inplace=True)
    return remove_stds



def standard_model(df, parent = True):
    if parent == True:
        df["frag_keys"] = df.apply(lambda x : tuple([x["Name"], x["Formula"], x["Parent"], x["Parent_Formula"]]), axis=1)
    elif parent == False:
        df["frag_keys"] = df.apply(lambda x : tuple([x["Name"], x["Formula"]]), axis=1)

    unique_frags = df["frag_keys"].unique().tolist()
    std_model_dict = {}

    for frags in unique_frags:
        df_subset = df[df["frag_keys"] == frags]
        unq_labels = df_subset["Label"].unique().tolist()
        lab_dict = {}
        for label in unq_labels:
            df_subset_on_labels = df_subset[df_subset["Label"] == label]
            label_frame = df_subset_on_labels.groupby("Sample Name")["Intensity"].apply(lambda x: numpy.array(x.tolist()))
            label_dict = label_frame.to_dict()
            lab_dict[label] = label_dict
        std_model_dict[frags] = lab_dict

    return std_model_dict



















