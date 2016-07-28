# chemicalFormulas.py
#
# Copyright (c) 2003, 2007, Paul McGuire
#
"""Define possible schema for a chemical formula"""
import pyparsing
from . import constants


class FormulaSchema(object):
    """This class has functions which help in defining all possible
    schemas a chemical formula can take. It takes into account only
    symbols which exist in periodic table and raises error if some
    other symbol is used in a formula.

    Attributes:
        chemicalformula_schema : Schema of chemical formula
        elements_and_molecular_weights : Dictionary of elements and
            molecular weights.Its a constant.
    """
    def __init__(self):
        """Initialise class with no arguments"""

        self.elements_and_molecular_weights = constants.ELE_ATOMIC_WEIGHTS

    @staticmethod
    def set_schema_letters():
        """define the letters and digits which will be part of the schema
        """
        caps = constants.UPPER_CASE
        lower = constants.LOWER_CASE
        digits = constants.DIGITS
        return caps, lower, digits

    def create_polyatom_schema(self):
        """define polyatom, it is element and its number of atoms
        taken together, example C6 is a polyatom in C6H12O6
        """
        caps, lower, digits = self.set_schema_letters()
        alphabet = pyparsing.Word(caps, lower)
        number = pyparsing.Word(digits).setParseAction(self.convert_integers)
        polyatom_schema = pyparsing.Group(alphabet("element")+\
                                pyparsing.Optional(number, default=1)("number_atoms"))
        return polyatom_schema

    def create_chemicalformula_schema(self):
        """define chemical formula schema, its group of polyatoms
        example C6,H12,O6 these three polyatoms together create C6H12O6,
        a chemical formula"""
        polyatom_schema = self.create_polyatom_schema()
        chemformula_schema = pyparsing.OneOrMore(polyatom_schema)
        return chemformula_schema

    def check_if_element(self, element):
        """check existence of element by searching it in the element -> molecular weight
        dictionary
        Args:
            element : the element symbol which is to be checked
        Returns:
            bool : True if element exists
        Raises:
            KeyError : If element doesn't exist
        """

        if element in self.elements_and_molecular_weights:
            return True
        else:
            print("Element does not exist", element)
            raise KeyError

    @staticmethod
    def convert_integers(tokens):
        """convert pyparse tokens to integer"""
        return int(tokens[0])
