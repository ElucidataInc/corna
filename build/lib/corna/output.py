import pandas as pd


def convert_dict_df(nest_dict, parent = True):

    new_dict = {}
    df_list = []
    for frag_name, label_dict in nest_dict.iteritems():
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
            df['Name'] = name
            df['Formula'] = formula
            if parent == True:
                 df['parent'] = parent
                 df_list.append(df)
    if parent == True:
        final_df = pd.concat(df_list)
    else:
        final_df = df
    final_df.rename(columns={"level_0":"Label", 0:"Sample Name", 1:'Intensity'}, inplace=True)
    final_df.pop('level_1')
    return final_df


