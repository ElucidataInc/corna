"""Ion, Label and Fragment class
Ion is given by name and formula of chemical species, label is collection of functions
to validate a label obtained from mass of species or label information given in form of
dictionary. Fragment class inherits these classes. It represnts an Ion with label present in it.
"""
import warnings

import helpers as hl


class Ion():
    """This class implements an Ion species with name
    and formula
    Attributes:
        name (string): Name of the ion
        formula (string): Chemical formula
    """

    def __init__(self, name, formula):
        """initialise Ion class
        Args:
            name (string): Name of the ion
            formula (string): Chemical formula
        """
        self.name = name
        self.formula = formula

    def get_formula(self):
        """Parsing formula to store as an element -> number of atoms dictionary
        Returns:
            parsed_formula (dict): element -> number of atoms"""
        parsed_formula = hl.get_formula(self.formula)
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
            warnings.warn('{} {}'.format("Element not in formula: ", element))
            return 0

    def get_mol_weight(self):
        """calculate molecular weight
        Returns:
            mw (float): molecular weight
        """
        parsed_formula = self.get_formula()
        mw = 0
        for sym, qty in parsed_formula.iteritems():
            mw = mw + hl.get_atomic_weight(sym) * qty
        return mw


class Label():
    """Collection of label validation functions"""

    def check_if_valid_isotope(self, isotope_list):
        """
        Args:
            isotope_list (string/list[string]): list of isotopes
            Example ['C13', 'N15']
        Return:
            bool: if valid returns true else false
        """
        if isinstance(isotope_list, str):
            isotope_list = [isotope_list, ]
        if all(hl.check_if_isotope_in_dict(iso) for iso in isotope_list):
            return True
        else:
            return False

    def get_num_labeled_atoms(self, isotope, label_dict):
        """get number of labeled atoms of an isotope in label dictionary
        Args:
            isotope (string): isotope symbol (eg 'C13')
            label_dict (dict): dictionary of isotope -> number of atoms
            Example {'C13':3, 'N14':5}
        Returns:
            number of atoms of the isotope in label dict
        Raises:
            KeyError: If isotope not present in label dictionary/constants
        """
        if self.check_if_valid_isotope(isotope):
            try:
                return label_dict[isotope]
            except KeyError:
                return 0
        else:
            raise KeyError('Isotope not available in constants', isotope)

    def get_label_from_mass(self, isotope, molecular_mass, isotopic_mass):
        """get label from molecular mass and isotopic mass
        Args:
            isotope (string): isotope symbol (eg 'C13')
            molecular_mass (float): molecular mass of the molecule
            isotopic_mass (float): isotopic mass of the molecule
        Returns:
            number of labeled atoms
        Raises:
            KeyError: If isotope not present in constants
        """
        if self.check_if_valid_isotope(isotope):
            nat_iso = hl.get_isotope_natural(isotope)
            if nat_iso == isotope:
                return 0
            atom_excess_mass = hl.get_isotope_mass(
                isotope) - hl.get_isotope_mass(nat_iso)
            number_label = int(
                round((isotopic_mass - molecular_mass) / atom_excess_mass))
            return number_label
        else:
            raise KeyError('Isotope not available in constants', isotope)


