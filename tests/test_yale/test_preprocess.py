from collections import OrderedDict
import numpy
import corna.algorithms.nacorr_mimosa.preprocess as preproc
import corna.isotopomer as iso
from corna.inputs.multiquant_parser import Multiquantkey


unlabeled_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'), 'C13_185.0_79.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([59689.272]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([59950.872]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([57204.072]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([58641.564]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([62607.86519]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([62521.092])})
input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'), 'C13_186.0_79.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([2746.8]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([1525.128]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([1438.8]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([2223.6]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([2745.492]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([2703.636])})

corrected_unlabeld_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'), 'C13_185.0_79.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': numpy.array([ 62608.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': numpy.array([ 58642.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': numpy.array([ 59951.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': numpy.array([ 62521.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': numpy.array([ 59689.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': numpy.array([ 57204.])})

corrected_input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'), 'C13_186.0_79.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': numpy.array([ 1968.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': numpy.array([ 1447.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': numpy.array([ 748.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': numpy.array([ 1927.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': numpy.array([ 1970.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': numpy.array([ 662.])})

unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([51666]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([52361.856]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([52538.436]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([56580.91398]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([52581.6]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([58989.492])})

input_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97','C3H6O6P'), 'C13_170.0_97.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([1874.364]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([1483.272]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([1874.364]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([2049.636]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([2092.8]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([2528.364])})

corr_unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([51666]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([52362.]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([52538.]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([56581.]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([52582.]),
                                                       'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([58989.])})

corr_input_fragment_dhap = iso.insert_data_to_fragment_mass(Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97','C3H6O6P'), 'C13_170.0_97.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([1293.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([902.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([1293.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([1468.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([1511.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([1947.])})



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

sample_data = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)':numpy.array([2746.8]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)':numpy.array([1525.128]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)':numpy.array([1438.8]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)':numpy.array([2223.6]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)':numpy.array([2745.492]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)':numpy.array([2703.636]),
               'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 2)':numpy.array([1308]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 18)':numpy.array([1700.4]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 34)':numpy.array([1220.364]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 50)':numpy.array([2354.4]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 66)':numpy.array([1615.38]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 82)':numpy.array([2092.8]),
               'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 3)':numpy.array([1831.2]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 19)':numpy.array([2572.836]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 35)':numpy.array([1394.328]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 51)':numpy.array([1132.728]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 67)':numpy.array([1612.764]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 83)':numpy.array([2134.656])}

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
    background_dict = preproc.background(list_of_replicates,
                                          input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')],
                                          unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')])
    assert all(val == 777.05402400000048 for val in background_dict.values())

def test_background_correction():
    assert preproc.background_correction(replicates, sample_background, sample_data, 2) == {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 34)': numpy.array([ 443.31]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 35)': numpy.array([ 617.27]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': numpy.array([ 1968.44]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 18)': numpy.array([ 923.35]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 82)': numpy.array([ 1315.75]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': numpy.array([ 1446.55]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': numpy.array([ 748.07]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 50)': numpy.array([ 1577.35]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 51)': numpy.array([ 355.67]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': numpy.array([ 1926.58]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 2)': numpy.array([ 530.95]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': numpy.array([ 1969.75]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 83)': numpy.array([ 1357.6]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 19)': numpy.array([ 1795.78]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 67)': numpy.array([ 835.71]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 66)': numpy.array([ 838.33]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': numpy.array([ 661.75]),
     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 3)': numpy.array([ 1054.15])}


def test_bulk_background_correction():
    test_dict = preproc.bulk_background_correction(fragment_dict, list_of_replicates, sample_background, 0)
    for key, value in test_dict.iteritems():
        assert corrected_fragment_dict[key].data == value.data

def test_met_background_correction():
    test_dict = preproc.met_background_correction(metabolite_frag_dict, list_of_replicates, sample_background)
    for key, value in test_dict['dhap'].iteritems():
        assert corrected_fragment_dict_dhap[key].data == value.data
    for key, value in test_dict['2pg'].iteritems():
        assert corrected_fragment_dict[key].data == value.data
