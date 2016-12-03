import numpy
import corna.algorithms.nacorr_mimosa.algorithms_yale as algo
import corna.isotopomer as iso
from corna.inputs.multiquant_parser import Multiquantkey
from corna.constants import ISOTOPE_NA_MASS

data_input = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1967.77,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1446.77,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 747.77,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1926.77,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 1969.77,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 661.77}

data_unlabel = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':  62610,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':  58640,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':  59950,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':  62520,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':  59690,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':  57200}

corrected_data_input = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': -55.07,
                             'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': -456.52,
                             'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': -1214.13,
                             'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': -94.,
                             'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':  43.33,
                             'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': -1211.27}

corrected_data_unlabel = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':  64676.13,
                          'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':  60575.12,
                          'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':  61928.35,
                          'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':  64583.16,
                          'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':  61659.77,
                          'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':  59087.6}

unlabeled_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'),
                                                      'C13_185.0_79.0', data_unlabel)

input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'),
                                                  'C13_186.0_79.0', data_input)


parent_frag_input = input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][0]
daughter_frag_input = input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][1]

parent_frag_unlabeled = unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')][0][0]
daughter_frag_unlabeled = unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')][0][1]


fragment_dict = dict(unlabeled_fragment, **input_fragment)

corrected_fragment_dict = {(186.0, 79.0): iso.Infopacket(frag=[parent_frag_input, daughter_frag_input],
                                                                                      data = corrected_data_input, unlabeled=False, name='2PG 185/79'),
                                                         (185.0, 79.0): iso.Infopacket(frag=[parent_frag_unlabeled, daughter_frag_unlabeled],
                                                                                      data = corrected_data_unlabel, unlabeled=True, name='2PG 185/79')}

unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':51670,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':52360,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':52540,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':56580,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':52580,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':58990})


input_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97','C3H6O6P'), 'C13_170.0_97.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':1292.67,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':901.67,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':1292.67,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':1468.67,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':1511.67,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':1946.67})

corrected_data_unlabel_dhap = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':53375.11,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':54087.88,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':54273.82,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':58447.14,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':54315.14,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':60936.67}

corrected_data_input_dhap = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':-384.00,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':-806.37,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':-412.71,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':-366.16,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':-190.21,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':42.83}


parent_frag_input_dhap = input_fragment_dhap[('DHAP 170/97_170.0', 'DHAP 170/97_97.0')][0][0]
daughter_frag_input_dhap = input_fragment_dhap[('DHAP 170/97_170.0', 'DHAP 170/97_97.0')][0][1]

parent_frag_unlabeled_dhap = unlabeled_fragment_dhap[('DHAP 169/97_169.0', 'DHAP 169/97_97.0')][0][0]
daughter_frag_unlabeled_dhap = unlabeled_fragment_dhap[('DHAP 169/97_169.0', 'DHAP 169/97_97.0')][0][1]

corrected_fragment_dict_dhap = {(169.0, 97.0): iso.Infopacket(frag=[parent_frag_unlabeled_dhap, daughter_frag_unlabeled_dhap],
                                                                                      data = corrected_data_unlabel_dhap, unlabeled=True, name='DHAP 169/97'),
                                                         (170.0, 97.0): iso.Infopacket(frag=[parent_frag_input_dhap, daughter_frag_input_dhap],
                                                                                      data = corrected_data_input_dhap, unlabeled=False, name='DHAP 169/97')}

fragment_dict_dhap = dict(unlabeled_fragment_dhap, **input_fragment_dhap)

metabolite_frag_dict = {'dhap':fragment_dict_dhap, '2pg': fragment_dict}
corrected_metabolite_dict = {'dhap': corrected_fragment_dict_dhap, '2pg': corrected_fragment_dict}

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

def test_nacorr_mp():
    assert algo.nacorr_mp(ISOTOPE_NA_MASS, 2, ('2PG 185/79', fragment_dict)) == ('2PG 185/79', corrected_fragment_dict)

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
