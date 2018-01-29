import pytest

from corna import autodetect_isotopes as auto


def test_get_ppm_required():
    assert auto.get_ppm_required('C6H6O', 0.0002) == 2.1251446692233573


def test_indistinguishable_ele_none():
    assert auto.get_indistinguishable_ele('C', 'N', 'C6H6N', 6) == None


def test_get_indistinguishable_ele():
    assert auto.get_indistinguishable_ele('C', 'N', 'C16H16O23N12',  2000) == None


def test_ppm_validation_borderline():
    assert auto.ppm_validation(10.5, 10, 'C9H9', 'H')


def test_ppm_validation_true():
    assert auto.ppm_validation(100, 10, 'C9H9', 'H')


def test_ppm_validation_false():
    assert auto.ppm_validation(1, 10, 'C9H9', 'H') == None


def test_get_element_correction_dict():
    assert auto.get_element_correction_dict(400, 'C14H65O9', ['C13']) == {'C': ['H', 'O17']}


def test_get_element_correction_dict_two_isotracer():
    assert auto.get_element_correction_dict(2, 'C6H6NO', ['C13','N15']) == {'C': [], 'N': []}


def test_get_element_correction_dict_without_isotracer():
    assert auto.get_element_correction_dict(2, 'C6H6NO', []) == {}


def test_get_element_correction_dict_keyerror():
    assert auto.get_element_correction_dict(20, 'C6H6NOPS', ['S34']) == {'S': []}


def test_raise_borderline_ppm_warning():
    assert auto.borderline_ppm_warning(30, 30.1, 'C5H5', 'H')


def test_borderline_ppm_warning():
    assert auto.borderline_ppm_warning(30, 300.1, 'C5H5', 'H') == None

def test_get_mass_diff():
    assert auto.get_mass_diff('C13', 'N') == 0.0063199068000000524

def test_get_mass_diff_keyerror():
    assert auto.get_mass_diff('C13','P') == None


def test_get_isotope_element_list():
    assert auto.get_isotope_element_list(['C13', 'N15']) == ['C', 'N']

def test_add_isotopes_list():
    assert auto.add_isotopes_list(['O', 'C']) == ['C', 'O17', 'O18']
