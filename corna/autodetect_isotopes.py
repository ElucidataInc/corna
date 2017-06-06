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
    """calculate molecular weight
        Returns:mol_wt (float): molecular weight
    """
    parsed_formula = parse_formula(formula)
    mol_wt = 0
    for sym, qty in parsed_formula.iteritems():
        mol_wt = mol_wt + hl.get_atomic_weight(sym) * qty
    return mol_wt

