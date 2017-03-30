
import numpy as np
from numpy.linalg import pinv
import pandas as pd

from ... inputs.maven_parser import frag_key
from ... helpers import get_isotope_element
from ... data_model import standard_model
from ... isotopomer import bulk_insert_data_to_fragment, Infopacket

def make_expected_na_matrix(N, pvec):
    """for a single labeled element, create the matrix M
    such that Mx=y where x is the actual distribution of input labels
    and y is the expected distribution of intensities with natural abundance

    N: number of atoms of this element
    pvec: expected isotopic distribution (e.g. [0.99,0.01])"""

    max_label=1+(N*(len(pvec)-1))
    correction_matrix = np.zeros((max_label,N+1))
    for i in range(N+1):
        column = np.zeros(i+1)
        column[-1]=1.0
        for nb in range(N-i):
            column = np.convolve(column, pvec)
        column.resize(max_label)
        correction_matrix[:, i] = column
    return correction_matrix

def add_indistinguishable_element(M,n,pvec):
    """to a matrix M formed by make_expected_na_matrix, add additional expected
    intensity corresponding to natural abundance from elements with same isotopic mass shift

    M: previous matrix formed by make_expected_na_matrix
    n: number of atoms of new element
    pvec: expected isotopic distribution of new element (e.g. [0.99,0.01])"""
    max_label=(n*(len(pvec)-1))
    M_new=np.zeros((M.shape[0]+max_label,M.shape[1]))
    M_new[:M.shape[0],:]=M
    for i in range(M.shape[1]):
        for j in range(n):
            M_new[:,i]=np.convolve(M_new[:,i],pvec)[:M_new.shape[0]]
    #print M_new
    return M_new

def make_correction_matrix(trac_atom, formuladict, na_dict, indist_elems):
    """create matrix M such that Mx=y where y is the observed isotopic distribution
    and x is the expected distribution of input labels

    atom_bag: dict of element:number of atoms in molecule (e.g. {'C':2,'O':1,'H':6})
    label_elem: element with input labeling
    indist_elems: elements with identical mass shift
    na_dict: dict of element:expected isotopic distribution
    :TODO This function relates to issue NCT-247. Need to change the function
    in more appropriate way.
    """
    M = make_expected_na_matrix(formuladict.get(trac_atom,0), na_dict[trac_atom])
    for e in indist_elems:
        if e in formuladict:
            M = add_indistinguishable_element(M, formuladict[e], na_dict[e])
    return pinv(M)

def make_all_corr_matrices(isotracers, formula_dict, na_dict, eleme_corr):
    corr_mats = {}
    for isotracer in isotracers:
        trac_atom = get_isotope_element(isotracer)
        try:
            indist_list = eleme_corr[trac_atom]
        except KeyError:
            indist_list = []
        corr_mats[isotracer] = make_correction_matrix(trac_atom, formula_dict, na_dict, indist_list)
    return corr_mats

def fragmentsdict_model(merged_df, intensity_col):
    """
    This function converts the dataframe into fragment dictionary model
    Args:
        merged_df : dataframe with input + metadata file
    Returns:
        fragments_dict : Dictionary of the form, example : {'Aceticacid_C13_1':
        [Fragment object, {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
    """
    fragments_dict = {}
    frag_merge_df = frag_key(merged_df)
    std_model_mvn = standard_model(frag_merge_df, intensity_col)
    for metabolite_name, label_dict in std_model_mvn.iteritems():
        fragments_dict[metabolite_name] = {}
        for label, data in label_dict.iteritems():
            fragments_dict[metabolite_name].update(
                bulk_insert_data_to_fragment(metabolite_name, {label: data},  number=True))

    return fragments_dict


def unique_samples_for_dict(fragments_dict):
    """
    This function returns the list of samples from fragment dictionary model

    Args:
        fragments_dict : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': intensity}, label/unlabe bool, metabname]

    Returns:
        sample_list : returns list of samples from the dictionary
                      of the form ['sample_1']
    """

    sample_list = list(set(sample for info in fragments_dict.values()
                           for sample in info.data.keys()))

    return sample_list


def label_sample_df(iso_tracers, fragments_dict):
    """
    This function returns dataframe with isotracers as indices and samples
    as columns like:
    N15 C13 Sample1 Sample2
    0   0   0.21    0.98
    0   1   0.34    0.11
    1   0   0.87    0.34
    1   1   0.23    0.76

    Args:
        iso_tracers : list of isotopic tracers
        fragments_dict : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': intensity}, label/unlabe bool, metabname]

    Returns:
        samp_lab_df :
    """
    sample_list = unique_samples_for_dict(fragments_dict)
    frag_info = fragments_dict.values()
    sam_lab_df = pd.DataFrame(columns=iso_tracers + sample_list)

    i=0
    for info in frag_info:
        dict_s = {}
        for isotopes in iso_tracers:
            try:
                dict_s.update({isotopes: info.frag.get_num_labeled_atoms_isotope(str(isotopes))})
            except KeyError:
                raise KeyError(
                        'Isotope not present in chemical formula', info.frag)
        dict_s.update(info.data)
        sam_lab_df.loc[i] = pd.Series(dict_s)
        i=i+1

    sam_lab_df = sam_lab_df.set_index(iso_tracers)
    sam_lab_df.columns.name = 'Sample'
    return sam_lab_df

def formuladict(fragments_dict):
    """
    This function creates a formula dictionary from the chemical
    formula defined in the input data file
    Args:
        fragments_dict : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': intensity}, label/unlabe bool, metabname]
    Returns:
        formula_dict : dictionary of the form {C:2, H:4, O:2}
    """
    # all elements of fragments dictionary belong to same metabolite, so same
    # formula
    fragment_info = fragments_dict.values()[0]
    formula_dict = fragment_info.frag.get_formula()

    return formula_dict


def fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict):
    """
    This function creates a model of fragments dictionary on which model functions can
    applied

    Args:
        iso_tracers : list of isotopic tracers
        fragments_dict : dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
        lab_samp_dict : dictionary of the form {(0, 1): {'sample_1': 0.0619}....}
    Returns:
        nacorr_fragment_dict : fragment dictionary model

    """
    nacorr_fragment_dict = {}
    for frag_name, frag_info in fragments_dict.iteritems():

        if len(iso_tracers) == 1:
            lab_tup_key = frag_info.frag.get_num_labeled_atoms_isotope(iso_tracers[0])

        elif len(iso_tracers) > 1:
            try:
                lab_tup_key = []
                for isotope in iso_tracers:
                    lab_tup_key.append(
                        frag_info.frag.get_num_labeled_atoms_isotope(isotope))
                lab_tup_key = tuple(lab_tup_key)
            except KeyError:
                raise KeyError(
                    'Name, Formula or Sample not found in input data file')

        nacorr_fragment_dict[frag_name] = Infopacket(frag_info.frag, lab_samp_dict[lab_tup_key],
                                           frag_info.unlabeled, frag_info.name)
    return nacorr_fragment_dict
