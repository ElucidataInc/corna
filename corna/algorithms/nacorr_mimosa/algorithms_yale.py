import multiprocessing as mp
from functools import partial

import numpy as np
from ... import helpers
from ... isotopomer import Infopacket


def na_correct_mimosa_algo_array(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                                 isotope, na, decimals):
    iso_elem = helpers.get_isotope_element(isotope)
    p = parent_frag_m.number_of_atoms(iso_elem)
    d = daughter_frag_n.number_of_atoms(iso_elem)
    m = parent_frag_m.get_num_labeled_atoms_isotope(isotope)
    n = daughter_frag_n.get_num_labeled_atoms_isotope(isotope)
    corrected_intensity = intensity_m_n * (1 + na * (p - m)) - intensity_m_1_n * na * ((p - d) - (m - n - 1)) -\
        intensity_m_1_n_1 * na * (d - (n - 1))

    return np.around(corrected_intensity, decimals)


def arrange_fragments_by_mass(fragments_dict):
    fragment_dict_mass = {}
    for key, value in fragments_dict.iteritems():
        parent_frag, daughter_frag = value.frag
        fragment_dict_mass[
            (parent_frag.isotope_mass, daughter_frag.isotope_mass)] = value
    return fragment_dict_mass


def na_correction_mimosa_by_fragment(fragments_dict, decimals):
    fragment_dict_mass = arrange_fragments_by_mass(fragments_dict)
    corrected_dict_mass = {}
    for key, value in fragment_dict_mass.iteritems():
        m_1_n = (key[0] - 1, key[1])
        m_1_n_1 = (key[0] - 1, key[1] - 1)
        parent_frag_m, daughter_frag_n = value.frag
        isotope = parent_frag_m.isotracer
        na = helpers.get_isotope_na(isotope)
        corrected_data = {}
        for sample_name, intensity_m_n in value.data.iteritems():
            try:
                intensity_m_1_n = fragment_dict_mass[m_1_n].data[sample_name]
            except KeyError:
                intensity_m_1_n = np.zeros(len(intensity_m_n))
            try:
                intensity_m_1_n_1 = fragment_dict_mass[m_1_n_1].data[sample_name]
            except KeyError:
                intensity_m_1_n_1 = np.zeros(len(intensity_m_n))
            corrected_data[sample_name] = na_correct_mimosa_algo_array(parent_frag_m,
                                                                       daughter_frag_n, intensity_m_n, intensity_m_1_n,
                                                                       intensity_m_1_n_1, isotope, na, decimals)

        corrected_dict_mass[key] = Infopacket(value.frag,
                                                         corrected_data, value.unlabeled, value.name)
    return corrected_dict_mass


def nacorr_mp(decimals,tuple):
    metabolite = tuple[0]
    fragment_dict = tuple[1]
    corr_fragment_dict = na_correction_mimosa_by_fragment(fragment_dict, decimals)
    return (metabolite, corr_fragment_dict)

def na_correction_mimosa(metabolite_frag_dict, decimals=2):
    pool = mp.Pool(mp.cpu_count()-1)
    nacorr_part = partial(nacorr_mp, decimals)
    nacorrected_list = pool.map(nacorr_part, metabolite_frag_dict.iteritems())
    pool.close()
    na_corrected_out = {metab_info[0]:metab_info[1] for metab_info in nacorrected_list}
    return na_corrected_out

