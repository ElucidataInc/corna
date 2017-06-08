import pytest

from corna import autodetect_isotopes as auto


def test_get_ppm_required():
    assert auto.get_ppm_required('C6H6O', 0.0002) == 2.1251446692233573


def test_get_elements_from_formula():
    assert auto.get_elements_from_formula('C6H6') == ['H', 'C']


def test_get_indistinguishable_ele():
    assert auto.get_indistinguishable_ele('C', 'N', 'C6H6N', 600) is None


def test_get_indistinguishable_ele():
    assert auto.get_indistinguishable_ele('C', 'N', 'C16H16O23N12',  2000) is 'N'


def test_ppm_validation():
    assert auto.ppm_validation(10.5, 10, 'C9H9', 'H') is True


def test_ppm_validation():
    assert auto.ppm_validation(100, 10, 'C9H9', 'H') is True


def test_ppm_validation():
    assert auto.ppm_validation(1, 10, 'C9H9', 'H') is None


def get_element_correction_dict():
    assert get_element_correction_dict(400, 'C14H65O9', ['C13']) == {'C': ['H', 'O']}

def test_borderline_ppm_warning():
    assert auto.borderline_ppm_warning(30, 30.1, 'C5H5', 'H') is True


def test_borderline_ppm_warning():
    assert auto.borderline_ppm_warning(30, 300.1, 'C5H5', 'H') is None

def test_get_mass_diff():
    assert auto.get_mass_diff('C','N') is 0.00631

def test_get_mass_diff():
    assert auto.get_mass_diff('C','P') is None







