import re
import numpy

def parse_formula(f):
    """
    Parse the elemental formula pand return the number
    of each element in a dictionnary d={'El_1':x,'El_2':y,...}.
    """
    s = "(" + "|".join(data.keys()) + ")([0-9]{0,})"
    d = dict((el,0) for el in data.keys())
    for el,n in re.findall(s,f):
        if n:
            d[el] += int(n)
        else:
            d[el] += 1
    return d

def calc_mdv(el_dict_meta, el_dict_der):
    """
    Calculate a mass distribution vector (at natural abundancy),
    based on the elemental compositions of both metabolite's and
    derivative's moieties.
    The element corresponding to the isotopic tracer is not taken
    into account in the metabolite moiety.
    """
    result = [1.]
    for el,n in el_dict_meta.iteritems():
        if el not in [el_cor, el_excluded]:
            for i in range(n):
                result = numpy.convolve(result, data[el])
    for el,n in el_dict_der.iteritems():
        for i in range(n):
            result = numpy.convolve(result, data[el])

    return list(result)

# data_iso / isotop
data = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015]}
#chemical formulaof metabolite
f = 'C6H12'
der = ''
# no of atoms in chemical formula
el_dict_meta = parse_formula(f)
el_dict_der = parse_formula(der)
# isotopic tracer
el_cor = ['C']
# elements not to be included for correction
el_excluded = ['H']
# mass distribution vector
result = calc_mdv(el_dict_meta, el_dict_der)
print result
