from __future__ import print_function
import pytest

from corna.model import Ion

class TestIonClass:

    @classmethod
    def setup_class(cls):
        name = 'Glucose'
        formula = 'C6H12O6'
        charge = -1
        cls.ion = Ion(name, formula, charge)

    @classmethod
    def teardown_class(cls):
        del cls.ion

    def test_get_formula(self):
        assert self.ion.get_formula() == {'C':6, 'H':12, 'O':6}

    def test_number_of_atoms(self):
        assert self.ion.number_of_atoms('C') == 6

    def test_number_of_atoms_wildcard(self):
        with pytest.raises(KeyError):
            self.ion.number_of_atoms('N')
