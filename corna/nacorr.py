import os
import warnings
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
from formula import Formula
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
iso_tracers = ['C13']
input_data = hl.read_file(data_dir + '/maven_output.csv')

def convert_labels_to_std(df, iso_tracers):
	new_labels = []
	for labels in input_data['Label']:
		if labels == 'C12 PARENT':
			labe = ''
			for tracs in iso_tracers:
				labe = labe + tracs+'_0_'
			new_labels.append(labe.strip('_'))
		else:
			splitted = labels.split('-label-')
			split2 = splitted[1].split('-')
			isotopelist = Formula(splitted[0]).parse_chemforumla_to_polyatom()
			el1 = (''.join(str(x) for x in isotopelist[0]))
			el1_num = el1 + '_'+ split2[0]
			if len(iso_tracers) == 1:
				new_labels.append(el1_num)

			else:
				try:
					el2 = '_'+(''.join(str(x) for x in isotopelist[1])) + '_' + split2[1]

					el = el1_num+el2
					new_labels.append(el)
				except:
					for tracer in iso_tracers:
						if tracer != el1:
							el = el1_num + '_' + tracer + '_0'
							new_labels.append(el)

	return new_labels
#print new_labels
#print input_data
input_data['Label'] = new_labels
print input_data




#parsed_formula = Formula(formula).parse_formula_to_elem_numatoms()

#input_data = hl.read_file(data_dir + '/data_multiple_tracers.csv')

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

outer_dict = {}
for s in sample_list:
	dict_s = {}
	for uv_new in universe_values:
		num = uv_new[0].get_num_labeled_atoms_isotope('C13')
		dict_s[num] = uv_new[1][s]
	outer_dict[s] = dict_s
#print outer_dict

#iso_tracer
iso_tracers = ['C']
#polyatomdata = polyatomschema.parseString(iso_tracers[0])
#polyatom = polyatomdata[0]
#iso_tracer = polyatom.element

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
	intensities = numpy.concatenate(numpy.array((value).values()))
	if len(iso_tracers) == 1:
	    iso_tracer = iso_tracers[0]

	    no_atom_tracer = formula_dict[iso_tracer]

	    correction_vector = algo.calc_mdv(formula_dict, iso_tracer, eleme_corr, na_dict)

	    correction_matrix = algo.corr_matrix(iso_tracer, formula_dict, eleme_corr, no_atom_tracer, na_dict, correction_vector)

	    icorr = algo.na_correction(correction_matrix, intensities, no_atom_tracer, optimization = True)

	    intensities = icorr

	dict2[key] = icorr

	dict1 = {}
	for i in range(0, len(icorr)):
		dict1[i] = icorr[i]

	dict2[key] = dict1

univ_new = dict2.values()
inverse_sample = []
for un_new in univ_new:
	inverse_sample.extend(un_new.keys())
inverse_sample = list(set(inverse_sample))

#dict_inverse = {0 :{s1: [], s2: []}, 1: {s1: [], s2: []}}
dict_inverse = {}
for inv in inverse_sample:
	sample_dict = {}
	for sample_tr in dict2.keys():
		k = dict2[sample_tr][inv]
		sample_dict[sample_tr] = numpy.array([k])
	dict_inverse[inv] = sample_dict

#fragment dict model
new_fragment_dict = {}
for key, value in fragments_dict.iteritems():
	new_fragment_dict[key] = [value[0], dict_inverse[value[0].get_num_labeled_atoms_isotope('C13')], value[2], value[3]]
#std_model_back = iso.fragment_dict_to_std_model(new_fragment_dict, number=True)
na_corr_df = corna.convert_to_df(new_fragment_dict, colname = 'NAcorr')
print na_corr_df
replace_neg =  postpro.replace_negative_to_zero(new_fragment_dict, replace_negative = True)
erich =  postpro.enrichment(new_fragment_dict, decimals = 2)























# MultiQuant

# read files
data_dir ='/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data_yale/'
mq_df = hl.concat_txts_into_df(data_dir + '/')
#mq_df = hl.concat_txts_into_df('/Users/sininagpal/OneDrive/Elucidata_Sini/Na_corr_demo/data/')
#print mq_df
mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')


# merge mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)
#print merged_data[(merged_data['Name'].isin(['Citrate 197/71','Citrate 191/67'])) & (merged_data['Sample Name'].isin(['A. [13C-glc] G2.5 0min', 'B. [13C-glc] G2.5 5min']))]
#merged_data.to_csv(data_dir + '/merged_mq.csv')

# standard model mq
std_model_mq = fp.standard_model(merged_data, parent = True)


# integrating isotopomer and parser (input is standardised model in form of nested dictionaries)
fragments_dict = {}
for frag_name, label_dict in std_model_mq.iteritems():
    if frag_name[2] == 'Citrate 191/67':
        new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
        fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True, number=False, mode=None))


#preprocessing for a given metabolite
preprocessed_dict = preproc.bulk_background_correction(fragments_dict, ['A. [13C-glc] G2.5 0min', 'B. [13C-glc] G2.5 5min',

                                                     'C. [13C-glc] G2.5 15min', 'D. [13C-glc] G2.5 30min',
                                                     'E. [13C-glc] G2.5 60min', 'F. [13C-glc] G2.5 120min',
                                                     'G. [13C-glc] G2.5 240min', 'H. [6,6-DD-glc] G2.5 240min'],
                                    'A. [13C-glc] G2.5 0min')

# na correction
na_corrected_dict = algo.na_correction_mimosa_by_fragment(preprocessed_dict)

na_corr_dict_std_model =  iso.fragment_dict_to_std_model(na_corrected_dict,mass=True,number=False)

# post processing - replace negative values by zero
# tested on std_model_mvn and std_model_mq - same data format as output from algorithm.py
#post_processed_dict = postpro.replace_negative_to_zero(na_corr_dict_std_model, replace_negative = True)


frac_enrichment = postpro.enrichment(preprocessed_dict)
frac_enr_dict_std_model =  iso.fragment_dict_to_std_model(frac_enrichment,mass=True,number=False)


dict_to_df = out.convert_dict_df(frac_enr_dict_std_model, parent = True)

