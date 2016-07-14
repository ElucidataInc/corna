import numpy as np
import helpers as hl
from scipy import optimize
from numpy.linalg import pinv
import file_parser as fp
import isotopomer as iso




def excluded_elements(iso_tracer, formula_dict, eleme_corr):
    """
    This function gives a list of elements to be excluded for correction

    Args:
        iso_tracer : List of isotopic tracer elements

        formula_dict : Dictionary of number of atoms of chemical formula

        eleme_corr : Indistinguishable species to be considered for correction
                     along with isotopic tracers

    Returns:
        el_excluded : List of elements to be excluded for correction
    """
    el_excluded = []

    for key, value in formula_dict.iteritems():
        if iso_tracer in eleme_corr.keys():
            if key not in eleme_corr[iso_tracer]:
                el_excluded.append(key)

    return el_excluded


def corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict):
    """
    This function creates a correction matrix using correction vector or mass distribution vector
    by convolving the correction vector over natural abundance of isotopic tracer elements. This
    correction matrix is used to correct input intensity values.

    Args:
        iso_tracer : List of isotopic tracer elements

        formula_dict : Dictionary of number of atoms of chemical formula

        eleme_corr : Indistinguishable species to be considered for correction
                     along with isotopic tracers

        na_dict : Dictionary of natural abundance values

        no_atom_tracer : no of atoms of isotopic tracer

        correction_vector : mass distribution vector

    Returns:
        correction_matrix: matrix to be used for correcting intensities
    """

    el_excluded = excluded_elements(iso_tracer,formula_dict, eleme_corr)

    correction_matrix = np.zeros((no_atom_tracer+1, no_atom_tracer+1))

    el_pur = [0,1]

    for i in range(no_atom_tracer+1):

        column = [1.]

        for na in range(i):
            column = np.convolve(column, el_pur)[:no_atom_tracer+1]
        if el_excluded != iso_tracer:
            for nb in range(no_atom_tracer-i):
                try:
                    column = np.convolve(column, na_dict[iso_tracer])[:no_atom_tracer+1]
                except KeyError:
                    raise KeyError('Element not found in Natural Abundance dictionary', iso_tracer)
        correction_matrix[:,i] = column

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
            raise KeyError('Element ' + str(trac) + ' given for correction not found in chemical \
             formula')

        eleme_corr = {}

        matrix_tracer = corr_matrix(str(trac), formula_dict, eleme_corr, no_atom_tracer, na_dict)

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
        fragments_dict : Dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
    """
    fragments_dict = {}
    std_model_mvn = fp.standard_model(merged_df, parent = False)
    print 'std_model_mvn'
    print std_model_mvn
    #fragments_list = []

    for metabolite_name, label_dict  in std_model_mvn.iteritems():
        fragments_dict[metabolite_name] = {}
        for label, data in label_dict.iteritems():
            fragments_dict[metabolite_name].update(iso.bulk_insert_data_to_fragment(metabolite_name, {label:data}, mass=False, number=True, mode=None))

    print 'fragmentsdict_model'
    print fragments_dict

    return fragments_dict


def unique_samples_for_dict(merged_df):
    """
    This function returns the list of samples from fragment dictionary model

    Args:
        merged_df : dataframe with input + metadata file

    Returns:
        sample_list : returns list of samples from merged dataframe
                      of the form ['sample_1', 'sample_2',..]
    """
    fragments_dict = fragmentsdict_model(merged_df)
    universe_values = fragments_dict.values()
    print 'universe values'
    print universe_values
    sample_list = []

    for uv in universe_values:
        try:
            samples = uv[1].keys()
        except KeyError:
            #this doesn't raise error properly, samples referred before assignment
            raise KeyError('Missing samples in dataframe', samples)
        sample_list.extend(samples)

    sample_list = list(set(sample_list))

    return sample_list



def samp_label_dcit(iso_tracers, merged_df):
    """
    This function returns dictionary of the form { sample1: { 0 : val, 1: value },
    sample2: {}, ...}

    Args:
        iso_tracers : list of isotopic tracers

        merged_df : dataframe with input + metadata file

    Returns:
        samp_lab_dict : label dictionary corresponding to each sample
    """
    sample_list = unique_samples_for_dict(merged_df)
    fragments_dict = fragmentsdict_model(merged_df)
    universe_values = fragments_dict.values()
    print 'universe values'
    print universe_values
    samp_lab_dict = {}

    for s in sample_list:
        dict_s = {}
        for uv_new in universe_values:
            lab_num = ()
            for isotopes in iso_tracers:
                try:
                    lab_num = lab_num + (uv_new[0].get_num_labeled_atoms_isotope(str(isotopes)),)
                except KeyError:
                    raise KeyError('Labels not defined with chemical formula in input file')

            dict_s[lab_num] = uv_new[1][s]

        samp_lab_dict[s] = dict_s

    return samp_lab_dict


def formuladict(merged_df):
    """
    This function creates a formula dictionary from the chemical
    formula defined in the input data file

    Args:
        merged_df : dataframe with input + metadata file. It has
                    chemical formula in the form C2H4O2
    Returns:
        formula_dict : dictionary of the form {C:2, H:4, O:2}
    """
    fragments_dict = fragmentsdict_model(merged_df)
    formula_dict = {}

    for key, value in fragments_dict.iteritems():
        try:
            formula_dict =  value[0].get_formula()
        except KeyError:
            raise KeyError('Chemical formula not found in input file')

    return formula_dict


def get_atoms_from_tracers(iso_tracers):
    """
    This function return the atoms of the isotopic tracer in the form of
    a list

    Arg:
        iso_tracers : list of isotopic tracers ['C13', 'N15']

    Returns:
        trac_atoms : list of atoms of isotopic tracers ['C', 'N']
    """
    trac_atoms = []
    for i in range(0, len(iso_tracers)):
        element = hl.parse_polyatom(iso_tracers[i])[0]
        trac_atoms.append(element)
    return trac_atoms


def check_samples_ouputdict(correc_inten_dict):
    """
    This function gives the list of unique samples from dictionary of corrected
    intensity model

    Args:
        correc_inten_dict : fragment dictionary model of corrected isntensities

    Returns:
        inverse_sample : list of unique label tuple from dictionary
    """
    univ_new = correc_inten_dict.values()
    inverse_sample = []

    for un_new in univ_new:
        inverse_sample.extend(un_new.keys())
    inverse_sample = list(set(inverse_sample))

    return inverse_sample


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
    for inv in label_list:
        sample_dict = {}
        for sample_tr in correc_inten_dict.keys():
            try:
                k = correc_inten_dict[sample_tr][inv]
            except KeyError:
                raise KeyError('samples and labels not found in corrected intensities dictionary', sample_tr, inv)
            sample_dict[sample_tr] = np.array([k])
        lab_samp_dict[inv] = sample_dict

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
    for key, value in fragments_dict.iteritems():

        if len(iso_tracers) == 1:
            tup_key = (value[0].get_num_labeled_atoms_isotope(iso_tracers[0]),)

        elif len(iso_tracers) > 1:
            try:
                tup_key = (value[0].get_num_labeled_atoms_isotope(iso_tracers[0]),
                            value[0].get_num_labeled_atoms_isotope(iso_tracers[1]))
            except KeyError:
                raise KeyError('Name, Formula or Sample not found in input data file')

        nacorr_fragment_dict[key] = [value[0], lab_samp_dict[tup_key], value[2], value[3]]

    return nacorr_fragment_dict



def eleme_corr_to_list(iso_tracers, eleme_corr):
    """
    This function creates a list of elements to be corrected for multi tracer na correction.
    It includes the tracer elements along with the indistinguishable species.
    """

    trac_atoms = get_atoms_from_tracers(iso_tracers)

    eleme_corr_list = []
    for i in trac_atoms:
        eleme_corr_list.append([i])
        if i in eleme_corr.keys():
            eleme_corr_list.append(eleme_corr[i])

    return sum(eleme_corr_list, [])



def filter_tuples(tuple_list, value_dict, positions):
    """
    This function filters the tuple list for multi tracer na correction and appends
    zero value to the combinations not present in the input data

    Args:
        tuple_list : list of tuples with all possible combinations of the elements to
                     be corrected

        value_dict : dictionary of labels and intensity value from input data

        positions : position of tuple to be ignored for filtering

    Returns:
        result_tuples : list of intensites with zeroes appended at positions for which
                        combinations are not found in the input data.This intensites vector
                        is used to multiply with the resultant correction matrix for multi tracer
    """
    result_tuples = []
    for tuples in tuple_list:
        tuple_l = list(tuples)
        filtered_tuple = [tuple_l[x] for x in positions]
        if sum(filtered_tuple) == 0:
            rqrd_pos = [tuple_l[x] for x in range(0,len(tuple_l)) if x not in positions]
            rqrd_tup = tuple(rqrd_pos)
            if rqrd_tup in value_dict.keys():
                result_tuples.append(value_dict[rqrd_tup][0])
            else:
                result_tuples.append(0)
        else:
            result_tuples.append(0)
    return result_tuples









# -------------------------YALE--------------------------------------------------
def na_correct_mimosa_algo(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    iso_elem = hl.get_isotope_element(isotope)
    p = parent_frag_m.number_of_atoms(iso_elem)
    d = daughter_frag_n.number_of_atoms(iso_elem)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()

    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))
    return np.around(corrected_intensity, decimals)

def na_correct_mimosa_algo_array(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    iso_elem = hl.get_isotope_element(isotope)
    p = parent_frag_m.number_of_atoms(iso_elem)
    d = daughter_frag_n.number_of_atoms(iso_elem)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()
    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))

    return np.around(corrected_intensity, decimals)

def arrange_fragments_by_mass(fragments_dict):
    fragment_dict_mass = {}
    for key, value in fragments_dict.iteritems():
        parent_frag, daughter_frag = value[0]
        fragment_dict_mass[(parent_frag.isotope_mass, daughter_frag.isotope_mass)] = value
    return fragment_dict_mass

def na_correction_mimosa_by_fragment(fragments_dict, decimals):
    fragment_dict_mass = arrange_fragments_by_mass(fragments_dict)
    corrected_dict_mass = {}
    for key, value in fragment_dict_mass.iteritems():
        m_1_n = (key[0]-1, key[1])
        m_1_n_1 = (key[0]-1, key[1]-1)
        parent_frag_m, daughter_frag_n = value[0]
        isotope = parent_frag_m.isotope
        na = hl.get_isotope_na(isotope)
        data = value[1]
        corrected_data = {}
        for sample_name, intensity_m_n in data.iteritems():
            try:
                intensity_m_1_n = fragment_dict_mass[m_1_n][1][sample_name]
            except KeyError:
                intensity_m_1_n = np.zeros(len(intensity_m_n))
            try:
                intensity_m_1_n_1 = fragment_dict_mass[m_1_n_1][1][sample_name]
            except KeyError:
                intensity_m_1_n_1 = np.zeros(len(intensity_m_n))
            corrected_data[sample_name] = na_correct_mimosa_algo_array(parent_frag_m,
                                        daughter_frag_n, intensity_m_n, intensity_m_1_n,
                                        intensity_m_1_n_1, isotope, na, decimals)

        corrected_dict_mass[key] = [value[0], corrected_data, value[2], value[3]]
    return corrected_dict_mass



