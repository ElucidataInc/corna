import pytest
import corna.helpers as help
import pandas as pd

def test_get_atomic_weight():
    assert help.get_atomic_weight('Al') == 26.981538

def test_get_atomic_weight_wildcard():
    with pytest.raises(KeyError) as err:
        help.get_atomic_weight('PP')
    assert err.value.message == 'Element doesnt exist'

def test_check_if_isotope_in_dict():
    assert help.check_if_isotope_in_dict('C13') == True

def test_check_if_isotope_in_dict_false():
    assert help.check_if_isotope_in_dict('C14') == False

def test_get_isotope_details():
    assert help.get_isotope_element('C13') == 'C'

def test_get_isotope_na():
    assert help.get_isotope_na('C13') == 0.0111

def    test_get_isotope_mass():
    assert help.get_isotope_mass('C13') == 13

def test_get_isotope_natural():
    assert help.get_isotope_natural('C13') == 'C12'

def test_get_isotope_keyerror():
    assert not help.check_if_isotope_in_dict('Ind5')

def test_label_dict_to_key():
    assert help.label_dict_to_key({'C13':2, 'N14':4}) == 'C13_2_N14_4'

def test_read_file():
    path = 'incorrectpath.xlsx'
    with pytest.raises(IOError):
        file_in = help.read_file(path)

def test_read_file_ext():
    path = 'no_or_invalid_extension'
    with pytest.raises(IOError):
        file_in = help.read_file(path)

def test_filter_df():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [2, 2, 2]})
    filter_dict = {'col_1': [1]}
    with pytest.raises(KeyError):
        filter_df = help.filter_df(df, filter_dict)

def test_create_dict_from_isotope_label_list():
    assert help.create_dict_from_isotope_label_list(['C13',2,'N15',5]) == {'C13': 2, 'N15': 5}

def test_create_dict_from_isotope_label_list_missing_number():
    with pytest.raises(ValueError) as err:
        help.create_dict_from_isotope_label_list(['C13','N15',5])
    assert err.value.message == 'The number of labels should be integer'

def test_create_dict_from_isotope_label_list_no_isotope():
    with pytest.raises(KeyError) as err:
        help.create_dict_from_isotope_label_list([6, 'C13','N15',5])
    assert err.value.message == 'The key must be an isotope'

def test_get_key_from_single_value_dict():
    assert help.get_key_from_single_value_dict({'C13':1}) == 'C13'

def test_get_value_from_single_value_dict():
    assert help.get_value_from_single_value_dict({'C13':1}) == 1

def test_get_key_from_single_value_dict_len_error():
    with pytest.raises(OverflowError):
        help.get_key_from_single_value_dict({'C13':1, 'C14':2})

def test_get_formula():
    assert help.get_formula('C6H12O6') == {'C':6, 'H':12, 'O':6}

def test_get_na_value_dict_O():
    assert help.get_na_value_dict()['O'] == [0.9976, 0.0004, 0.002]
