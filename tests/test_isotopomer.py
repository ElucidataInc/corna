import numpy
import pytest

import corna.isotopomer as iso
from corna.model import Fragment

class TestIsotopomerClass:
    @classmethod
    def setup_class(cls):
        cls.fragment = Fragment('Glucose', 'C6H12O6')
        cls.frag_key = 'glucose_C6H12O6'
        cls.label_dict = {'C13':4}
        cls.label_key = 'C13_4'
        cls.intensities = numpy.array([2345, 5673, 456, 567.3])
        cls.intensity_err = [2345, 5673, 456, 567.3]

    @classmethod
    def teardown_class(cls):
        del cls.fragment
        del cls.frag_key
        del cls.label_dict
        del cls.label_key
        del cls.intensities
        del cls.intensity_err

    def test_create_fragment(self):
        assert isinstance(iso.create_fragment('glucose', 'C6H12O6')[self.frag_key], Fragment)

    def test_create_isotopomer_label(self):
        assert iso.create_isotopomer_label({self.frag_key: self.fragment}, self.label_dict)[0][self.frag_key]\
               == {self.label_key:self.label_dict}

    def test_add_data_isotopomers(self):
        assert numpy.array_equal(numpy.array([ 2345. ,  5673. ,   456. ,   567.3]),
                                 iso.add_data_isotopomers(self.frag_key, self.label_dict,
                                                          self.intensities)['glucose_C6H12O6']['C13_4'])

    def test_add_data_isotopomers_array_err(self):
        with pytest.raises(AssertionError) as err:
            iso.add_data_isotopomers(self.frag_key, self.label_dict, self.intensity_err)
        assert err.value.message == 'intensity should be numpy array'

def test_parse_label_number():
    assert iso.parse_label_number('C13_1_N15_2') == {'C13':1, 'N15':2}

def test_parse_label_number_isotope_error():
    with pytest.raises(KeyError):
     iso.parse_label_number('C131_N15_2')

def test_parse_label_number_num_error():
    with pytest.raises(ValueError):
     iso.parse_label_number('C13_N15')