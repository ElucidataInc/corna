import algorithms as algo
import numpy as np




def na_correction(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    samp_lab_dict = algo.samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)

    formula_dict = algo.formuladict(merged_df)
    fragments_dict = algo.fragmentsdict_model(merged_df)



def single_trac_na_correc(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    samp_lab_dict = algo.samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)

    formula_dict = algo.formuladict(merged_df)
    fragments_dict = algo.fragmentsdict_model(merged_df)

    # { sample1: { 0 : val, 1: value }, sample2: {}, ...}
    correc_inten_dict = {}
    for samp_name, label_dict in samp_lab_dict.iteritems():

        intensities = np.concatenate(np.array((label_dict).values()))

        if len(trac_atoms) == 1:
            iso_tracer = trac_atoms[0]

            no_atom_tracer = formula_dict[iso_tracer]

            icorr = algo.perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = True)
        # { 0 : val, 1: val, 2: val, ...}
        inten_index_dict = {}
        for i in range(0, len(icorr)):
            inten_index_dict[i] = icorr[i]

        correc_inten_dict[samp_name] = inten_index_dict
    sample_list = algo.check_samples_ouputdict(correc_inten_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = algo.label_sample_dict(sample_list, correc_inten_dict)
    nacorr_dict_model = fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model

def multi_trac_na_correc(merged_df, iso_tracers, eleme_corr, na_dict):

    labels_std = hl.convert_labels_to_std(merged_df, iso_tracers)
    merged_df['Label'] = labels_std
    sample_label_dict = algo.samp_label_dcit(iso_tracers, merged_df)
    formula_dict = algo.formuladict(merged_df)
    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    fragments_dict = algo.fragmentsdict_model(merged_df)

    if not eleme_corr:
        eleme_corr_list = trac_atoms
    else:
        eleme_corr_list = eleme_corr_to_list(iso_tracers, eleme_corr)

    no_atom_tracers = []
    for i in eleme_corr_list:
        no_atom_tracers.append(formula_dict[i])

    corr_intensities_dict = {}
    for samp_name, lab_dict in sample_label_dict.iteritems():
        intens_idx_dict = {}
        l = [np.arange(x+1) for x in no_atom_tracers]
        tup_list = list(product(*l))

        indist_sp = sum(eleme_corr.values(),[])

        tup_pos = [i for i, e in enumerate(eleme_corr_list) if e in indist_sp]

        intensities_list = filter_tuples(tup_list, lab_dict, tup_pos)

        icorr = multi_label_correc(na_dict, formula_dict, eleme_corr_list, intensities_list)
        print 'corrected inten'
        print icorr
        ############### line below is incorroect dictionary for now
        # to do here, this is input data dict only - to get the icorr values with keys here
        intens_idx_dict = lab_dict

        corr_intensities_dict[samp_name] = intens_idx_dict

    sample_list = algo.check_samples_ouputdict(corr_intensities_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = algo.label_sample_dict(sample_list, corr_intensities_dict)

    nacorr_dict_model = algo.fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model