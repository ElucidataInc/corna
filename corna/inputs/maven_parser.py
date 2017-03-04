import pandas as pd

from collections import namedtuple

from column_conventions import maven as maven_constants
from corna import constants as con
from corna import input_validation
from corna import dataframe_validator
from corna.custom_exception import NoIntersectionError
from corna.helpers import merge_two_dfs, create_dict_from_isotope_label_list
from corna.helpers import chemformula_schema, check_column_headers
from corna.validation_report_class import ValidationReport

MavenKey = namedtuple('MavenKey', 'name formula')

REQUIRED_COLUMNS_MAVEN = [maven_constants.NAME, maven_constants.LABEL,
                          maven_constants.FORMULA]
REQUIRED_COLUMNS_MAVEN_METADATA = [maven_constants.SAMPLE]

LOGS = {}
ISOTRACER = []
COLUMN_DUPLICATE_CHECK = [[maven_constants.NAME, maven_constants.LABEL]]


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
                            left_on=con.VAR_COL, right_on=maven_constants.SAMPLE)
    except KeyError:
        raise KeyError(maven_constants.SAMPLE + ' column not found in metadata')

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
    df[con.PARENT_COL] = df[maven_constants.NAME]
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
    fixed_cols = [maven_constants.NAME, maven_constants.LABEL, maven_constants.FORMULA]
    col_headers = df1.columns.tolist()
    check_column_headers(col_headers, fixed_cols)
    melt_cols = [x for x in col_headers if x not in fixed_cols]

    # try:
    long_form = pd.melt(df1, id_vars=fixed_cols, value_vars=melt_cols)
    # except KeyError():
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
            x[maven_constants.NAME], x[maven_constants.FORMULA]), axis=1)
    except KeyError:
        raise KeyError('Missing columns in data')
    return df


def convert_std_label_key_to_maven_label(df):
    # TODO: File format change should lead to removal
    # of these fucntions
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
                    num_string = num_string + '-' + str(num_iso)
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


def get_intersection(first_set, second_set):
    """
     This function returns the intersection of two sets.
    """
    return list(first_set.intersection(second_set))


def get_column_names_set(df):
    """
    This function returns set of column headers in df.
    """
    return set(df.columns.values.tolist())


def get_unique_column_value(df, column):
    """
    This function return set of unique values in column
    """
    return set(df[column].tolist())


def drop_duplicate_rows(df, column):
    """
    This function drops the duplicate row in the given column of given
    df.
    """
    return df.drop_duplicates(column)


def get_metadata_df(metadata_path):
    """
    This function converts metadata file into df. It also validates
    the input file. If the validation fails it returns a empty df.
    :param metadata_path:absolute path of metadata info file
    :return: df of input metadata file
    """
    if check_basic_validation(metadata_path):
        metadata_df = get_df_frm_path(metadata_path)
    else:
        metadata_df = get_df_frm_path()

    if input_validation.validate_df(metadata_df, REQUIRED_COLUMNS_MAVEN_METADATA):
        return metadata_df


def get_sample_column(maven_df):
    """
    This function will extract out sample column headers
    from the maven df and returns in the form of list.
    :param maven_df: maven dataframe
    :return: sample column headers in the data frame
    """
    return [column for column in list(maven_df)
            if column not in REQUIRED_COLUMNS_MAVEN]


def get_validator_cls_obj(df, fn_lst):
    """
    This function creates instance of ValidationReport, then
    append all the reports which are generated after validation.
    It then return the class instance.
    :param df: df on which validation check is to be performed
    :param fn_lst: list of validation fn
    :return:df_validator: class instance of ValidationReport
    """
    df_validator = ValidationReport()

    for each_fn in fn_lst:
        df_validator.append_df_to_global_df(each_fn(df))

    return df_validator


def get_validation_fn_lst():
    """
    This function returns list of all the validation function for
    a df.
    """
    list = [report_missing_values, report_duplicate_values,
            report_label_column_format, report_label_in_formula,
            report_formula_column_format, report_intensity_values]
    return list


def report_missing_values(maven_df):
    return input_validation.check_missing(maven_df)


def report_duplicate_values(maven_df):
    return input_validation.check_duplicate(maven_df, 0, COLUMN_DUPLICATE_CHECK)


def report_label_column_format(maven_df):
    return input_validation.validator_column_wise(maven_df, 0,
                    [maven_constants.LABEL],[input_validation.check_label_column_format])


def report_formula_column_format(maven_df):
    return input_validation.validator_column_wise(maven_df, 0,
                [maven_constants.FORMULA],[input_validation.check_formula_is_correct])


def report_label_in_formula(maven_df):
    return input_validation.validator_for_two_column(
        maven_df, maven_constants.LABEL, maven_constants.FORMULA,
        input_validation.check_label_in_formula)


def report_intensity_values(maven_df):
    sample_columns = get_sample_column(maven_df)
    return input_validation.validator_column_wise(maven_df, 0,
                    sample_columns, [input_validation.check_intensity_value])


def get_validation_logs(validator):
    """
    This function returns logs of validation.
    :param validator: class instnce of ValidationReport
    :return: logs of all the validation checks
    """
    return validator.generate_warning_error_list_of_strings()