class Fragment(Ion, Label):
    """Combines ion and label information
    Attributes:
        name (string): Name of the ion
        formula (string): Chemical formula
        label_dict (dict): Dictionary containing label information of the ion
        isotope -> number of atoms
    """

    def __init__(self, name, formula, **kwargs):
        """initialise fragment
        Args:
            name (string): Name of the ion
            formula (string): Chemical formula
            kwargs: possible keywords
        Keyword Args:
            label_dict (dict): dictionary isotope -> number of atoms
            isotracer (string): isotope symbol (in case of label from mass, only one isotracer)
            isotope_mass (float): isotopic mass of the molecule
            molecular_mass (float): molecular mass of the molecule
            mode (string): positive or negative mode (pos/neg)
        """
        # TODO: create function to get isotope mass
        Ion.__init__(self, name, formula)
        self.label_dict = self.get_label_dict(**kwargs)

    def __str__(self):
        """represenation of a fragment instance by formula
        Returns:
            formula (string): chemical formula of associated ion
        """
        return self.formula

    def __repr__(self):
        """represenation of a fragment instance by formula
        Returns:
            formula (string): chemical formula of associated ion
        """
        return self.formula

    def get_label_dict(self, **kwargs):
        """get label dictionary from mass or number
        Args:
            kwargs: possible keywords
        Keyword Args:
            label_dict (dict): dictionary isotope -> number of atoms
            isotracer (string): isotope symbol (in case of label from mass, only one isotracer)
            isotope_mass (float): isotopic mass of the molecule
            molecular_mass (float): molecular mass of the molecule
            mode (string): positive or negative mode (pos/neg)
        Returns:
            label_dict (dict) : isotope -> number of atoms
        Raises:
            KeyError : if keyword args not valid
        """
        if kwargs.has_key('label_dict'):
            label_dict = kwargs['label_dict']
        elif kwargs.has_key('isotracer') and kwargs.has_key('isotope_mass'):
            self.isotracer = kwargs['isotracer']
            self.isotope_mass = kwargs['isotope_mass']
            try:
                mol_mass = kwargs['molecular_mass']
            except:
                mol_mass = None
            try:
                mode = kwargs['mode']
            except:
                mode = None
            label_dict = self.create_label_dict_from_mass(self.isotracer, self.isotope_mass,
                                                          mode=mode, molecular_mass=mol_mass)
        else:
            raise KeyError('Fragment should contain label information')
        self.check_if_valid_label(label_dict)
        return label_dict

    def get_elem_num(self, label_dict):
        """get number of atoms corresponding to elements
         in label dictionary
         Args:
             label_dict (dict): dictionary isotope -> number of atoms
         Returns:
             elem_num (dict): dictionary of element -> number of atoms
         example:
            {'C12':2, 'C13':5}, -> {'C':7}
        """
        elem_num = {}
        for iso in label_dict.keys():
            element = hl.get_isotope_element(iso)
            try:
                elem_num[element] = elem_num[element] + label_dict[iso]
            except KeyError:
                elem_num[element] = label_dict[iso]
        return elem_num

    def check_if_valid_label(self, label_dict):
        """check presence of element in formula and if total number of atoms
        corresponding to an element in given formula range
        Args:
            label_dict (dict): dictionary isotope -> number of atoms
        Returns:
            bool : true if valid label
        Raises:
            OverflowError: if number of atoms not in valid formula range
            KeyError: if element not in formula
        """
        elem_num = self.get_elem_num(label_dict)
        formula = self.get_formula()
        try:
            if all(0 <= num <= formula[ele] for ele, num in elem_num.iteritems()):
                return True
            else:
                raise OverflowError('Number of labeled atoms must be '
                                    'less than/equal to total number of atoms: '
                                    + self.name + ' ' + self.formula)
        except KeyError:
            warnings.warn('{} {}'.format('Labeled element not in formula: ', self.formula))

    def effective_mol_mass(self, mode, molecular_mass):
        """effective molecular mass in diff mass spec modes
        Args:
            mode (string): positive or negative mode (pos/neg)
            molecular_mass (float): molecular mass of the formula
        Returns:
            eff_mol_mass (float): effective molecular mass, depending on lcms mode
        Raises:
            TypeError: If invalid mode provided
        """
        if molecular_mass == None:
            if mode == 'pos':
                eff_mol_mass = self.get_mol_weight() + 1
            elif mode == 'neg':
                eff_mol_mass = self.get_mol_weight() - 1
            else:
                raise TypeError('Only two modes possible -> pos/neg')
        else:
            if mode == 'pos':
                eff_mol_mass = molecular_mass + 1
            elif mode == 'neg':
                eff_mol_mass = molecular_mass - 1
            else:
                raise TypeError('Only two modes possible -> pos/neg')
        return eff_mol_mass

    def create_label_dict_from_mass(self, isotope, isotopic_mass, mode=None, molecular_mass=None):
        """given an isotope, find number of labeled atoms using difference of
        isotopic mass and effective molecular mass
        Args:
            isotope (string): isotope symbol
            isotopic_mass (float): isotopic mass of the molecule
            mode (string): positive or negative mode (pos/neg)
            molecular_mass (float): molecular mass of the molecule
        Returns:
            label_dict (dict): isotope -> number of atoms
        """
        if mode != None:
            molecular_mass = self.effective_mol_mass(mode, molecular_mass)
        elif molecular_mass == None:
            molecular_mass = self.get_mol_weight()
        num = self.get_label_from_mass(isotope, molecular_mass, isotopic_mass)
        return {isotope: num}

    def check_if_unlabel(self):
        """say dict is unlabel if it contains no label isotopes are zero
        Returns:
            bool: if unlabel true else false
        """
        if all(hl.get_isotope_natural(key) == key or value == 0
               for key, value in self.label_dict.iteritems()):
            return True
        else:
            return False

    def get_num_labeled_atoms_isotope(self, isotope):
        """get number of labeled atoms corresponding to an isotope
        Args:
            isotope (string): isotope symbol
        Returns:
            num of atoms os the isotope in label dictionary
        """
        return self.get_num_labeled_atoms(isotope, self.label_dict)
