import corna.preprocess as preproc

def test_background_noise_label_less():
    assert round(preproc.background_noise(2, 0.011, 5, 100), 3) == 0.121

def test_background_noise_label_more():
    assert preproc.background_noise(5, 0.011, 2, 100) == 1.6105099999999996e-08

