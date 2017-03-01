from collections import namedtuple
from corna.input_validation import check_missing,check_duplicate
from corna.input_validation import validator_column_wise,validator_for_two_column
from corna.input_validation import check_formula_is_correct
from corna.input_validation import check_postive_numerical_value
from corna.input_validation import check_label_column_format,check_label_in_formula
from corna.validation_report_class import ValidationReport
from corna.input_validation import validate_input_file

import pandas as pd

from . column_conventions import maven as c
from .. helpers import merge_two_dfs, create_dict_from_isotope_label_list, chemformula_schema, check_column_headers
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
                                  left_on=VAR_COL, right_on=c.SAMPLE)
    except KeyError:
        raise KeyError(c.SAMPLE + ' column not found in metadata')

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
    col_headers = df1.columns.tolist()
    check_column_headers(col_headers, fixed_cols)
    melt_cols = [x for x in col_headers if x not in fixed_cols]

    #try:
    long_form = pd.melt(df1, id_vars=fixed_cols, value_vars=melt_cols)
    #except KeyError():
    #    raise KeyError('columns {} not found in input data'.format(','.join(fixed_cols)))
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


def filtered_data_frame(maven_data_frame, metadata_data_frame):
    """
    This function returns filtered maven_dataframe , only those
    sample columns is returned which are present in metadata_dataframe
    sample list. It first get the intersection of maven_data_frame
    columns with all the entries of Sample in metadataframe.

    :param maven_data_frame:
    :param metadata_data_frame:
    :return:
    """
    filtered_metadata_frame = metadata_data_frame.drop_duplicates(required_columns_metadata)
    metadata_sample_column_set = set(filtered_metadata_frame[c.SAMPLE].tolist())
    maven_sample_list = set(maven_data_frame.columns.values.tolist())
    intersection_sample_list = list(maven_sample_list.intersection(metadata_sample_column_set))
    if intersection_sample_list:
        maven_data_frame_column = required_columns_raw_data+intersection_sample_list
        filtered_maven_dataframe = maven_data_frame[maven_data_frame_column]
    else:
        raise
    return filtered_maven_dataframe


def read_maven_file(maven_file_path, maven_sample_metadata_path):
    """
    This function reads maven and metadata file, convert it to df and
    checks for validation of files. If validation does not raise any
    error it returns mergedf with logs and iso-tracer data.
    :param maven_file_path: absolute path of maven raw file
    :param maven_sample_metadata_path: absolute path of metadatafile
    :return: mergedf : pandas df
             logs: dictionary of errors and warnings
             iso-tracer : dictionary of iso-tracer


    """
    vr = ValidationReport()
    input_maven_data_frame = validate_input_file(maven_file_path, required_columns_raw_data)
    if maven_sample_metadata_path:
        metadata_data_frame = validate_input_file(maven_sample_metadata_path, required_columns_metadata)
        maven_data_frame = filtered_data_frame(input_maven_data_frame, metadata_data_frame)
    else:
        maven_data_frame = input_maven_data_frame
    vr.append(check_missing(maven_data_frame))
    vr.append(check_duplicate(maven_data_frame, 0, [['Name', 'Label']]))
    sample_column = [column for column in list(maven_data_frame)
                     if column not in required_columns_raw_data]

    vr.append(validator_column_wise(maven_data_frame, 0, sample_column, [check_postive_numerical_value]))
    vr.append(validator_column_wise(maven_data_frame, 0, [c.LABEL], [check_label_column_format]))
    vr.append(validator_column_wise(maven_data_frame, 0, [c.FORMULA], [check_formula_is_correct]))
    vr.append(validator_for_two_column(maven_data_frame, c.LABEL, c.FORMULA, check_label_in_formula))
    vr.generate_report()
    vr.generate_action()
    vr.decide_action()
    corrected_maven_df = vr.take_action(maven_data_frame)
    logs = vr.generate_warning_error_list_of_strings()
    merge_df = pd.DataFrame()
    if vr.action['action'] != 'Stop_Tool':
        if maven_sample_metadata_path:
            merge_df = maven_merge_dfs(corrected_maven_df,metadata_data_frame)
        else:
            merge_df = convert_inputdata_to_stdfrom(corrected_maven_df)

    return merge_df, logs