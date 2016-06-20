import pandas as pd
import config as conf


def convert_dict_df(nest_dict, parent = True):
    """
    This function convert the fragment dictionary model in dataframe
    """
    print 'nest dict'
    print nest_dict
    df_list = []
    for frag_name, label_dict in nest_dict.iteritems():
        df, df_list = lists_labeldict(df_list, frag_name, label_dict)
    if parent == True:
        final_df = pd.concat(df_list)
    else:
        final_df = df
    final_df.rename(columns={"level_0":conf.LABEL_COL, 0:conf.SAMPLE_COL, 1:conf.INTENSITY_COL}, inplace=True)
    final_df.pop('level_1')
    print 'df'
    print final_df
    return final_df


def lists_labeldict(df_list, frag_name, label_dict):
    """
    This function extracts lists of metabolite name, formula, parent from label dictionary
    model
    """
    name = []
    formula = []
    parent = []
    lab = []
    frames = []

    for key, value in label_dict.iteritems():
        tup = []
        for k, v in value.iteritems():
            for intensity in v:
                tup.append((k, intensity))
                name.append(frag_name[0])
                formula.append(frag_name[1])
                if parent == True:
                    parent.append(frag_name[2])
        lab.append(key)
        frames.append(pd.DataFrame(tup))
        df = pd.concat(frames, keys=lab).reset_index()
        df[conf.NAME_COL] = name
        df[conf.FORMULA_COL] = formula
        if parent == True:
            df[conf.PARENT_COL] = parent
            df_list.append(df)
    return (df, df_list)



