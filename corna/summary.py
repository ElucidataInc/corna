import pandas as pd


def summary_raw_intensity_msms(raw_intensity_df):
    summary_list = []
    dict1 = {'Number of rows': raw_intensity_df['Original Filename'].count(),
             'Number of samples': len(raw_intensity_df['Original Filename'].unique()),
             'Number of cohorts': len(raw_intensity_df['Sample Name'].unique()),
             'Number of metabolites': len(raw_intensity_df['Component Name'].unique())}
    dict_label_list = dict1.keys()
    for i in range(0, len(dict_label_list)):
        dict2 = {}
        dict2['label'] = dict_label_list[i]
        dict2['value'] = dict1[dict_label_list[i]]
        summary_list.append(dict2)
    return summary_list


def summary_metadata_mq(metadata_mq_df):
    summary_list = []
    dict1 = {'Number of fragments': metadata_mq_df['Component Name'].count(),
             'Number of unlabeled fragments': len(metadata_mq_df['Unlabeled Fragment'].unique()),
             'isotopic tracer': list((metadata_mq_df['Isotopic Tracer'].unique()))
            }
    dict_label_list = dict1.keys()
    for i in range(0, len(dict_label_list)):
        dict2 = {}
        dict2['label'] = dict_label_list[i]
        dict2['value'] = dict1[dict_label_list[i]]
        summary_list.append(dict2)
    return summary_list


def summary_sample_metadata(metadata_std_df):
    summary_list = []
    dict1 = {'Number of background samples': len(metadata_std_df['Background Sample'].unique()),
             'Fields in metadata': ", ".join(list(metadata_std_df)),
            }
    dict_label_list = dict1.keys()
    for i in range(0, len(dict_label_list)):
        dict2 = {}
        dict2['label'] = dict_label_list[i]
        dict2['value'] = dict1[dict_label_list[i]]
        summary_list.append(dict2)
    return summary_list


def summary_raw_intensity_lcms(raw_intensity_df):
    summary_list = []
    dict1 = {'Number of metabolites': len(raw_intensity_df['Name'].unique()),
             'Number of samples': (len(list(raw_intensity_df)) - 3),
             'Number of blank intensity cells': raw_intensity_df.isnull().values.ravel().sum(),
             #'Number of labelled elements': len(raw_intensity_df['Component Name'].unique()),
             'Number of rows': raw_intensity_df['Label'].count()}
    dict_label_list = dict1.keys()
    for i in range(0, len(dict_label_list)):
        dict2 = {}
        dict2['label'] = dict_label_list[i]
        dict2['value'] = dict1[dict_label_list[i]]
        summary_list.append(dict2)
    return summary_list

def lcms_metadata(meta_df):
    summary_list = []
    dict1 = {'Fields in metadata': ", ".join(list(meta_df)),
             'Number of rows in metadata': list(meta_df[[0]].count())[0],
             }
    dict_label_list = dict1.keys()
    for i in range(0, len(dict_label_list)):
        dict2 = {}
        dict2['label'] = dict_label_list[i]
        dict2['value'] = dict1[dict_label_list[i]]
        summary_list.append(dict2)
    return summary_list

