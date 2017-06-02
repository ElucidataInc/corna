import corna.algorithms.mimosa_nacorr as algo
import corna.isotopomer as iso
import tests.data_constants as data_constants
from corna.constants import ISOTOPE_NA_MASS

parent_frag_input, daughter_frag_input,\
fragment_dict, data_input,\
parent_frag_unlabeled,\
daughter_frag_unlabeled, data_unlabel,\
corrected_fragment_dict, metabolite_frag_dict,\
corrected_fragment_dict_dhap, corrected_fragment_dict = data_constants.algorithms_yale_constants()

def test_na_correct_mimosa_array():
    assert algo.na_correct_mimosa_algo_array(parent_frag_input, daughter_frag_input, 1967.77,
                                             62610, 0., 'C13', 0.011, 2) == -55.07

def test_arrange_fragments_by_mass():
    assert algo.change_fragment_keys_to_mass(fragment_dict) == {(186.0, 79.0): iso.Infopacket(frag=[parent_frag_input, daughter_frag_input],
                                                                                      data = data_input, unlabeled=False, name='2PG 185/79'),
                                                         (185.0, 79.0): iso.Infopacket(frag=[parent_frag_unlabeled, daughter_frag_unlabeled],
                                                                                      data = data_unlabel, unlabeled=True, name='2PG 185/79')}

def test_na_correction_mimosa_by_fragment():
    assert algo.na_correction_mimosa_by_fragment(fragment_dict, ISOTOPE_NA_MASS, 2) == corrected_fragment_dict

def test_na_correction_mimosa():
    test_dict = algo.na_correction_mimosa(metabolite_frag_dict)
    for key, value in test_dict['dhap'].iteritems():
        assert corrected_fragment_dict_dhap[key].data == value.data
        assert corrected_fragment_dict_dhap[key].unlabeled == value.unlabeled
        assert corrected_fragment_dict_dhap[key].name == value.name
    for key, value in test_dict['2pg'].iteritems():
        assert corrected_fragment_dict[key].data == value.data
        assert corrected_fragment_dict[key].unlabeled == value.unlabeled
        assert corrected_fragment_dict[key].name == value.name
