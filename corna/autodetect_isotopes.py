import pandas as pd
from helpers import get_formula as parse_formula
import helpers as hl
import re
import warnings

mass_diff_dict = {'C13': {'N': 0.00631, 'O': 0.00087, 'H': 0.00292, 'S': 0.004},
                  'N15': {'C': 0.00631, 'O': 0.00087, 'H': 0.00292, 'S': 0.004},
                  'H2' : {'C': 0.00631, 'O': 0.00087, 'N': 0.00292, 'S': 0.004},
                  'S34': {'C': 0.00631, 'O': 0.00087, 'H': 0.00292, 'N': 0.004}
                 }

def get_mol_weight(formula):
    """
    This function returns molecular weight of a metabolite.
    :param formula: formula of the metabolite
    :return: molecular weight (float)
    """
    parsed_formula = parse_formula(formula)
    mol_wt = 0
    for sym, qty in parsed_formula.iteritems():
        mol_wt = mol_wt + hl.get_atomic_weight(sym) * qty
    if mol_wt == 0.0:
        raise Exception ('Molecular weight of a metabolite cannot be zero')
    return mol_wt


def get_ppm_required(formula, delta_m):
    """
    This function calculates the ppm of the machine
    required to distinguish between the two elements
    in a metabolite.
    :param formula: formula of the metabolite
    :param delta_m: mass diff. between the two elements
    :return: required pp
    """
    metabolite_mass = get_mol_weight(formula)
    required_ppm = (1000000) * (delta_m / metabolite_mass)
    return required_ppm


def get_elements_from_formula(formula):
    """
    This functions creates a list of all the elements
    present in the formula
    :param formula:formula of the metabolite
    :return: ele_list: list of elements present in
    the formula
    """
    ele_list = re.findall('([A-Z][a-z]?)', str(formula))
    return ele_list


def raise_warning(ppm_user_input, required_ppm, formula, ele):
    """
    This function raises warning when the required ppm and
    user input ppm are nearly equal.
    :param ppm_user_input: ppm of the machine used by the user
    :param required_ppm:ppm required to distinguish between the two elements
    :param formula:formula for which the elements are distinguished
    :param ele:element for which ppm requirements are measured
    """
    if (required_ppm - 0.5) <= ppm_user_input <= (required_ppm + 0.5):
        warnings.warn('The ppm requirement for ' +
                      ele + ' is at the borderline. Therefore, ' +
                      formula + ' is corrected for ' + ele)


