import pandas as pd

from .. import config as conf
from .. helpers import merge_dfs, VAR_COL, VAL_COL



def maven_merge_dfs(df1, df2):
    """
    This function combines the MAVEN input file dataframe and the metadata
    file dataframe

    Args:
        input_data : MAVEN input data in form of pandas dataframe
        metadata : metadata in the form of pandas dataframe

    Returns:
        combined_data : dataframe with input data and metadata combined
    """

    long_form = melt_df(df1)

    try:
        merged_df = merge_dfs(long_form, df2, how='left',
                                 left_on=VAR_COL, right_on='sample')
    except KeyError:
        raise KeyError('sample column not found in metadata')


    df_std_form = column_manipulation(merged_df)

    return df_std_form


def column_manipulation(df):
    """
    This function adds a parent column to dataframe and renames
    the sample and intensity columns in order to bring it in standard data model

    Args:
        df : dataframe on which column changes are to be done

    Returns:
        df : df with added columns and standard column names
    """
    df[conf.PARENT_COL] = df[conf.NAME_COL]

    df.rename(
        columns={VAR_COL: conf.SAMPLE_COL, VAL_COL:conf.INTENSITY_COL},
        inplace=True)

    return df




def melt_df(df1):
    """
    This function melts the dataframe in long form based on some fixed columns
    Args:
        df : dataframe to be converted in long format
    Returns:
        long_form : dataframe in long format

    """
    fixed_cols = [conf.NAME_COL, conf.LABEL_COL, conf.FORMULA_COL]

    melt_cols = [x for x in df1.columns.tolist() if x not in fixed_cols]

    try:
        long_form = pd.melt(df1, id_vars=fixed_cols, value_vars=melt_cols)
    except KeyError():
        raise KeyError('columns' + conf.NAME_COL + conf.LABEL_COL
                       + conf.FORMULA_COL + 'not found in input data')

    return long_form


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    try:
        df[conf.FRAG_COL] = df.apply(lambda x : tuple([x[conf.NAME_COL], x[conf.FORMULA_COL]]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df