import pandas as pd

from . column_conventions import maven as c
from .. helpers import merge_two_dfs
#, VAR_COL, VAL_COL, SAMPLE_COL, INTENSITY_COL
from .. constants import PARENT_COL, VAR_COL, VAL_COL, FRAG_COL, SAMPLE_COL, INTENSITY_COL


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
        merged_df = merge_two_dfs(long_form, df2, how='left',
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
    df[PARENT_COL] = df[c.NAME]
    df.rename(
        columns={VAR_COL: SAMPLE_COL, VAL_COL: INTENSITY_COL},
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
    fixed_cols = [c.NAME, c.LABEL, c.FORMULA]

    melt_cols = [x for x in df1.columns.tolist() if x not in fixed_cols]

    try:
        long_form = pd.melt(df1, id_vars=fixed_cols, value_vars=melt_cols)
    except KeyError():
        raise KeyError('columns {} not found in input data'.format(','.join(fixed_cols)))
    return long_form


def convert_inputdata_to_stdfrom(input_df):
    """
    This function convert the input data file(maven format) into standard data model. It gives
    the same format as in merged data (maven + metadata). This function can be used if the user
    does not wish to input metadata file and proceed as it is with the input data file

    Args:
        input_df : MAVEN input data in the form of pandas dataframe
    Returns:
        std_form_df : dataframe with input data in standard data model format that can be
                    used in further processing
    """
    long_form = melt_df(input_df)
    std_form_df = column_manipulation(long_form)

    return std_form_df


def frag_key(df):
    """
    This function creates a fragment key column in merged data based on parent information.
    """
    try:
        df[FRAG_COL] = df.apply(lambda x: tuple(
            [x[c.NAME], x[c.FORMULA]]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df
