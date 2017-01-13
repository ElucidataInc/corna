import pytest
import numpy as np
import corna.postprocess as pp


def test_replace_negatives_zero():
	assert pp.zero_if_negative(-1.23) == 0

def test_replace_negatives():
	assert pp.zero_if_negative(1.23) == 1.23










