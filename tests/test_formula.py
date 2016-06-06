"""unit testing module for Formula class"""
import pytest
from pyparsing import ParseException

from corna.formula import Formula

formula = Formula('C6H12O6')
err_formula = Formula('5O7')
err_formula_elem = Formula('Sar5H6')

def test_init_formula():
    assert isinstance(formula, Formula)

def test_parse_chemicalforumla_to_polyatom():
    formula_list = (formula.parse_chemforumla_to_polyatom()).asList()
    assert formula_list == [['C', 6], ['H', 12], ['O', 6]]

def test_parse_chemicalforumla_to_polyatom_wildcard():
    with pytest.raises(ParseException):
        err_formula.parse_chemforumla_to_polyatom()

def test_parse_formula_to_elem_numatoms():
    elem_numatoms_dict = formula.parse_formula_to_elem_numatoms()
    assert elem_numatoms_dict == {'C': 6, 'H': 12, 'O': 6}

def test_parse_formula_to_elem_numatoms_wildcard():
    with pytest.raises(KeyError):
        err_formula_elem.parse_formula_to_elem_numatoms()


