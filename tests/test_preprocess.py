import corna.preprocess as preproc


def test_background_noise_label_less():
    assert round(preproc.background_noise(2, 0.011, 5, 100), 3) == 0.121

def test_background_noise_label_more():
    assert preproc.background_noise(5, 0.011, 2, 100) == 1.6105099999999996e-08

def test_backround_subtraction():
    assert preproc.backround_subtraction(27800, 2.29E+03) == 25510.0

def test_backround_subtraction_negative():
    assert preproc.backround_subtraction(2.29E+03, 27800) == 0.0