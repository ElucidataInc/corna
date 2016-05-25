
import numpy as np
import helpers as hl

def na_correct_mimosa_algo(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    p = parent_frag_m.get_number_of_atoms_isotope(isotope)
    d = daughter_frag_n.get_number_of_atoms_isotope(isotope)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()

    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))
    return np.around(corrected_intensity, decimals)

def na_correct_mimosa_algo_array(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    p = parent_frag_m.get_number_of_atoms_isotope(isotope)
    d = daughter_frag_n.get_number_of_atoms_isotope(isotope)
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
