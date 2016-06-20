
import numpy as np
import helpers as hl
import numpy
import math
from scipy import optimize
import file_parser as fp
import isotopomer as iso
from formulaschema import FormulaSchema



polyatomschema = FormulaSchema().create_polyatom_schema()

# MULTIQUANT
def na_correct_mimosa_algo(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    p = parent_frag_m.get_number_of_atoms_isotope(isotope)
    d = daughter_frag_n.get_number_of_atoms_isotope(isotope)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()

    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))
    return np.around(corrected_intensity, decimals)

def na_correct_mimosa_algo_array(parent_frag_m, daughter_frag_n, intensity_m_n, intensity_m_1_n, intensity_m_1_n_1,
                      isotope, na, decimals):
    p = parent_frag_m.get_number_of_atoms_isotope(isotope)
    d = daughter_frag_n.get_number_of_atoms_isotope(isotope)
    m = parent_frag_m.get_num_labeled_atoms_tracer()
    n = daughter_frag_n.get_num_labeled_atoms_tracer()
    corrected_intensity = intensity_m_n * (1+na*(p-m)) - intensity_m_1_n * na * ((p-d) - (m-n-1)) -\
                         intensity_m_1_n_1 * na * (d - (n-1))

    return np.around(corrected_intensity, decimals)

def arrange_fragments_by_mass(fragments_dict):
    fragment_dict_mass = {}
    for key, value in fragments_dict.iteritems():
        parent_frag, daughter_frag = value[0]
        fragment_dict_mass[(parent_frag.isotope_mass, daughter_frag.isotope_mass)] = value
    return fragment_dict_mass

def na_correction_mimosa_by_fragment(fragments_dict, decimals):
    fragment_dict_mass = arrange_fragments_by_mass(fragments_dict)
    corrected_dict_mass = {}
    for key, value in fragment_dict_mass.iteritems():
        m_1_n = (key[0]-1, key[1])
        m_1_n_1 = (key[0]-1, key[1]-1)
        parent_frag_m, daughter_frag_n = value[0]
        isotope = parent_frag_m.isotope
        na = hl.get_isotope_na(isotope)
        data = value[1]
        corrected_data = {}
        for sample_name, intensity_m_n in data.iteritems():
            try:
                intensity_m_1_n = fragment_dict_mass[m_1_n][1][sample_name]
            except KeyError:
                intensity_m_1_n = np.zeros(len(intensity_m_n))
            try:
                intensity_m_1_n_1 = fragment_dict_mass[m_1_n_1][1][sample_name]
            except KeyError:
                intensity_m_1_n_1 = np.zeros(len(intensity_m_n))
            corrected_data[sample_name] = na_correct_mimosa_algo_array(parent_frag_m,
                                        daughter_frag_n, intensity_m_n, intensity_m_1_n,
                                        intensity_m_1_n_1, isotope, na, decimals)

        corrected_dict_mass[key] = [value[0], corrected_data, value[2], value[3]]
    return corrected_dict_mass

# MAVEN





def excluded_elements(iso_tracer, formula_dict, eleme_corr):
    el_excluded = []
    for key, value in formula_dict.iteritems():
        if iso_tracer in eleme_corr.keys():
            if key not in eleme_corr[iso_tracer]:
                el_excluded.append(key)
    return el_excluded


def calc_mdv(formula_dict, iso_tracer, eleme_corr, na_dict):
    """
    Calculate a mass distribution vector (at natural abundancy),
    based on the elemental compositions of both metabolite's and
    derivative's moieties.
    The element corresponding to the isotopic tracer is not taken
    into account in the metabolite moiety.
    """
    el_excluded = excluded_elements(iso_tracer, formula_dict, eleme_corr)

    correction_vector = [1.]
    for el, n in formula_dict.iteritems():

        if not el == iso_tracer and el not in el_excluded:

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

        if not eleme_corr:
            correction_vector = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            column = correction_vector[:no_atom_tracer+1]
        else:
            column = correction_vector[:no_atom_tracer+1]
        #for na in range(i):
            #column = numpy.convolve(column, el_pur)[:no_atom_tracer+1]
        if el_excluded != iso_tracer:
            for nb in range(no_atom_tracer-i):
                #na_dict[iso_tracer] = [0.99, 0.011]
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


def cost_function(corrected_intensites, intensities, correction_matrix):
    """
    Cost function used for BFGS minimization.
        return : (sum(v_mes - mat_cor * corrected_intensites)^2, gradient)
    """
    x = intensities - numpy.dot(correction_matrix, corrected_intensites)
    # calculate sum of square differences and gradient
    return (numpy.dot(x,x), numpy.dot(correction_matrix.transpose(),x)*-2)

