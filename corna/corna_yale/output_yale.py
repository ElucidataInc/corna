import pandas as pd
import config_yale as conf
import ..helpers as hl


def convert_dict_df(nest_dict):
    """
    This function convert the fragment dictionary model in dataframe
    Args:
        nest_dict : dictionary of the form ('L-Methionine', 'C5H10NO2S'):
        {'C13_1': {'sample_1': array([  3.18407678e-07])}, 'C13_0': {'sample_1': array([ 0.48557866])}..}

    Returns:
        final_df : final dataframe
    """
    df_list = []
    for frag_name, label_dict in nest_dict.iteritems():
        df, df_list = lists_labeldict(df_list, frag_name, label_dict)

    final_df = pd.concat(df_list)

    final_df.rename(columns={
                        hl.LEVEL_0_COl:conf.LABEL_COL,
                        0:conf.SAMPLE_COL,
                        1:conf.INTENSITY_COL},
                    inplace=True)
    final_df.pop(hl.LEVEL_1_COL)

    return final_df


def lists_labeldict(df_list, frag_name, label_dict):
    """
    This function extracts lists of metabolite name, formula, parent from
    label dictionary model
    Args:
        df_list : list of dataframes to be combined

        frag_name : metabolite and its formula

        label_dict : dictionary with labels as keys adn intensity as intensalues

    Returns:
        (df, df_list) : final dataframe or list of dataframes to be appended
    """
    name = []
    formula = []
    parent = []
    lab = []
    frames = []

    for label, samp_dict in label_dict.iteritems():
        tup = []
        for samp, intens in samp_dict.iteritems():
            for intensity in intens:
                tup.append((samp, intensity))
                name.append(frag_name[0])
                formula.append(frag_name[1])
                parent.append(frag_name[2])
        lab.append(label)
        frames.append(pd.DataFrame(tup))
        df = pd.concat(frames, keys=lab).reset_index()
        df[conf.NAME_COL] = name
        df[conf.FORMULA_COL] = formula
        df[conf.PARENT_COL] = parent
        df_list.append(df)

    return (df, df_list)