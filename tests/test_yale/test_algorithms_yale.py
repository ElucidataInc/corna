import numpy
import corna.algorithms.nacorr_mimosa.algorithms_yale as algo
import corna.isotopomer as iso
from corna.inputs.multiquant_parser import Multiquantkey

unlabeld_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'), 'C13_185.0_79.0',
                                                      {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': numpy.array([ 62608.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': numpy.array([ 58642.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': numpy.array([ 59951.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': numpy.array([ 62521.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': numpy.array([ 59689.]),
      'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': numpy.array([ 57204.])})

input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79','C3H6O7P'), 'C13_186.0_79.0',
                                                  {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': numpy.array([ 1968.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': numpy.array([ 1447.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': numpy.array([ 748.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': numpy.array([ 1927.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': numpy.array([ 1970.]),
                                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': numpy.array([ 662.])})

def test_na_correct_mimosa_array():
    print algo.na_correct_mimosa_algo_array(input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][0],
                                            input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][1],
                                            numpy.array[59689., 59951., 57204., 58642., 62608., 62521.],
                                            numpy.zeros(6),
                                            numpy.zeros(6),
                                            'C13',
                                            0.011,
                                            2)







# def test_na_correct_mimosa():
#     assert algo.na_correct_mimosa_algo(input_fragment[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')][0][0],
#                                   input_fragment[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')][0][1],
#                                   2055, 40820, 0, 'C13', 0.011) == 798.3600000000001

# def test_na_correct_mimosa_zero():
#     assert algo.na_correct_mimosa_algo(input_fragment[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')][0][0],
#                                   input_fragment[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')][0][1],
#                                   769, 87550, 0, 'C13', 0.011) == 0


# def test_arrange_fragments_by_mass():
#     test_dict = algo.arrange_fragments_by_mass(glutamate_146_41)
#     for key, value in glutamate_146_41_output_dict.iteritems():
#         assert test_dict[key] == value

# def test_na_correction_mimosa_by_fragment():
#     test_dict = algo.na_correction_mimosa_by_fragment(glutamate_146_41)
#     test_data = test_dict[(147.0, 42.0)][1]
#     assert numpy.array_equal(numpy.around(test_data['F. [13C-glc] G2.5 120min'],8), numpy.around(numpy.array([991.7099655, 522.23934132,
#                                                                                  2790.3025836, 0., 1768.9036688,

#                                                                                  2126.6667507 ]),8))

