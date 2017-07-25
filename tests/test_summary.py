import os

import pandas as pd
import pytest

from corna import summary as sm


def test_create_list_of_dict():
    list_of_field = ['a', 'b']
    fields_dict = {'a': 1, 'b': 2}
    assert sm.create_list_of_dict(list_of_field, fields_dict) == [{'value': 1, 'label': 'a'},
                                                                  {'value': 2, 'label': 'b'}]


def test_summary_raw_msms():
    raw_df = pd.DataFrame({'Original Filename': [1, 2],
                           'Sample Name': ['a', 'b'],
                           'Component Name': ['aa', 'bb']})
    assert sm.summary_raw_msms(raw_df) == {'Number of cohorts': 2,
                                           'Number of metabolites': 2,
                                           'Number of rows': 2,
                                           'Number of samples': 2}


def test_summary_meta_msms_isotopic():
    meta_df = pd.DataFrame({'Component Name': [1, 2],
                            'Unlabeled Fragment': ['a', 'b'],
                            'Isotopic Tracer': ['C13','C13']})
    assert sm.summary_meta_msms(meta_df) == {'isotopic tracer': 'C13',
                                             'Number of fragments': 2,
                                             'Number of unlabeled fragments': 2}


def test_summary_meta_msms_no_isotopic():
    meta_df = pd.DataFrame({'Component Name': [1, 2],
                            'Unlabeled Fragment': ['a', 'b']})
    assert sm.summary_meta_msms(meta_df) == {'Number of fragments': 2,
                                             'Number of unlabeled fragments': 2}


def test_summary_smp_msms():
    meta_df = pd.DataFrame({'Background Sample': [1, 2],
                            'cohort name': ['a', 'b']})
    assert sm.summary_smp_msms(meta_df) == {'Fields in metadata': 'Background Sample, cohort name',
                                             'Number of background samples': 2}


def test_summary_raw_lcms():
    raw_df = pd.DataFrame({'Label': [1, 2],
                           'Name': ['a', 'b'],
                           'smp1': ['aa', 'bb']})
    assert sm.summary_raw_lcms(raw_df) == {'Number of blank intensity cells': 0,
                                           'Number of metabolites': 2,
                                           'Number of rows': 2,
                                           'Number of samples': 0}


def test_summary_meta_lcms():
    raw_df = pd.DataFrame({'cohort name': [1, 2],
                           'sample name': ['a', 'b']})
    assert sm.summary_meta_lcms(raw_df) == {'Fields in metadata': 'cohort name, sample name',
                                            'Number of rows in metadata': 2}


def test_create_summary():
    raw_df = pd.DataFrame({'Original Filename': [1, 2],
                           'Sample Name': ['a', 'b'],
                           'Component Name': ['aa', 'bb']})
    df_type = 'INPUT DATA'
    assert sm.create_summary(raw_df, df_type) == [{'label': 'Number of samples', 'value': 2},
                                                  {'label': 'Number of rows', 'value': 2},
                                                  {'label': 'Number of metabolites', 'value': 2},
                                                  {'label': 'Number of cohorts', 'value': 2}]