def fragmentsdict_model(merged_df):
    fragments_dict = {}
    std_model_mvn = fp.standard_model(merged_df, parent = False)
    for frag_name, label_dict in std_model_mvn.iteritems():
        fragments_dict.update(iso.bulk_insert_data_to_fragment(frag_name, label_dict, mass=False, number=True, mode=None))

    return fragments_dict


def unique_samples_for_dict(merged_df):
    fragments_dict = fragmentsdict_model(merged_df)
    universe_values = fragments_dict.values()
    sample_list = []
    for uv in universe_values:
        samples = uv[1].keys()
        sample_list.extend(samples)
    sample_list = list(set(sample_list))
    return sample_list



def samp_label_dcit(iso_tracers, merged_df):
    """
    Dictionary of the form { sample1: { 0 : val, 1: value }, sample2: {}, ...}
    """
    sample_list = unique_samples_for_dict(merged_df)
    fragments_dict = fragmentsdict_model(merged_df)
    universe_values = fragments_dict.values()
    samp_lab_dict = {}
    for s in sample_list:
        dict_s = {}
        for uv_new in universe_values:
            if len(iso_tracers) == 1:
                lab_num = uv_new[0].get_num_labeled_atoms_isotope(iso_tracers[0])
            elif len(iso_tracers) > 1:
                lab_num = ()
                for isotopes in iso_tracers:
                    lab_num = lab_num + (uv_new[0].get_num_labeled_atoms_isotope(str(isotopes)),)
            dict_s[lab_num] = uv_new[1][s]
        samp_lab_dict[s] = dict_s

    return samp_lab_dict

def formuladict(merged_df):
    fragments_dict = fragmentsdict_model(merged_df)
    formula_dict = {}
    for key, value in fragments_dict.iteritems():
        formula_dict =  value[0].get_formula()

    return formula_dict


def get_atoms_from_tracers(iso_tracers):
    trac_atoms = []
    for i in range(0, len(iso_tracers)):
        polyatomdata = polyatomschema.parseString(iso_tracers[i])
        polyatom = polyatomdata[0]
        trac_atoms.append(polyatom.element)
    return trac_atoms



def perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = True):

    correction_vector = calc_mdv(formula_dict, iso_tracer, eleme_corr, na_dict)

    correction_matrix = corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)

    icorr = na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

    return icorr


def na_corrected_output(merged_df, iso_tracers, eleme_corr, na_dict, optimization = True):
    # tracer C13, N15 goes
    samp_lab_dict = samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = get_atoms_from_tracers(iso_tracers)
    # this onwards tracer C, N goes
    #iso_tracers_el = trac_atoms

    formula_dict = formuladict(merged_df)
    fragments_dict = fragmentsdict_model(merged_df)

    # { sample1: { 0 : val, 1: value }, sample2: {}, ...}
    correc_inten_dict = {}
    for samp_name, label_dict in samp_lab_dict.iteritems():

        intensities = numpy.concatenate(numpy.array((label_dict).values()))

        if len(trac_atoms) == 1:
            iso_tracer = trac_atoms[0]

            no_atom_tracer = formula_dict[iso_tracer]

            icorr = perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = True)
        # { 0 : val, 1: val, 2: val, ...}
        inten_index_dict = {}
        for i in range(0, len(icorr)):
            inten_index_dict[i] = icorr[i]

        correc_inten_dict[samp_name] = inten_index_dict
    sample_list = check_samples_ouputdict(correc_inten_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = label_sample_dict(sample_list, correc_inten_dict)
    nacorr_dict_model = fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model


def check_samples_ouputdict(correc_inten_dict):
    univ_new = correc_inten_dict.values()
    inverse_sample = []
    for un_new in univ_new:
        inverse_sample.extend(un_new.keys())
    inverse_sample = list(set(inverse_sample))
    return inverse_sample

def label_sample_dict(sample_list, correc_inten_dict):
    lab_samp_dict = {}
    for inv in sample_list:
        sample_dict = {}
        for sample_tr in correc_inten_dict.keys():
            k = correc_inten_dict[sample_tr][inv]
            sample_dict[sample_tr] = numpy.array([k])
        lab_samp_dict[inv] = sample_dict
    return lab_samp_dict


    #fragment dict model
def fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict):
    nacorr_fragment_dict = {}
    for key, value in fragments_dict.iteritems():
        if len(iso_tracers) == 1:
            nacorr_fragment_dict[key] = [value[0], lab_samp_dict[value[0].get_num_labeled_atoms_isotope(iso_tracers[0])], value[2], value[3]]
        elif len(iso_tracers) > 1:
            tup_key = (value[0].get_num_labeled_atoms_isotope(iso_tracers[0]),
                value[0].get_num_labeled_atoms_isotope(iso_tracers[1]))
            nacorr_fragment_dict[key] = [value[0], lab_samp_dict[tup_key], value[2], value[3]]

    return nacorr_fragment_dict







