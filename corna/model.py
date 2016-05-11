from formula import Formula
import helpers as hl

class Ion():
    def __init__(self, name, formula, charge):
        self.name = name
        self.formula = formula
        self.charge = charge

    def get_formula(self):
        """Parsing formula to store as an element -> number of atoms dictionary"""
        parsed_formula = Formula(self.formula).parse_formula_to_elem_numatoms()
        return parsed_formula

    def number_of_atoms(self, element):
        """Number of atoms of a given element
        Args:
            element : name of the element for which
                number of atoms are to be calculated
        Returns:
            num_atoms : number of atoms of the element
        Raises:
            KeyError : if element doesn't exist in the
                formula
        """
        parsed_formula = self.get_formula()
        try:
            num_atoms = parsed_formula[element]
            return num_atoms
        except KeyError:
            raise KeyError("Element not in formula", element)

    def get_mol_weight(self):
        parsed_formula = self.get_formula()
        mw=0
        for sym,qty in parsed_formula.iteritems():
            mw = mw + hl.get_atomic_weight(sym)*qty
        return mw

class Label():
    def __init__(self, isotope_dict):
        self.isotope_dict = isotope_dict
        #create a constant dict for isotopes
        #isotope -> mass

    def get_num_labeled_atoms(self, element, label_dict):
        try:
            num_atoms = label_dict[element]
            if num_atoms == 0:
                raise ValueError('Number of atoms cant be zero')
            else:
                return num_atoms
        except KeyError:
            raise KeyError('Element not labeled')

