"""Store chemical formula in a desirable format"""
from formulaschema import FormulaSchema


class Formula(object):
    """This class stores a formula string as a
    dictionary

    Attributes:
        formula : formula in string format
        schema_obj : instance of FormulaSchema class
    """

    def __init__(self, formula_string):
        """Initialise class with formula string
        """
        self.formula = formula_string
        self.schema_obj = FormulaSchema()

    def parse_chemforumla_to_polyatom(self):
        """parse chemical formula to return polyatom (group
        of element and number of atoms)
        Returns:
            formula_data : group of polyatoms
        """
        chemformula_schema = self.schema_obj.create_chemicalformula_schema()
        formula_data = chemformula_schema.parseString(self.formula)
        return formula_data

    def parse_formula_to_elem_numatoms(self):
        """convert polyatoms to element -> number of atoms dictionary
        Returns:
            parsed_formula : dictionary of element->no. of atoms corresponding
                to input formula string of the class
        """
        parsed_formula = {}
        formula_data = self.parse_chemforumla_to_polyatom()
        for polyatom in formula_data:
            if self.schema_obj.check_if_element(polyatom.element):
                parsed_formula[polyatom.element] = polyatom.number_atoms

        return parsed_formula
