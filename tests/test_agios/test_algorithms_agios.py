import pytest
import numpy as np
import pandas as pd

import corna.helpers as hl
from corna.model import Fragment
from corna import isotopomer as iso
from corna.corna_agios import algorithms_agios as algo


iso_tracer = ['C13']

formula_dict = {'C':2, 'H':4, 'O':2}

no_atom_tracer = 2

eleme_corr = {}

na_dict = {'H':[0.98,0.01,0.01], 'S': [0.922297, 0.046832, 0.030872], 'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}

df = pd.DataFrame({'Name': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
   'Parent': {0: 'Acetic', 1: 'Acetic', 2: 'Acetic'}, \
    'Label': {0: 'C12 PARENT', 1: 'C13-label-1', 2: 'C13-label-2'}, \
     'Intensity': {0: 0.3624, 1: 0.040349999999999997, 2: 0.59724999999999995}, \
      'Formula': {0: 'H4C2O2', 1: 'H4C2O2', 2: 'H4C2O2'}, \
      'info2': {0: 'culture_1', 1: 'culture_1', 2: 'culture_1'}, \
       'Sample Name': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1'}})

correc_inten_dict = {'sample_1': {(0, 1): np.array([ 0.0619]), (0, 0): np.array([ 0.2456]), \
     (3, 0): np.array([ 0.0003]), (3, 1): np.array([ 0.0001]), (2, 1): np.array([ 0.0015]), \
      (2, 0): np.array([ 0.0071]), (5, 0): np.array([ 0.]), (5, 1): np.array([ 0.60045]), \
      (1, 0): np.array([ 0.06665]), (4, 1): np.array([ 0.]), (1, 1): np.array([ 0.0164]), \
       (4, 0): np.array([ 0.])}}

acetic_frag = Fragment('Acetic','H4C2O2',label_dict={'C13':0})
fragments_dict = {'Acetic_C13_0': [acetic_frag,{'sample_1': np.array([ 0.3624])}, True, 'Acetic']}

label_list = [(0, 1), (0, 0), (3, 0), (3, 1), (2, 1), (2, 0), (5, 0), \
                 (5, 1), (1, 0), (4, 1), (1, 1), (4, 0)]


def test_corr_matrix():
    iso_tracer = 'C'
    with pytest.raises(KeyError):
        c_matrix = algo.corr_matrix(iso_tracer, no_atom_tracer, na_dict)


def test_matrix_multiplication():
    correction_matrix = [[0,1], [2,3]]
    intensities = [1]
    with pytest.raises(ValueError):
        multiply = algo.matrix_multiplication(correction_matrix, intensities)


def test_multi_label_matrix():
    eleme_corr_list = ['S']
    with pytest.raises(KeyError):
        multi_lab_cm = algo.multi_label_matrix(na_dict, formula_dict, eleme_corr_list)


def test_formula_dict():
    assert algo.formuladict(fragments_dict) == {'C':2, 'H':4, 'O':2}


def test_tracer_atoms():
    out_atom = ['C']
    atoms = algo.get_atoms_from_tracers(iso_tracer)
    assert atoms == out_atom


def test_check_labels_corrdict():
    lab_list = algo.check_labels_corrdict(correc_inten_dict)
    assert lab_list == label_list


def test_label_sample_dict():
    out_label_samp_dc = {(0, 1): {'sample_1': np.array([[ 0.0619]])}, \
    (0, 0): {'sample_1': np.array([[ 0.2456]])}, (3, 0): {'sample_1': np.array([[ 0.0003]])}, \
    (3, 1): {'sample_1': np.array([[ 0.0001]])}, (2, 1): {'sample_1': np.array([[ 0.0015]])}, \
    (2, 0): {'sample_1': np.array([[ 0.0071]])}, (5, 0): {'sample_1': np.array([[ 0.]])}, \
    (5, 1): {'sample_1': np.array([[ 0.60045]])}, (1, 0): {'sample_1': np.array([[ 0.06665]])}, \
    (4, 1): {'sample_1': np.array([[ 0.]])}, (1, 1): {'sample_1': np.array([[ 0.0164]])}, \
    (4, 0): {'sample_1': np.array([[ 0.]])}}
    lab_samp_dict = algo.label_sample_dict(label_list, correc_inten_dict)
    assert lab_samp_dict == out_label_samp_dc


def test_eleme_corr_list():
    eleme_corr = {'C':['H']}
    el_list = algo.eleme_corr_to_list(iso_tracer, eleme_corr)
    assert el_list == ['C', 'H']


def test_input_intens_list():
    tuple_list = [(0,0,0), (0,0,1), (2,1,2)]
    value_dict = {(0, 1): np.array([1]), (0, 0): np.array([2])}
    positions = [1]
    out = [2,1,0]
    result = algo.input_intens_list(tuple_list, value_dict, positions)
    assert out == result