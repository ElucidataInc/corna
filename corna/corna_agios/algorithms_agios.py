
import numpy as np
from numpy.linalg import pinv

import corna.helpers as hl
import corna.file_parser as fp
import corna.isotopomer as iso


def corr_matrix(iso_tracer, no_atom_tracer, na_dict):
    """
    This function creates a correction matrix using correction vector or mass distribution vector
    by convolving the correction vector over natural abundance of isotopic tracer elements. This
    correction matrix is used to correct input intensity values.
    Args:
        iso_tracer : List of isotopic tracer elements
        na_dict : Dictionary of natural abundance values
        no_atom_tracer : no of atoms of isotopic tracer
        correction_vector : mass distribution vector
    Returns:
        correction_matrix: matrix to be used for correcting intensities
    """

    correction_matrix = np.zeros((no_atom_tracer+1, no_atom_tracer+1))

    el_pur = [0, 1]

    for i in range(no_atom_tracer+1):

        column = [1.]

        for na in range(i):
            column = np.convolve(column, el_pur)[:no_atom_tracer+1]
        for nb in range(no_atom_tracer-i):
            try:
                column = np.convolve(column, na_dict[iso_tracer])[:no_atom_tracer+1]
            except KeyError:
                raise KeyError('Element not found in Natural Abundance dictionary', iso_tracer)
        correction_matrix[:, i] = column

    return correction_matrix


def matrix_multiplication(correction_matrix, intensities):
    """
    This function multiplies the inverse of correction matrix with the intensities
    vector

    Args:
        correction_matrix
        intensities : list of intensities
    Returns:
        corrected_intensites : list of corrected intensities after matrix multiplication
    """

    matrix = np.array(correction_matrix)
    mat_inverse = pinv(matrix)
    inten_trasp = np.array(intensities).transpose()

    try:
        corrected_intensites = np.matmul(mat_inverse, inten_trasp)
    except ValueError:
        raise ValueError('Matrix size = ' + str(len(mat_inverse)) + ' and intensities = ' \
         + str(len(inten_trasp)) + ' Length does not match, \
            hence cant be multiplied')

    return corrected_intensites


def multi_label_matrix(na_dict, formula_dict, eleme_corr_list):
    """
    This function creates a correction matrix for multiple tracers using kronecker
    product of matrices of different elements. Numpy kron function is used to get the product

    Args:
        na_dict : Dictionary of natural abundance values
        formula_dict : Dictionary of number of atoms of chemical formula
        eleme_corr_list : list of elements to be corrected (isotracers + indistinguishable elements)

    Returns:
        correction_matrix : resultant correction matrix for multiple tracers, obtained after kronecker
                            product of matrices of different elements

    """

    correction_matrix = [1.]

    for trac in eleme_corr_list:
        try:
            no_atom_tracer = formula_dict[trac]
        except KeyError:
            raise KeyError('Element ' + str(trac) +
                           ' given for correction not found in chemical formula')

        matrix_tracer = corr_matrix(str(trac), no_atom_tracer, na_dict)
        correction_matrix = np.kron(correction_matrix, matrix_tracer)

    return correction_matrix


def multi_label_correc(na_dict, formula_dict, eleme_corr_list, intensities_list):
    """
    This function does matrix multiplication of multi label correction matrix
    with intensities_list by calling other functions
    """
    M = multi_label_matrix(na_dict, formula_dict, eleme_corr_list)
    icorr = matrix_multiplication(M, intensities_list)

    return icorr


def fragmentsdict_model(merged_df):
    """
    This function converts the dataframe into fragment dictionary model
    Args:
        merged_df : dataframe with input + metadata file
    Returns:
        fragments_dict : Dictionary of the form, example : {'Aceticacid_C13_1':
        [Fragment object, {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
    """
    fragments_dict = {}
    std_model_mvn = fp.standard_model(merged_df)

    for metabolite_name, label_dict  in std_model_mvn.iteritems():
        fragments_dict[metabolite_name] = {}
        for label, data in label_dict.iteritems():
            fragments_dict[metabolite_name].update(
                iso.bulk_insert_data_to_fragment(metabolite_name, {label: data}))

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
                           for sample in info[1].keys()))

    return sample_list



def samp_label_dcit(iso_tracers, fragments_dict):
    """
    This function returns dictionary of the form { sample1: { 0 : val, 1: value },
    sample2: {}, ...}

    Args:
        iso_tracers : list of isotopic tracers
        fragments_dict : Dictionary of the form, {'Metabname_label':
        [Fragment object, {'sample_name': intensity}, label/unlabe bool, metabname]

    Returns:
        samp_lab_dict : label dictionary corresponding to each sample
    """
    sample_list = unique_samples_for_dict(fragments_dict)
    frag_info = fragments_dict.values()
    samp_lab_dict = {}

    for samp in sample_list:
        dict_s = {}
        for info in frag_info:
            lab_num = ()
            for isotopes in iso_tracers:
                try:
                    lab_num = lab_num + (info[0].get_num_labeled_atoms_isotope(str(isotopes)),)
                except KeyError:
                    raise KeyError('Isotope not present in chemical formula', info[0])
            dict_s[lab_num] = info[1][samp]
        samp_lab_dict[samp] = dict_s

    return samp_lab_dict


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
    #all elements of fragments dictionary belong to same metabolite, so same formula
    fragment_info = fragments_dict.values()[0]
    formula_dict = fragment_info[0].get_formula()

    return formula_dict


