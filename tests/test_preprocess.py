import numpy
import corna.preprocess as preproc
import corna.isotopomer as iso

def test_background_noise_label_less():
    assert round(preproc.background_noise(2, 0.011, 5, 100), 3) == 0.121

def test_background_noise_label_more():
    assert preproc.background_noise(5, 0.011, 2, 100) == 1.6105099999999996e-08

def test_backround_subtraction():
    assert preproc.backround_subtraction(27800, 2.29E+03) == 25510.0

def test_backround_subtraction_negative():
    assert preproc.backround_subtraction(2.29E+03, 27800) == 0.0


input_fragment = iso.insert_data_to_fragment(('Glutamate 147/41', 'C2HO', 'C5H8NO4'), 'C13_147.0_41.0', {'A. [13C-glc] G2.5 0min':
                                                                                             numpy.array([1155.5335, 1409.6325, 2052.6495,
                                                                                              1284.4085, 1542.459, 1542.5255])}, mass=True, number=False, mode=None)
unlabeled_fragment = iso.insert_data_to_fragment(('Glutamate 146/41', 'C2HO', 'C5H8NO4'), 'C13_146.0_41.0', {'A. [13C-glc] G2.5 0min':
                                                                                             numpy.array([45057.0155, 31707.183, 54944.625,
                                                                                              32608.4505, 60981.034, 38701.986])}, mass=True, number=False, mode=None)

def test_background():
    assert preproc.background('A. [13C-glc] G2.5 0min', input_fragment[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')],
                       unlabeled_fragment[('Glutamate 146/41_146.0', 'Glutamate 146/41_41.0')]) == [191.31336829999998, 731.09878379999998, 876.83452499999999, 586.58765930000004, 237.4648724000001, 714.30299960000002]

background_list = [1.23E+02, 3.81E+02, 0.00E+00, 3.85E+02, 2.43E+02, 0.00E+00]
sample_data = {'A. [13C-glc] G2.5 0min' : numpy.array([128.9, 385.1, 0, 385.2, 250.6, 0]),
'B. [13C-glc] G2.5 5min' : numpy.array([258.1, 370.2, 901.3, 1026, 127, 254]),
'C. [13C-glc] G2.5 15min' : numpy.array([2182, 1797, 3722, 1798, 2440, 1928]),
'D. [13C-glc] G2.5 30min': numpy.array([2952, 3468,	3595, 2696,	3339, 2569]),
'E. [13C-glc] G2.5 60min': numpy.array([2184, 2569,	2827, 2440,	3851, 3595]),
'F. [13C-glc] G2.5 120min': numpy.array([3466, 3850, 4234, 3210, 3593, 3210]),
'G. [13C-glc] G2.5 240min': numpy.array([2825, 4236, 7703, 3466, 2440, 2954]),
'H. [6,6-DD-glc] G2.5 240min': numpy.array([258, 0,	0, 127.1, 770.3, 0])}

corrected_sample =  {'D. [13C-glc] G2.5 30min': numpy.array([ 2567.,  3083.,  3210.,  2311.,  2954.,  2184.]),
                     'F. [13C-glc] G2.5 120min': numpy.array([ 3081.,  3465.,  3849.,  2825.,  3208.,  2825.]),
                     'A. [13C-glc] G2.5 0min': numpy.array([ 0. ,  0.1,  0. ,  0.2,  0. ,  0. ]),
                     'G. [13C-glc] G2.5 240min': numpy.array([ 2440.,  3851.,  7318.,  3081.,  2055.,  2569.]),
                     'H. [6,6-DD-glc] G2.5 240min': numpy.array([   0. ,    0. ,    0. ,    0. ,  385.3,    0. ]),
                     'E. [13C-glc] G2.5 60min': numpy.array([ 1799.,  2184.,  2442.,  2055.,  3466.,  3210.]),
                     'C. [13C-glc] G2.5 15min': numpy.array([ 1797.,  1412.,  3337.,  1413.,  2055.,  1543.]),
                     'B. [13C-glc] G2.5 5min': numpy.array([   0. ,    0. ,  516.3,  641. ,    0. ,    0. ])}

#this test not working properly, write correct test
def test_background_correction():
    test_output = preproc.background_correction(background_list, sample_data)
    for key, value in corrected_sample.iteritems():
        if not numpy.array_equal(test_output[key], value):
            assert False
    assert True
