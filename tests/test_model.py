from __future__ import print_function
import pytest

from corna.model import Ion
from corna.model import Label

class TestIonClass:

    @classmethod
    def setup_class(cls):
        cls.ion = Ion('Glucose', 'C6H12O6', -1)
        cls.ion_err = Ion('OrganicCompund', 'CH2R', 0)

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

    def test_molecular_weight(self):
        assert self.ion.get_mol_weight() == 180.15588

    def test_molecular_weight_wildcard(self):
        with pytest.raises(KeyError):
            self.ion_err.get_mol_weight()

class TestLabelClass:

    @classmethod
    def setup_class(cls):
        cls.label = Label({'C':2,'N':3})

    @classmethod
    def teardown_class(cls):
        del cls.label

    def test_get_number_of_labeled_atoms(self):
        self.label.get_num_labeled_atoms('C')