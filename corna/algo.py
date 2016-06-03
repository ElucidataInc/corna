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
m_size = 3
nAtom_cor = 2
el_excluded = []
iso_tracer = 'C'
data = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205]}
formula_dict = {'C':2, 'H':4, 'O':2}
elem_corr = ['C', 'H', 'O']

def correction_matrix(correction_vector, m_size, nAtom_cor, iso_tracer, data):
	correction_matrix = numpy.zeros((m_size, nAtom_cor+1))

	for i in range(nAtom_cor+1):
	    column = correction_vector[:m_size]
        for nb in range(nAtom_cor-i):
        	column = numpy.convolve(column, data[iso_tracer])[:m_size]
		correction_matrix[:,i] = column
	return correction_matrix

def correction_vector(formula_dict, elem_corr, data):
	correction_vector = []
	for key, value in formula_dict.iteritems():
		if key in elem_corr:
			for i in range(0, len(data[key])):
				print key, data[key][i]

			#math.factorial(sum(f)) * ((p[0] ** f[0]) / math.factorial(f[0])) * ((p[1] ** f[1]) / math.factorial(f[1]))


correction_vector(formula_dict, elem_corr, data)



