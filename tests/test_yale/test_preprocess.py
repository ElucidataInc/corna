import numpy
from collections import OrderedDict

import corna.algorithms.mimosa_bgcorr as preproc
import corna.isotopomer as iso
from corna.constants import ISOTOPE_NA_MASS
from corna.inputs.multiquant_parser import Multiquantkey
from corna.isotopomer import Infopacket

unlabeled_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'), 'C13_185.0_79.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':59689.272,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':59950.872,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':57204.072,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':58641.564,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':62607.86519,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':62521.092})
input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'), 'C13_186.0_79.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':2746.8,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':1525.128,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':1438.8,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':2223.6,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':2745.492,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':2703.636})

corrected_unlabeld_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'), 'C13_185.0_79.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':  62608.,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':  58642.,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':  59951.,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':  62521.,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':  59689.,
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':  57204.})

corrected_input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'), 'C13_186.0_79.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':  1968.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':  1447.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':  748.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':  1927.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':  1970.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':  662.})

unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':51666,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':52361.856,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':52538.436,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':56580.91398,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':52581.6,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':58989.492})

input_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97','C3H6O6P'), 'C13_170.0_97.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':1874.364,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':1483.272,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':1874.364,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':2049.636,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':2092.8,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':2528.364})

corr_unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':51666,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':52362.,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':52538.,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':56581.,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':52582.,
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':58989.})

corr_input_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97','C3H6O6P'), 'C13_170.0_97.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':1293.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':902.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':1293.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':1468.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':1511.,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':1947.})



list_of_replicates = [numpy.array(['TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)',
                                           'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)',
                                           'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)',
                                           'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)',
                                           'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)',
                                           'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)'], dtype=object)]

replicates = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 777.05402400000048,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 777.05402400000048,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 777.05402400000048,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 777.05402400000048,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 777.05402400000048,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 777.05402400000048}

sample_background = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)' : 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 2)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 3)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 18)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 19)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 34)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 35)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 50)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 51)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 66)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 67)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 82)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)',
'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 83)': 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)'}

sample_data = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':2746.8,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':1525.128,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':1438.8,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':2223.6,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':2745.492,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':2703.636,
               'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 2)':1308,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 18)':1700.4,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 34)':1220.364,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 50)':2354.4,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 66)':1615.38,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 82)':2092.8,
               'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 3)':1831.2,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 19)':2572.836,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 35)':1394.328,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 51)':1132.728,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 67)':1612.764,
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 83)':2134.656}

fragment_dict = dict(unlabeled_fragment, **input_fragment)
fragment_dict_dhap = dict(unlabeled_fragment_dhap, **input_fragment_dhap)

corrected_fragment_dict = dict(corrected_unlabeld_fragment, **corrected_input_fragment)
corrected_fragment_dict_dhap = dict(corr_unlabeled_fragment_dhap, **corr_input_fragment_dhap)

metabolite_frag_dict = {'dhap':fragment_dict_dhap, '2pg': fragment_dict}

def test_background_noise_label_daughter_unlabel():
    assert preproc.background_noise(31710, 0.011, 5, 1, 2, 0) == 1046.43

def test_background_noise_label_daughter_label():
     assert preproc.background_noise(31710, 0.011, 5, 1, 2, 1) == 697.62

def test_backround_subtraction():
    assert preproc.backround_subtraction(27800, 2.29E+03) == 25510.0


def test_background():
    background_dict = preproc.background(list_of_replicates, input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')],
                                         unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')], isotope_dict=ISOTOPE_NA_MASS)
    output = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 759.14724240000032,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 759.14724240000032,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 759.14724240000032,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 759.14724240000032,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 759.14724240000032,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 759.14724240000032}
    assert background_dict == output

def test_background_correction():
    result = preproc.background_correction(replicates, sample_background, sample_data, 0)
    output = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 34)': 443.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 35)': 617.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1968.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 18)': 923.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 82)': 1316.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1447.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 748.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 50)': 1577.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 51)': 356.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1927.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 2)': 531.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 1970.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 83)': 1358.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 19)': 1796.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 67)': 836.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 66)': 838.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 662.0,
              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 3)': 1054.0}
    assert result == output


def test_bulk_background_correction():
    test_dict = preproc.bulk_background_correction(fragment_dict, list_of_replicates, sample_background, ISOTOPE_NA_MASS, 0)
    assert test_dict[('2PG 185/79_185.0', '2PG 185/79_79.0')].data == {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 62608.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 58642.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 59951.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 62521.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 59689.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 57204.0}

    assert test_dict[('2PG 186/79_186.0', '2PG 186/79_79.0')].data == {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1986.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1464.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 766.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1944.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':1988.0,
                                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 680.0}


def test_met_background_correction():
    test_dict = preproc.met_background_correction(metabolite_frag_dict, list_of_replicates, sample_background)
    assert test_dict['dhap'][('DHAP 170/97_170.0', 'DHAP 170/97_97.0')].data == {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1529.0,
                                                                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1486.0,
                                                                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 919.0,
                                                                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1964.0,
                                                                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 1310.0,
                                                                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 1310.0}

    assert test_dict['2pg'][('2PG 185/79_185.0', '2PG 185/79_79.0')].data == {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 62608.0,
                                                                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 58642.0,
                                                                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 59951.0,
                                                                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 62521.0,
                                                                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 59689.0,
                                                                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 57204.0}
