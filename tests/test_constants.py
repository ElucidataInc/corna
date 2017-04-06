"""Unit testing module for """
import pytest

import corna.constants as const

const_obj = const.PyConstObj(value=100)
const_dict = const.PyConstObj(elem_mol={'C':12,'O':16})

def test_const_value():
    assert const_obj.VALUE == 100

def test_cant_change_value():
    with pytest.raises(ValueError):
        const_obj.VALUE = 90

def test_name_small_doesnt_exist():
    with pytest.raises(AttributeError):
        print const_obj.value

def test_const_dict():
    const_dict.ELEM_MOL['N'] = 8
    print const_dict.ELEM_MOL