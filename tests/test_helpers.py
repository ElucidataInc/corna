import pytest
import corna.helpers as help

def test_get_atomic_weight():
    assert help.get_atomic_weight('Al') == 26.981538

def test_get_atomic_weight_wildcard():
    with pytest.raises(KeyError) as err:
        help.get_atomic_weight('R')
    assert err.value.message == 'Element doesnt exist'
