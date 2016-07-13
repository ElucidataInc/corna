"""The MIT License (MIT)

Copyright (c) 2015 Daniel Gopar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


class PyConstObj(object):
    """ Implementation of a constant object in Python """

    # --------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """

        :rtype: object
        """
        for name, value in kwargs.items():
            super(PyConstObj, self).__setattr__(name.upper(), value)

    # --------------------------------------------------------------------------
    def __setattr__(self, name, val):
        """ When trying to set a new value to the constant object """
        # If variable already exists in instance
        if name in self.__dict__:
            raise ValueError("Cannot change value of a constant")
        else:
            super(PyConstObj, self).__setattr__(name.upper(), val)

def const_element_mol_weight_dict():
    """Constant for elem->mol weight dictionary"""
    element_mol_weight_dict = {'H': 1.007940, 'He': 4.002602, 'Li': 6.941000,
                               'Be': 9.012182, 'B': 10.811000, 'C': 12.010700,
                               'N': 14.006700, 'O': 15.999400, 'F': 18.998403,
                               'Ne': 20.179700, 'Na': 22.989770, 'Mg': 24.305000,
                               'Al': 26.981538, 'Si': 28.085500, 'P': 30.973761,
                               'S': 32.065000, 'Cl': 35.453000, 'Ar': 39.948000,
                               'K': 39.098300, 'Ca': 40.078000, 'Sc': 44.955910,
                               'Ti': 47.867000, 'V': 50.941500, 'Cr': 51.996100,
                               'Mn': 54.938049, 'Fe': 55.845000, 'Co': 58.933200,
                               'Ni': 58.693400, 'Cu': 63.546000, 'Zn': 65.409000,
                               'Ga': 69.723000, 'Ge': 72.640000, 'As': 74.921600,
                               'Se': 78.960000, 'Br': 79.904000, 'Kr': 83.798000,
                               'Rb': 85.467800, 'Sr': 87.620000, 'Y': 88.905850,
                               'Zr': 91.224000, 'Nb': 92.906380, 'Mo': 95.940000,
                               'Tc': 98.000000, 'Ru': 101.070000, 'Rh': 102.905500,
                               'Pd': 106.420000, 'Ag': 107.868200, 'Cd': 112.411000,
                               'In': 114.818000, 'Sn': 118.710000, 'Sb': 121.760000,
                               'Te': 127.600000, 'I': 126.904470, 'Xe': 131.293000,
                               'Cs': 132.905450, 'Ba': 137.327000, 'La': 138.905500,
                               'Ce': 140.116000, 'Pr': 140.907650, 'Nd': 144.240000,
                               'Pm': 145.000000, 'Sm': 150.360000, 'Eu': 151.964000,
                               'Gd': 157.250000, 'Tb': 158.925340, 'Dy': 162.500000,
                               'Ho': 164.930320, 'Er': 167.259000, 'Tm': 168.934210,
                               'Yb': 173.040000, 'Lu': 174.967000, 'Hf': 178.490000,
                               'Ta': 180.947900, 'W': 183.840000, 'Re': 186.207000,
                               'Os': 190.230000, 'Ir': 192.217000, 'Pt': 195.078000,
                               'Au': 196.966550, 'Hg': 200.590000, 'Tl': 204.383300,
                               'Pb': 207.200000, 'Bi': 208.980380, 'Po': 209.000000,
                               'At': 210.000000, 'Rn': 222.000000, 'Fr': 223.000000,
                               'Ra': 226.000000, 'Ac': 227.000000, 'Th': 232.038100,
                               'Pa': 231.035880, 'U': 238.028910, 'Np': 237.000000,
                               'Pu': 244.000000, 'Am': 243.000000, 'Cm': 247.000000,
                               'Bk': 247.000000, 'Cf': 251.000000, 'Es': 252.000000,
                               'Fm': 257.000000, 'Md': 258.000000, 'No': 259.000000,
                               'Lr': 262.000000, 'Rf': 261.000000, 'Db': 262.000000,
                               'Sg': 266.000000, 'Bh': 264.000000, 'Hs': 277.000000,
                               'Mt': 268.000000, 'Ds': 281.000000, 'Rg': 272.000000,
                               'Cn': 285.000000, 'Uuq': 289.000000, 'Uuh': 292.000000}

    constant_obj = PyConstObj(elem_mol_weight_dict=element_mol_weight_dict)
    return constant_obj.ELEM_MOL_WEIGHT_DICT

def const_caps():
    """Constant for alphabet upper case"""
    constant_obj = PyConstObj(upper_case="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return constant_obj.UPPER_CASE

def const_lower():
    """Constant for alphabet lower case"""
    constant_obj = PyConstObj(lower_case="abcdefghijklmnopqrstuvwxyz")
    return constant_obj.LOWER_CASE

def const_digit():
    """Constant for digits"""
    constant_obj = PyConstObj(digits="0123456789")
    return constant_obj.DIGITS

def const_na_dict():
    # na_dict = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015],
    #             'O': [0.99757, 0.00038, 0.00205], 'N': [0.99636, 0.00364],
    #             'S': [0.922297, 0.046832, 0.030872]}
    na_dict = {'H':[0.98,0.01,0.01], 'C': [0.95, 0.05], 'S': [0.922297, 0.046832, 0.030872], \
    'O':[0.95,0.03,0.02], 'N': [0.8, 0.2]}
    const_obj = PyConstObj(na_dict=na_dict)
    return const_obj.NA_DICT

def const_isotope_na_mass():
    isotope_na_mass = {'NA':{'C12':0.989, 'C13':0.011,
                             'N14':0.99636, 'N15':0.00364,
                             'O16':0.99757, 'O17':0.00038, 'O18':0.00205,
                             'H1':0.999885, 'H2':0.000115,
                             'S32':0.9493, 'S33':0.0076, 'S34':0.0429,
                             'P31':1},
                       'Element':{'C12':'C', 'C13':'C',
                                  'N14':'N', 'N15':'N',
                                  'H1':'H', 'H2':'H',
                                  'O16':'O', 'O17':'O', 'O18':'O',
                                  'S32':'S', 'S33':'S', 'S34':'S',
                                  'P31':'P31'},
                       'amu':{'C12':12, 'C13':13,
                              'N14':14, 'N15':15,
                              'O16':16, 'O17':17, 'O18':18,
                              'S32':32, 'S33':33, 'S34':34,
                              'P31':31},
                       'Natural Isotope':{'C12':'C12', 'C13':'C12',
                                  'N14':'N14', 'N15':'N14',
                                  'O16':'O16', 'O17':'O16', 'O18':'O16',
                                  'S32':'S32', 'S33':'S32', 'S34':'S32',
                                  'P31':'P31'}}
    # isotope_na_mass = {'C12': {'NA':0.9893, 'mol_mass':12, 'nat_form': 'C12'},
    #                    'C13': {'NA':0.011, 'mol_mass':13, 'nat_form': 'C12'},
    #                    'C14': {'NA':0, 'mol_mass':14.003241989, 'nat_form': 'C12'},
    #                    'N14': {'NA':0.00364, 'mol_mass':14.003074, 'nat_form': 'N14'},
    #                    'N15': {'NA':0.00364, 'mol_mass':15.0001088982, 'nat_form': 'N14'},
    #                    'O16': {'NA':0.00364, 'mol_mass':15.994915, 'nat_form': 'O16'},
    #                    'O17': {'NA':0.00364, 'mol_mass':16.999132, 'nat_form': 'O17'},
    #                    'O18': {'NA':0.00364, 'mol_mass':17.999160, 'nat_form': 'O18'},
    #                    'H1': {'NA':0.00364, 'mol_mass':1.007825, 'nat_form': 'H1'},
    #                    'H2': {'NA':0.00364, 'mol_mass':2.014102, 'nat_form': 'H1'}}
    const_obj = PyConstObj(isotope_na_mass=isotope_na_mass)
    return const_obj.ISOTOPE_NA_MASS

def const_variable():
    const_obj = PyConstObj(var_col="variable")
    return const_obj.VAR_COL

def const_col_level_0():
    const_obj = PyConstObj(level_0_col="level_0")
    return const_obj.LEVEL_0_COL

def const_col_level_1():
    const_obj = PyConstObj(level_1_col="level_1")
    return const_obj.LEVEL_1_COL

def const_value():
    const_obj = PyConstObj(val_col="value")
    return const_obj.VAL_COL