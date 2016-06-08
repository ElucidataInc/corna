import os
import warnings
import operator
import numpy
import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import algorithms as algo
import postprocess as postpro
import output as out
#from collections import defaultdict
from formulaschema import FormulaSchema
#import algo as al
import corna


polyatomschema = FormulaSchema().create_polyatom_schema()

warnings.simplefilter(action = "ignore")
# setting relative path
basepath = os.path.dirname(__file__)
#data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))
data_dir ='/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data_agios/'

# Maven

# read files
input_data = hl.read_file(data_dir + '/data_multiple_tracers.csv')

# metadata
metadata = hl.read_file(data_dir + '/metadata.csv')

# merge data file and metadata
merged_df = fp.maven_merge_dfs(input_data, metadata)

# filter df if reqd , given example
filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')

# std model maven
std_model_mvn = fp.standard_model(merged_df, parent = False)

fragments_dict = {}
for frag_name, label_dict in std_model_mvn.iteritems():
	fragments_dict.update(iso.bulk_insert_data_to_fragment(frag_name, label_dict, mass=False, number=True, mode=None))


#{ sample1: { 0 : val, 1: value }, sample2:


universe_values = fragments_dict.values()
sample_list = []
for uv in universe_values:
	samples = uv[1].keys()
	sample_list.extend(samples)
sample_list = list(set(sample_list))

tracers = ['C13', 'N15']
outer_dict = {}
for s in sample_list:
	dict_s = {}
	for uv_new in universe_values:
		tup = ()
		for x in tracers:
			tup = tup + (uv_new[0].get_num_labeled_atoms_isotope(str(x)),)
		dict_s[tup] = uv_new[1][s]

	outer_dict[s] = dict_s
#print outer_dict


#print outer_dict

#iso_tracer
iso_trac = ['C13', 'N15']
iso_tracers = []
for i in range(0, len(iso_trac)):
	polyatomdata = polyatomschema.parseString(iso_trac[i])
	polyatom = polyatomdata[0]
	iso_tracers.append(polyatom.element)
print iso_tracers

# formula dict
formula_dict = {}
for key, value in fragments_dict.iteritems():
	formula_dict =  value[0].get_formula()


#element_correc
eleme_corr = {'C': ['H', 'O'], 'N': ['S']}

#na dict
na_dict = {'C': [0.99, 0.011], 'H' : [0.99, 0.00015], 'O': [0.99757, 0.00038, 0.00205], 'N': [0.99636, 0.00364], 'S': [0.922297, 0.046832, 0.030872]}

#dict2 = {s1{0:v1, 1:v2}, s2 ...}
dict2 = {}


for key, value in outer_dict.iteritems():
	iso_tracer = iso_tracers[0]

	no_atom_tracer = formula_dict[iso_tracer]
	sorted_keys = value.keys()
	sorted_keys.sort(key = lambda x: x[1])

	keys_tracer1 = sorted_keys[:no_atom_tracer+1]
	keys_tracer1.sort(key = lambda x: x[0])

	#print list(set(sorted_keys) - set(keys_tracer1))

	intens = []

	for keys in keys_tracer1:
		intens.append(value[keys])

	intensities = numpy.concatenate(numpy.array(intens))

	correction_vector = algo.calc_mdv(formula_dict, iso_tracer, eleme_corr, na_dict)

	correction_matrix = algo.corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)

	icorr = algo.na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

	#intensities = icorr

	dict1 = {}
	for i in range(0, len(icorr)):
		dict1[i] = icorr[i]

	dict2[key] = dict1


final_dict={}
iso_tracer = iso_tracers[1]
no_atom_tracer = formula_dict[iso_tracer]
for key, value in dict2.iteritems():
	final_dict1 = {}
	for corr_key, corr_val in value.iteritems():
		intens = []

		for orig_key, orig_value in outer_dict[key].iteritems():

			if corr_key == orig_key[0]:
				if orig_key[1] == 0:
					intens.append((orig_key, corr_val))
				else:
					intens.append((orig_key, orig_value))
		intens.sort(key = lambda x:x[0])
		#for x in (intens):
		intensities = [intens[0][1], intens[1][1]]

		correction_vector = algo.calc_mdv(formula_dict, iso_tracer, eleme_corr, na_dict)

		correction_matrix = algo.corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)

		icorr = algo.na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

		for i in range(0,len(icorr)):
			final_dict1[(corr_key, i)] = icorr[i]
	final_dict[key] = final_dict1

#print final_dict

univ_new = final_dict.values()
inverse_sample = []
for un_new in univ_new:
	inverse_sample.extend(un_new.keys())
inverse_sample = list(set(inverse_sample))

#dict_inverse = {0 :{s1: [], s2: []}, 1: {s1: [], s2: []}}
dict_inverse = {}
for inv in inverse_sample:
	sample_dict = {}
	for sample_tr in final_dict.keys():
		k = final_dict[sample_tr][inv]
		sample_dict[sample_tr] = numpy.array([k])
	dict_inverse[inv] = sample_dict

#fragment dict model
new_fragment_dict = {}
for key, value in fragments_dict.iteritems():
	tup_key = (value[0].get_num_labeled_atoms_isotope(tracers[0]),
		value[0].get_num_labeled_atoms_isotope(tracers[1]))
	new_fragment_dict[key] = [value[0], dict_inverse[tup_key], value[2], value[3]]
#std_model_back = iso.fragment_dict_to_std_model(new_fragment_dict, number=True)
na_corr_df = corna.convert_to_df(new_fragment_dict, all=False, colname = 'NAcorr')

#print na_corr_df










