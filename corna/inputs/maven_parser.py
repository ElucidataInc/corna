from collections import namedtuple

import pandas as pd

from corna.helpers import create_dict_from_isotope_label_list, chemformula_schema
from . column_conventions import maven as c
from .. helpers import merge_two_dfs
#, VAR_COL, VAL_COL, SAMPLE_COL, INTENSITY_COL
from .. constants import PARENT_COL, VAR_COL, VAL_COL, FRAG_COL, SAMPLE_COL, INTENSITY_COL


MavenKey = namedtuple('MavenKey','name formula')

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
        df[FRAG_COL] = df.apply(lambda x: MavenKey(
            x[c.NAME], x[c.FORMULA]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df


def convert_std_label_key_to_maven_label(df):
    #TODO: File format change should lead to removal
    #of these fucntions
    """
    This function converts the labels C13_1_N15_1 in the form
    C13N15-label-1-1
    """
    def process_label(label):
        label_dict = create_dict_from_isotope_label_list(label.split('_'))
        if all(num_isotopes == 0 for num_isotopes in label_dict.values()):
            return 'C12 PARENT'
        else:
            isotrac_string = ''
            num_string = ''
            for isotrac, num_iso in label_dict.iteritems():
                if num_iso != 0:
                    isotrac_string = isotrac_string + isotrac
                    num_string = num_string +'-' + str(num_iso)
            return isotrac_string + '-label' + num_string

    df['Label'] = [process_label(l) for l in df['Label']]
    return df


def convert_labels_to_std(df, iso_tracers):
    """
    This function converts the labels C13N15-label-1-1 in the form
    C13_1_N15_1
    """
    def process_label(label):
        if label == 'C12 PARENT':
            return '_'.join('{}_0'.format(t) for t in iso_tracers)
        else:
            formula, enums = label.split('-label-')
            isotopes = set(''.join(map(str, i))
                           for i in chemformula_schema.parseString(formula))
            msg = """iso_tracers must have all isotopes from input data
                    Got: {!r}
                    Expected: {!r}
                  """.format(iso_tracers, isotopes.union(iso_tracers))
            assert set(isotopes).issubset(set(iso_tracers)), msg
            # The final label must have all iso_tracers
            # Use zeroes as default, else the number from given label
            inmap = {i: 0 for i in iso_tracers}
            inmap.update({i: n for i, n in zip(isotopes, enums.split('-'))})
            # The order is important, so we don't map on inmap directly
            return '_'.join("{}_{}".format(i, inmap[i]) for i in iso_tracers)

    df['Label'] = [process_label(l) for l in df['Label']]
    return df