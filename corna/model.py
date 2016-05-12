import numpy as np

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
    def check_if_valid_isotope(self, isotope_list):
        if isinstance(isotope_list, str):
            isotope_list = [isotope_list,]
        for iso in isotope_list:
                print iso
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



class LabelmetabIon():
    pass

class Fragment(Ion, Label):
    def __init__(self, name, formula, charge, label_dict, parent):
        Ion.__init__(self, name, formula, charge)
        Label.__init__(self, label_dict)
        try:
            assert isinstance(parent, LabelmetabIon)
        except AssertionError:
            raise AssertionError('Parent should belong to LabelMetabIon')
        self.parent = parent

    def sensible_label(self):
        formula = self.get_formula()
        for ele, qty in self.label_dict.iteritems():
            try:
                print ele
                if 0 < qty <= formula[ele]:
                    pass
                else:
                    raise OverflowError('Number of labeled atoms must be '
                                        'less than total number of atoms '
                                        'and greater than zero')
            except KeyError:
                raise KeyError('Labeled element not in formula')
        return True
