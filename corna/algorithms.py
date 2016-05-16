def na_correct_mimosa_algo(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na):
    p = parent_frag_m.get_number_of_atoms_isotope(isotope)
    d = daughter_frag_n.get_number_of_atoms_isotope(isotope)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()
    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))
    if corrected_intensity>0:
        return corrected_intensity
    else:
        return 0

def arrange_fragments_by_mass(fragments_dict):
    fragment_dict_mass = {}
    for key, value in fragments_dict.iteritems():
        parent_frag, daughter_frag = value[0]
        fragment_dict_mass[(parent_frag.isotope_mass, daughter_frag.isotope_mass)] = value
    return fragment_dict_mass

def na_correction_mimosa_by_fragment(fragments_dict):
    fragment_dict_mass = arrange_fragments_by_mass(fragments_dict)