def get_atoms_from_tracers(iso_tracers):
    """
    This function return the atoms of the isotopic tracer in the form of
    a list
    Args:
        iso_tracers : list of isotopic tracers ['C13', 'N15']
    Returns:
        trac_atoms : list of atoms of isotopic tracers ['C', 'N']
    """
    trac_atoms = []

    for i in range(0, len(iso_tracers)):
        element = hl.get_isotope_element(iso_tracers[i])
        trac_atoms.append(element)

    return trac_atoms


def check_labels_corrdict(correc_inten_dict):
    """
    This function gives the list of unique samples from dictionary of corrected
    intensity model
    Args:
        correc_inten_dict : fragment dictionary model of corrected isntensities
    Returns:
        lab_key_list : list of unique label tuple from dictionary
    """
    lab_corr_int_dict = correc_inten_dict.values()
    lab_key_list = []

    for un_new in lab_corr_int_dict:
        lab_key_list.extend(un_new.keys())
    lab_key_list = list(set(lab_key_list))

    return lab_key_list


def label_sample_dict(label_list, correc_inten_dict):
    """
    This function returns a dictionary with outer key as number of labeled tracer
    as tuple and dictionary with sample name amd its value

    Args:
        label_list : list of unique labels
        correc_inten_dict : fragment dictionary model of corrected intensities
    Returns:
        lab_samp_dict : dictionary label as outer key and sample dictionary
                        corresponding to each label
    """

    lab_samp_dict = {}

    for labs in label_list:
        sample_dict = {}
        for sample in correc_inten_dict.keys():
            try:
                intensity = correc_inten_dict[sample][labs]
            except KeyError:
                raise KeyError('samples and labels not found'
                               ' in corrected intensities dictionary', sample, labs)
            sample_dict[sample] = np.array([intensity])
        lab_samp_dict[labs] = sample_dict

    return lab_samp_dict


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
            lab_tup_key = (frag_info[0].get_num_labeled_atoms_isotope(iso_tracers[0]),)

        elif len(iso_tracers) > 1:
            try:
                lab_tup_key = []
                for isotope in iso_tracers:
                    lab_tup_key.append(frag_info[0].get_num_labeled_atoms_isotope(isotope))
                lab_tup_key = tuple(lab_tup_key)
            except KeyError:
                raise KeyError('Name, Formula or Sample not found in input data file')

        nacorr_fragment_dict[frag_name] = [frag_info[0], lab_samp_dict[lab_tup_key],
                                           frag_info[2], frag_info[3]]

    return nacorr_fragment_dict



def eleme_corr_to_list(iso_tracers, eleme_corr):
    """
    This function creates a list of elements to be corrected for multi tracer na correction.
    It includes the tracer elements along with the indistinguishable species.
    """
    trac_atoms = get_atoms_from_tracers(iso_tracers)

    eleme_corr_list = []

    for atoms in trac_atoms:
        eleme_corr_list.append([atoms])
        if atoms in eleme_corr.keys():
            eleme_corr_list.append(eleme_corr[atoms])

    return sum(eleme_corr_list, [])



def input_intens_list(num_label_comb, label_dict, indist_el_position):
    """
    This function filters the tuple list for multi tracer na correction and appends
    zero value to the combinations not present in the input data

    Args:
        num_label_comb : list of tuples with all possible combinations of the number of elements
                     to be corrected. For example, In C5H10NO2S, if element to be corrected are
                     C,H,N then this list will be [(0,0,0), (1,0,0), (0,0,1).....so on..(5,10,1)]

        label_dict : dictionary of labels and intensity value from input data. This dictionary has
                     keys for isotracers (C,N) , {(0,0): inten1, (1,0) : inten2 ..so on}

        indist_el_position : position of tuple to be ignored for filtering. This position accounts for the
                    position of indistinguishable species, so for example from tuple (C,H,N) =
                    (1,0,0), position 1 is ignored to give tuple for isotracers (C,N) = (1,0)

    Returns:
        input_intensities : list of intensites with zeroes appended at positions for which
                        combinations are not found in the input data.This intensites vector
                        is used to multiply with the resultant correction matrix for multi tracer.
                        Here labels for which intensities are not given in the input data, ie for
                        indistinguishable species, intensities are taken as zero.
    """
    input_intensities = []

    for tuples in num_label_comb:
        tuple_l = list(tuples)
        filter_indist_el = [tuple_l[x] for x in indist_el_position]
        if sum(filter_indist_el) == 0:
            tracer_tup_key = tuple([tuple_l[x] for x in range(0, len(tuple_l))
                                    if x not in indist_el_position])
            if tracer_tup_key in label_dict.keys():
                input_intensities.append(label_dict[tracer_tup_key][0])
            else:
                input_intensities.append(0)
        else:
            input_intensities.append(0)

    return input_intensities



