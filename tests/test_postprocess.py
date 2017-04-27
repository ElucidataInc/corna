import pickle

import pytest
import numpy as np
import corna.postprocess as postprocess

import constants

def test_replace_negatives_zero():
	assert postprocess.zero_if_negative(-1.23) == 0

def test_replace_negatives():
	assert postprocess.zero_if_negative(1.23) == 1.23


def test_sum_intensities_non_uniform_sample():
	##regression test NCT-265
	fragments_dict = pickle.load(open(constants.FRAGMENT_DICT_NON_UNIFORM_SAMPLE, "rb"))
	postprocess.sum_intensities(fragments_dict)







