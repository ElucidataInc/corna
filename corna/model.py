import numpy as np

from formulaschema import FormulaSchema
from formula import Formula
import helpers as hl


class Ion():
    def __init__(self, name, formula):
        self.name = name
        self.formula = formula

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
    def check_if_valid_isotope(self, isotope_list):
        if isinstance(isotope_list, str):
            isotope_list = [isotope_list,]
        for iso in isotope_list:
                hl.get_isotope(iso)
        return True

    def get_num_labeled_atoms(self, isotope, label_dict):
        self.check_if_valid_isotope(isotope)
        if isotope == hl.get_isotope_natural(isotope):
            return 0
        try:
            return label_dict[isotope]
        except KeyError:
            raise KeyError('Isotope not present in label dictionary')

    def get_label_from_mass(self, isotope, molecular_mass, isotopic_mass):
        self.check_if_valid_isotope(isotope)
        nat_iso = hl.get_isotope_natural(isotope)
        if nat_iso == isotope:
            return 0
        atom_excess_mass = hl.get_isotope_mass(isotope) - hl.get_isotope_mass(nat_iso)
        number_label = int(round((isotopic_mass - molecular_mass)/atom_excess_mass))
        return number_label


class Fragment(Ion, Label):
    def __init__(self, name, formula, parent, **kwargs):
        Ion.__init__(self, name, formula)
        self.parent = parent
        if kwargs.has_key('label_dict'):
            self.label_dict = kwargs['label_dict']
        elif kwargs.has_key('isotracer') and kwargs.has_key('isotope_mass'):
            isotope = kwargs['isotracer']
            isotope_mass = kwargs['isotope_mass']
            if kwargs.has_key('molecular_mass'):
                mol_mass = kwargs['molecular_mass']
                self.label_dict = self.create_label_dict_given_mol_mass(isotope, isotope_mass, mol_mass)
            elif kwargs.has_key('mode'):
                mode = kwargs['mode']
                self.label_dict = self.create_label_dict_from_mass(isotope, isotope_mass, mode)
        else:
            raise KeyError('Fragment should contain label information')
        self.check_if_valid_label(self.label_dict)

    def get_elem_num(self, label_dict):
        polyatomschema = FormulaSchema().create_polyatom_schema()
        elem_num = {}
        for iso in label_dict.keys():
            polyatomdata = polyatomschema.parseString(iso)
            polyatom = polyatomdata[0]
            try:
                elem_num[polyatom.element] = elem_num[polyatom.element] + label_dict[iso]
            except KeyError:
                elem_num[polyatom.element] = label_dict[iso]

        return elem_num

    def check_if_valid_label(self, label_dict):
        elem_num = self.get_elem_num(label_dict)
        formula = self.get_formula()
        for ele, num in elem_num.iteritems():
            try:
                if 0 <= num <= formula[ele]:
                        pass
                else:
                        raise OverflowError('Number of labeled atoms must be '
                                        'less than/equal to total number of atoms')
            except KeyError:
                raise KeyError('Labeled element not in formula')
        return True

    def effective_mol_mass(self, mode):
        if mode == 'pos':
            eff_mol_mass = self.get_mol_weight() + 1
        elif mode == 'neg':
            eff_mol_mass = self.get_mol_weight() - 1
        else:
            raise TypeError('Only two modes possible -> pos/neg')
        return eff_mol_mass

    def create_label_dict_from_mass(self, isotope, isotopic_mass, mode):
        molecular_mass = self.effective_mol_mass(mode)
        num = self.get_label_from_mass(isotope, molecular_mass, isotopic_mass)
        return {isotope: num}

    def create_label_dict_given_mol_mass(self, isotope, isotopic_mass, mol_mass):
        num = self.get_label_from_mass(isotope, mol_mass, isotopic_mass)
        return {isotope: num}