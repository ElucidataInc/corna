"""Unit testing module for """
import pytest

import corna.constants as const


def test_mass_diff_dict():
    assert const.MASS_DIFF_DICT['O17']['N'] == 0.0044


def test_isotope_dict():
    assert const.ISOTOPE_DICT['O'] == ['O17','O18']