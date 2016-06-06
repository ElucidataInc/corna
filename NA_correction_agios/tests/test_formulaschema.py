"""Unit testing module for formulaschema"""

import pytest

from corna.formulaschema import FormulaSchema

schema_obj = FormulaSchema()
polyatom_schema = schema_obj.create_polyatom_schema()
chemformula_schema = schema_obj.create_chemicalformula_schema()


def test_init_formulaschema():
    assert isinstance(schema_obj, FormulaSchema)


def test_create_polyatom_schema():
    polyatom_token = polyatom_schema.parseString('Elem1')
    polyatom = polyatom_token[0]
    assert (isinstance(polyatom.element, basestring)) and (isinstance(polyatom.number_atoms, int))


def test_check_if_element():
    assert schema_obj.check_if_element('H')


def test_check_if_element_wildcard():
    with pytest.raises(KeyError):
        schema_obj.check_if_element('Hij')
