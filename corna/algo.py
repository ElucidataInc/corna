import numpy
import math

formula = 'C2H4O2'

#formula = abundance(i) = fact( sum (freq(i)) ) * prod( p(i)** f(i) / fact(f(i)) )

# tested correction values comparing to mida 8 yrs paper - correct
#matrix for C2:
#for M1 c13(1):
f = [1,1]
p = [0.011, 0.99]
corr_C_m1 = math.factorial(sum(f)) * ((p[0] ** f[0]) / math.factorial(f[0])) * ((p[1] ** f[1]) / math.factorial(f[1]))

#for M0 c12(2):
f = [0,2]
p = [0.011, 0.99]
corr_C_m1 = math.factorial(sum(f)) * ((p[0] ** f[0]) / math.factorial(f[0])) * ((p[1] ** f[1]) / math.factorial(f[1]))


#for M2 c13(2):
f = [2,0]
p = [0.011, 0.99]
corr_C_m2 = math.factorial(sum(f)) * ((p[0] ** f[0]) / math.factorial(f[0])) * ((p[1] ** f[1]) / math.factorial(f[1]))




# checking for convolution:
c2 = [0.97832, 0.02156, 0.00012]
h4 = [0.99938, 0.00062, 0.00000015, 0.000000000015, 0.00000000000000059]
o2 = [0.995186, 0.000738, 0.00407, 0.00000151, 0.000000416]
c2h4 = numpy.convolve(c2, h4)
c2h4o2 = numpy.convolve(c2h4, o2)[:9]
#correction vector
correction_vector = c2h4o2





#correction matrix:
#len_tracer_data = 3
#no_atom_tracer = 2
len_tracer_data = 5
no_atom_tracer = 4
el_excluded = []
iso_tracer = 'C'
na_dict = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205]}
#formula_dict = {'C':2, 'H':4, 'O':2}
formula_dict = {'C':4, 'H':5, 'O':5}
elem_corr = ['H', 'O']


def excluded_elements(formula_dict, elem_corr):
	el_excluded = []
	for key, value in formula_dict.iteritems():
		if key not in elem_corr:
			el_excluded.append(key)
	return el_excluded


def calc_mdv(formula_dict, iso_tracer, elem_corr):
    """
    Calculate a mass distribution vector (at natural abundancy),
    based on the elemental compositions of both metabolite's and
    derivative's moieties.
    The element corresponding to the isotopic tracer is not taken
    into account in the metabolite moiety.
    """
    el_excluded = excluded_elements(formula_dict, elem_corr)
    correction_vector = [1.]
    for el,n in formula_dict.iteritems():
        if el not in [iso_tracer, el_excluded]:
            for i in range(n):
                correction_vector = numpy.convolve(correction_vector, na_dict[el])

    return list(correction_vector)


def correction_matrix(formula_dict, elem_corr,correction_vector, len_tracer_data, no_atom_tracer, iso_tracer, na_dict):
	el_excluded = excluded_elements(formula_dict, elem_corr)
	correction_matrix = numpy.zeros((len_tracer_data, no_atom_tracer+1))

	for i in range(no_atom_tracer+1):
	    column = correction_vector[:len_tracer_data]
	    if el_excluded != iso_tracer:
	        for nb in range(no_atom_tracer-i):
	        	column = numpy.convolve(column, na_dict[iso_tracer])[:len_tracer_data]

		correction_matrix[:,i] = column

	return correction_matrix



correction_vector = calc_mdv(formula_dict, iso_tracer, elem_corr)
print correction_vector
corr_matrix = correction_matrix(formula_dict, elem_corr,correction_vector, len_tracer_data, no_atom_tracer, iso_tracer, na_dict)
print corr_matrix



