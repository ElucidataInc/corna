import numpy
import pytest

import corna.isotopomer as iso
from corna.isotopomer import Infopacket
from corna.inputs.multiquant_parser import Multiquantkey
from corna.inputs.maven_parser import MavenKey
from corna.model import Fragment


def test_create_fragment_from_mass():
    frag_obj = iso.create_fragment_from_mass\
                          ('Glucose', 'C6H12O6', 'C13', 180, molecular_mass=None, mode=None)
    assert frag_obj['Glucose'].formula == 'C6H12O6'
    assert frag_obj['Glucose'].name == 'Glucose'
    assert frag_obj['Glucose'].isotracer == 'C13'
    assert frag_obj['Glucose'].isotope_mass == 180


def test_create_fragment_from_number():
    frag_obj = iso.create_fragment_from_number('Glucose', 'C6H12O6', {'C13': 2})
    assert frag_obj['Glucose'].name == 'Glucose'
    assert frag_obj['Glucose'].formula == 'C6H12O6'
    assert frag_obj['Glucose'].label_dict == {'C13': 2}


def test_create_fragment_from_number_error():
    with pytest.raises(KeyError) as err:
        iso.create_fragment_from_number('Glucose', 'C6H12O6', {'C133': 2})
        assert err.value.message == 'Check available isotope list', 'C133'


def test_create_combined_fragment():
    assert iso.create_combined_fragment\
         ({'Succinate 121/103_121.0': 'C4H5O4'},
          {'Succinate 121/103_103.0': 'C4H3O3'}) == {('Succinate 121/103_121.0',
                                                      'Succinate 121/103_103.0'): ['C4H5O4', 'C4H3O3']}


def test_validate_data():
    data = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 134)': 36575.724000000002,
            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 122)': 1361.3520000000001,
            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 190)': 54075.227999999996}
    assert iso.validate_data(data) == None


def test_validate_data_numerical_error():
    data = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 134)': 36575.724000000002,
            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 122)': 'abc'}
    with pytest.raises(TypeError) as err:
        iso.validate_data(data)
        assert err.value.message == 'Intensities should be numerical values'


def test_validate_data_sample_error():
    data = {1234: 36575.724000000}
    with pytest.raises(TypeError) as err:
        iso.validate_data(data)
        assert err.value.message == 'Sample Names should be of type unicode or string'


def test_add_data_fragment():
    frag_dict = {('Succinate 121/103_121.0', 'Succinate 121/103_103.0'): ['C4H5O4', 'C4H3O3']}
    data = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 134)': 5187.6000000000004,
            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 122)': 0.0,
            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 190)': 4480.1999999999998}
    label_info = False
    name = 'Succinate 117/99'
    assert iso.add_data_fragment(frag_dict,
                                 data, label_info, name) == {('Succinate 121/103_121.0', 'Succinate 121/103_103.0'):
                                                               Infopacket(frag=['C4H5O4', 'C4H3O3'],
                                                               data={'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 122)': 0.0,
                                                                     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 190)': 4480.2,
                                                                     'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 134)': 5187.6},
                                                               unlabeled=False, name='Succinate 117/99')}


def test_parse_label_number():
    assert iso.parse_label_number('C13_1_N15_2') == {'C13': 1, 'N15': 2}


def test_parse_label_number_isotope_error():
    with pytest.raises(KeyError) as err:
        iso.parse_label_number('C131_N15_2')
        assert err.value.message == 'The key must be an isotope'


def test_parse_label_number_num_error():
    with pytest.raises(ValueError):
     iso.parse_label_number('C13_N15')


# below test cases removed from agios delivery
def test_parse_label_mass():
    assert iso.parse_label_mass('C13_191_111') == {'tracer': 'C13', 'parent_mass': 191, 'daughter_mass': 111}


def test_parse_label_mass_indexerror():
    with pytest.raises(IndexError) as err:
        iso.parse_label_mass('C13')
    assert err.value.message == 'The key should have three components,' \
                                ' isotope, parent mass and daughter mass' \
                                ' separated by _ in the same order'


def test_parse_label_mass_value_error():
    with pytest.raises(ValueError) as err:
        iso.parse_label_mass('C13_N15_11')
    assert err.value.message == 'Masses should be convertible to floats'


def test_parse_label_mass_key_error():
    with pytest.raises(KeyError) as err:
        iso.parse_label_mass('191_111')
    assert err.value.message == 'Isotope should be part of the constants'


def test_insert_data_to_fragment_mass():
    frag_info = Multiquantkey(name='Succinate 121/103', formula='C4H3O3', parent='Succinate 117/99',
                              parent_formula='C4H5O4')
    label = 'C13_121_103'
    sample_dict = {'sample 134': 5187.60}
    assert str(iso.insert_data_to_fragment_mass(frag_info, label, sample_dict, mode=None)) == "{('Succinate 121/103_121.0', " \
                                                                                              "'Succinate 121/103_103.0'): " \
                                                                                              "Infopacket(frag=[C4H5O4, C4H3O3]," \
                                                                                              " data={'sample 134': 5187.6}, " \
                                                                                              "unlabeled=False, name='Succinate 117/99')}"


def test_insert_data_to_fragment_number():
    frag_info = MavenKey(name='CDP', formula='C9H15N3O11P2')
    label = 'C13_8_N15_3'
    sample_dict = {'SAMPLE_#SNYGTT5_2_6': 0.0,
                   'SAMPLE_#SNYGTT5_3_5': 1598.6510000000001}
    assert str(iso.insert_data_to_fragment_number(frag_info, label, sample_dict)) == "{'CDP_C13_8_N15_3': Infopacket(frag=C9H15N3O11P2, " \
                                                                                     "data={'SAMPLE_#SNYGTT5_3_5': 1598.651," \
                                                                                     " 'SAMPLE_#SNYGTT5_2_6': 0.0}," \
                                                                                     " unlabeled=False, name='CDP')}"


def test_bulk_insert_data_to_fragment():
    frag_info = MavenKey(name='CDP', formula='C9H15N3O11P2')
    list_data_dict = {'C13_8_N15_3': {'SAMPLE_#SNYGTT5_3_5': 1598.6510000000001}}
    assert str(iso.bulk_insert_data_to_fragment(frag_info, list_data_dict, mass=False, number=True)) == "{'CDP_C13_8_N15_3':" \
                                                                                                        " Infopacket(frag=C9H15N3O11P2, " \
                                                                                                        "data={'SAMPLE_#SNYGTT5_3_5': 1598.651}, " \
                                                                                                        "unlabeled=False, " \
                                                                                                        "name='CDP')}"


