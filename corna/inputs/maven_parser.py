import pandas as pd

from collections import namedtuple

from column_conventions import maven as c
from corna import constants as con
from corna import dataframe_validator
from corna import input_validation
from corna import dataframe_validator
from corna.helpers import merge_two_dfs, create_dict_from_isotope_label_list
from corna.helpers import chemformula_schema, check_column_headers
from corna.validation_report_class import ValidationReport



from . column_conventions import maven as c
from .. helpers import merge_two_dfs, create_dict_from_isotope_label_list, chemformula_schema, check_column_headers
#, VAR_COL, VAL_COL, SAMPLE_COL, INTENSITY_COL
from .. constants import PARENT_COL, VAR_COL, VAL_COL, FRAG_COL, SAMPLE_COL, INTENSITY_COL

MavenKey = namedtuple('MavenKey','name formula')

REQUIRED_COLUMNS_MAVEN = [c.NAME, c.LABEL, c.FORMULA]
REQUIRED_COLUMNS_MAVEN_METADATA = [c.SAMPLE]

LOGS = {}
ISOTRACER = []

COLUMN_DUPLICATE_CHECK = [[c.NAME,c.LABEL]]
COLUMN_DUPLICATE_CHECK = [[c.NAME,c.LABEL]]
ISOTRACER_COLUMN = 'isotracer'
VALIDATOR = ValidationReport()
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
                                  left_on=con.VAR_COL, right_on=c.SAMPLE)
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
    df[con.PARENT_COL] = df[c.NAME]
    df.rename(
        columns={con.VAR_COL: con.SAMPLE_COL, con.VAL_COL: con.INTENSITY_COL},
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
        df[con.FRAG_COL] = df.apply(lambda x: MavenKey(
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
    filtered_metadata_frame = metadata_data_frame.drop_duplicates(REQUIRED_COLUMNS_MAVEN_METADATA)
    metadata_sample_column_set = set(filtered_metadata_frame[c.SAMPLE].tolist())
    maven_sample_list = set(maven_data_frame.columns.values.tolist())
    intersection_sample_list = list(maven_sample_list.intersection(metadata_sample_column_set))
    if intersection_sample_list:
        maven_data_frame_column = REQUIRED_COLUMNS_MAVEN+intersection_sample_list
        filtered_maven_dataframe = maven_data_frame[maven_data_frame_column]
    else:
        raise
    return filtered_maven_dataframe


def get_metadata_df(metadata_path):

    if input_validation.validate_input_file(metadata_path):
        return dataframe_validator.read_input_file(metadata_path)
    else:
        return input_validation.get_df()


def get_sample_column(maven_df):
    """
    This function will extract out sample column headers
    from the maven df and returns in the form of list.
    :param maven_df: maven dataframe
    :return: sample column headers in the data frame
    """
    return [column for column in list(maven_df)
                     if column not in REQUIRED_COLUMNS_MAVEN]


def get_corrected_maven_df(maven_df):

    VALIDATOR.append(report_missing_values(maven_df))
    VALIDATOR.append(report_duplicate_values(maven_df))
    VALIDATOR.append(report_label_column_format(maven_df))
    VALIDATOR.append(report_label_in_formula(maven_df))
    VALIDATOR.append(report_formula_column_format(maven_df))
    VALIDATOR.append(report_intensity_values(maven_df))
    VALIDATOR.generate_report()
    VALIDATOR.generate_action()
    VALIDATOR.decide_action()

    corrected_df = VALIDATOR.take_action(maven_df)

    return corrected_df


def report_missing_values(maven_df):

    return input_validation.check_missing(maven_df)


def report_duplicate_values(maven_df):

    return input_validation.check_duplicate(maven_df,COLUMN_DUPLICATE_CHECK)


def report_label_column_format(maven_df):

    return input_validation.validator_column_wise(maven_df, 0,[c.LABEL],
                              [input_validation.check_label_column_format])


def report_formula_column_format(maven_df):

    return input_validation.validator_column_wise(maven_df, 0,[c.FORMULA],
                              [input_validation.check_formula_is_correct])


def report_label_in_formula(maven_df):

    return input_validation.validator_for_two_column(
            maven_df, c.LABEL, c.FORMULA,
            input_validation.check_label_in_formula)


def report_intensity_values(maven_df):

    sample_columns = get_sample_column(maven_df)
    return input_validation.validator_column_wise(maven_df, 0, sample_columns,
                              [input_validation.check_intensity_value])


def get_validation_logs():

    return VALIDATOR.generate_warning_error_list_of_strings()


def get_extracted_isotracer(label):

    return label.split('-label-')[0]


def get_extraced_isotracer_df(maven_df):

    return maven_df[c.LABEL].apply(get_extracted_isotracer)


def get_isotracer_dict(maven_df):

    isotracer_df = get_extraced_isotracer_df(maven_df)
    return isotracer_df[ISOTRACER_COLUMN].value_counts().to_dict()


def get_merge_df(maven_df,metadata_df):

    if metadata_df:
        return maven_merge_dfs(maven_df,metadata_df)
    else:
        return convert_inputdata_to_stdfrom(maven_df)



def read_maven_file(maven_file_path, metadata_path):
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

    if input_validation.validate_input_file(maven_file_path):
        input_maven_df = dataframe_validator.read_input_file(maven_file_path)
    else:
        return input_validation.get_df(), None, None

    if metadata_path:
        metadata_df = get_metadata_df(metadata_path)
        maven_df = filtered_data_frame(input_maven_df,metadata_df)
    else:
        metadata_df = None
        maven_df = input_maven_df

    corrected_maven_df = get_corrected_maven_df(maven_df)

    validation_logs = get_validation_logs()

    if not validation_logs[con.VALIDATION_ERROR]:
        isotracer_dict = get_isotracer_dict(corrected_maven_df)
        merged_df = get_merge_df(corrected_maven_df,metadata_df)
        return merged_df, validation_logs, isotracer_dict
    else:
        return corrected_maven_df,validation_logs,None





