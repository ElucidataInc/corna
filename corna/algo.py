import numpy
import math
from scipy import optimize




def excluded_elements(iso_tracer, formula_dict, eleme_corr):
    el_excluded = []
    for key, value in formula_dict.iteritems():
        if iso_tracer in eleme_corr.keys():
            if key not in eleme_corr[iso_tracer]:
                el_excluded.append(key)
    return el_excluded


def calc_mdv(formula_dict, iso_tracer, eleme_corr):
    """
    Calculate a mass distribution vector (at natural abundancy),
    based on the elemental compositions of both metabolite's and
    derivative's moieties.
    The element corresponding to the isotopic tracer is not taken
    into account in the metabolite moiety.
    """
    el_excluded = excluded_elements(iso_tracer, formula_dict, eleme_corr)

    correction_vector = [1.]
    for el,n in formula_dict.iteritems():
        #if el not in [iso_tracer, el_excluded]:

        if not el == iso_tracer and el not in el_excluded:
        #if el not in el_excluded

            for i in range(n):
                correction_vector = numpy.convolve(correction_vector, na_dict[el])

    return list(correction_vector)


def corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector):

    #no_atom_tracer = formula_dict[iso_tracer]
    el_excluded = excluded_elements(iso_tracer,formula_dict, eleme_corr)
    correction_matrix = numpy.zeros((no_atom_tracer+1, no_atom_tracer+1))
    el_pur = na_dict[iso_tracer]
    el_pur.reverse()

    for i in range(no_atom_tracer+1):
        print iso_tracer
        print no_atom_tracer
        column = correction_vector[:no_atom_tracer+1]
        print column
        #for na in range(i):
            #column = numpy.convolve(column, el_pur)[:no_atom_tracer+1]
        if el_excluded != iso_tracer:
            for nb in range(no_atom_tracer-i):
                column = numpy.convolve(column, na_dict[iso_tracer])[:no_atom_tracer+1]


        correction_matrix[:,i] = column

    return correction_matrix




def na_correction(correction_matrix, intensities, no_atom_tracer, optimization = False):


    if optimization == False:
        matrix = numpy.array(correction_matrix)
        mat_inverse = numpy.linalg.inv(matrix)
        inten_trasp = numpy.array(intensities).transpose()
        corrected_intensites = numpy.dot(mat_inverse, inten_trasp)

    else:
        corrected_intensites, residuum = [], [float('inf')]
        icorr_ini = numpy.zeros(no_atom_tracer+1)
        inten_trasp = numpy.array(intensities).transpose()
        corrected_intensites, r, d = optimize.fmin_l_bfgs_b(cost_function, icorr_ini, fprime=None, approx_grad=0,\
                                           args=(inten_trasp, correction_matrix), factr=1000, pgtol=1e-10,\
                                           bounds=[(0.,float('inf'))]*len(icorr_ini))


    return corrected_intensites


def cost_function(corrected_intensites, intensities, mat_cor):
    """
    Cost function used for BFGS minimization.
        return : (sum(v_mes - mat_cor * corrected_intensites)^2, gradient)
    """
    x = intensities - numpy.dot(correction_matrix, corrected_intensites)
    # calculate sum of square differences and gradient
    return (numpy.dot(x,x), numpy.dot(correction_matrix.transpose(),x)*-2)



#len_tracer_data = 5

#no_atom_tracer = 4

#el_excluded = []

#iso_tracer = 'C'
#iso_tracers = ['C', 'H']
iso_tracers = ['C', 'N']

na_dict = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205], 'N': [0.99636, 0.00364], 'S': [0.922297, 0.046832, 0.030872]}

#C5H10NO2S
formula_dict = {'C':5, 'H':10, 'O':2, 'N': 1, 'S':1}
#formula_dict = {'C':4, 'H':4, 'O':4}


#elem_corr = ['H', 'O']
eleme_corr = {'C': ['H', 'O'], 'N': ['S']}
#eleme_corr = {'C': ['H', 'O']}

intensities = [0.572503, 0.219132, 0.122481, 0.054081, 0.031800, 0]



subset_formula_dict = dict((k, formula_dict[k]) for k in iso_tracers)

max_trac_value_key = max(subset_formula_dict, key = subset_formula_dict.get)

no_atom_tracer = subset_formula_dict[max_trac_value_key]



if len(iso_tracers) == 1:
    iso_tracer = iso_tracers[0]
    correction_vector = calc_mdv(formula_dict, iso_tracer, eleme_corr)
    #print correction_vector
    correction_matrix = corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)

    no_atom_tracer = formula_dict[iso_tracer]
    icorr = na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

    intensities = icorr


# multiple tracer
elif len(iso_tracers) > 1:
    for i in range(0, len(iso_tracers)):
        iso_tracer = iso_tracers[i]

        #no_atom_tracer = formula_dict[iso_tracer]

        correction_vector = calc_mdv(formula_dict, iso_tracer, eleme_corr)

        correction_matrix = corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)


        #intensities = intensities[:no_atom_tracer+1]
        icorr = na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

        intensities = icorr

print icorr



# single tracer - works correctly
#correction_vector = calc_mdv(formula_dict, iso_tracer, elem_corr)

#correction_matrix = corr_matrix(formula_dict, elem_corr,correction_vector, len_tracer_data, no_atom_tracer, iso_tracer, na_dict)

#icorr1 = na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)
#icorr2 = na_correction(correction_matrix, intensities, no_atom_tracer, optimization = False)



#Todo
#1) eleme_corr[iso_tracer] wont work if isotracer not in ele corr dict
#2) len tracer data to be automated ( hard coded right now)



