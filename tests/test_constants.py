"""Unit testing module for """
import pytest

import corna.constants as const

const_obj = const.PyConstObj(value=100)

def test_const_value():
    assert const_obj.VALUE == 100

def test_cant_change_value():
    with pytest.raises(ValueError):
        const_obj.VALUE = 90

def test_name_small_doesnt_exist():
    with pytest.raises(AttributeError):
        print const_obj.value
