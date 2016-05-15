def na_correct_mimosa(frag_m_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1, isotope, na):
    frag_m = frag_m_n[0]
    frag_n = frag_m_n[1]
    p = frag_m.get_labeled_elem_num(isotope)
    d = frag_n.get_labeled_elem_num(isotope)
    m = frag_m.get_num_labeled_atoms(isotope)
    n = frag_n.get_num_labeled_atoms(isotope)
    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))