def get_extracted_isotracer(label):
    """
    This function takes label as an argumnet and returns the
    iso-tracer present in label. This helps in counting iso-tracer
    present in label column value.
    for ex: label = 'C13N15-label-1-2
            returns = 'C13N15
    :param label: label column value
    :return: extracted iso-tracer value
    """
    if label == con.UNLABELLED_LABEL:
        return 'C13N15'
    else:
        return label.split('-label-')[0]


def get_extraced_isotracer_df(maven_df):
    """
    This function extract iso-tracer information of
    all the values of label column.
    :param maven_df: df whose iso-tracer needs to get extracted
    :return: extracted iso-tracers for each label column value
    """
    return maven_df[maven_constants.LABEL].apply(get_extracted_isotracer)


def get_isotracer_dict(maven_df):
    """
    This function counts the iso-tracer in label column of
     the maven df. Dict with isotracer as key and its number as value
     is returned.
    :param maven_df: maven_df whose iso-tracer needs to be counted
    :return: dict of iso-tracer and its number
    """
    isotracer_df = get_extraced_isotracer_df(maven_df)
    return isotracer_df.value_counts().to_dict()


def check_df_empty(df):
    return df.empty


def get_merge_df(maven_df, metadata_df):
    """
    This function merge the metadata_df with maven_df. If metadata_df
    is not present it converts the maven df in long format (standard format)
    :param mave_df: df of raw maven input file
    :param metadata_df: df of metadata info file
    :return merge_df: std wide form df
    """
    if check_df_empty(metadata_df):
        return convert_inputdata_to_stdfrom(maven_df)
    else:
        return maven_merge_dfs(maven_df, metadata_df)


def check_error_present(logs):
    """
    This function checks if any error is present in the validation
    logs.
    :param logs: validation logs after all the validation checks
    :return: Boolean True if error is present
    """

    if logs[con.VALIDATION_ERROR]:
        return True
    else:
        return False


def check_basic_validation(path):
    """
    This function performs basic validation check of the input file.
    """
    return input_validation.validate_input_file(path)


def get_df_frm_path(path=None):
    """
    This function converts input file into pandas df. If no path
    is given it returns a empty df.
    :param path: path of input file.
    :return:converted df
    """
    if path:
        return dataframe_validator.read_input_file(path)
    else:
        return pd.DataFrame()


def get_corrected_maven_df(maven_df):
    """
    This function performs validation check on df and return
    corrected df i.e. df with corrected values. The logs of
    all the validation function with applied action on warnings
    is also generated.
    :param maven_df: df on which validation is to be performed
    :return: corrected_df: df after validation check
    :return: logs : logs of all the validation checks
    """

    validation_function_list = get_validation_fn_lst()
    validator = get_validator_cls_obj(maven_df, validation_function_list)

    validator.generate_report()
    validator.generate_action()
    validator.decide_action()

    corrected_df = validator.take_action(maven_df)
    logs = get_validation_logs(validator)
    return corrected_df, logs


def filtered_data_frame(maven_df, metadata_df):
    """
    This function filters maven df column according to the
    sample present in metadata df. If there is no intersection
    between the two df it rises an error.

    :param maven_df: maven df which needs to be filtered
    :param metadata_df:metadata df whcih contains info about sample
    :return: filtered maven df according to the sample in metadata_df
    """
    filtered_meta_df = drop_duplicate_rows \
        (metadata_df, REQUIRED_COLUMNS_MAVEN_METADATA)

    metadata_sample_column_set = get_unique_column_value \
        (filtered_meta_df, maven_constants.SAMPLE)

    maven_sample_list = get_column_names_set(maven_df)

    intersection_sample_list = get_intersection \
        (maven_sample_list, metadata_sample_column_set)

    if intersection_sample_list:
        maven_data_frame_column = REQUIRED_COLUMNS_MAVEN + intersection_sample_list
        filtered_maven_df = maven_df[maven_data_frame_column]
    else:
        raise NoIntersectionError
    return filtered_maven_df


def read_maven_file(maven_file_path, metadata_path):
    """
    This function reads maven and metadata file, convert it to df and
    checks for validation of files. If validation does not raise any
    error it returns mergedf with logs and iso-tracer data.
    :param maven_file_path: absolute path of maven raw file
    :param maven_sample_metadata_path: absolute path of metadatafile
    :return: mergedf : merge df of Maven and Metadata File
             logs: dictionary of errors and warnings
             iso-tracer : dictionary of iso-tracer details
    """

    if check_basic_validation(maven_file_path):
        input_maven_df = get_df_frm_path(maven_file_path)
    else:
        return get_df_frm_path(), None, None

    if metadata_path:
        metadata_df = get_metadata_df(metadata_path)
        maven_df = filtered_data_frame(input_maven_df, metadata_df)
    else:
        metadata_df = get_df_frm_path()
        maven_df = input_maven_df
    corrected_maven_df, validation_logs = get_corrected_maven_df(maven_df)
    if not check_error_present(validation_logs):
        isotracer_dict = get_isotracer_dict(corrected_maven_df)
        merged_df = get_merge_df(corrected_maven_df, metadata_df)
        return merged_df, validation_logs, isotracer_dict
    else:
        return corrected_maven_df, validation_logs, None
