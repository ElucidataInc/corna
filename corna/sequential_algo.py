import numpy
import algorithms as algo


def correction_tracer1_species1(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    na_dict = {'H': [0.00015, 0.99], 'C': [0.05, 0.95], 'S': [0.030872, 0.046832, 0.922297], 'O': [0.00205, 0.00038, 0.99757], 'N': [0.2, 0.8]}
    samp_lab_dict = algo.samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    # this onwards tracer C, N goes
    iso_tracers = trac_atoms

    formula_dict = algo.formuladict(merged_df)

    fragments_dict = algo.fragmentsdict_model(merged_df)

    correc_inten_dict1 = {}
    for samp_name, lab_dict in samp_lab_dict.iteritems():
        iso_tracer = iso_tracers[0]

        no_atom_tracer = formula_dict[iso_tracer]
        #sorted tuples by tracer 2
        sorted_keys = lab_dict.keys()
        sorted_keys.sort(key = lambda x: x[1])
        # get intensities for one tracer only
        keys_tracer1 = sorted_keys[:no_atom_tracer+1]
        # sort tuples by tracer 1 00, 10, 20, 30, 40, 50..soon
        keys_tracer1.sort(key = lambda x: x[0])

        #print list(set(sorted_keys) - set(keys_tracer1))

        intens = []

        for keys in keys_tracer1:
            intens.append(lab_dict[keys])

        intensities = numpy.concatenate(numpy.array(intens))

        icorr = algo.perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = False)

        inten_index_dict = {}
        for i in range(0, len(icorr)):
            inten_index_dict[i] = icorr[i]

        correc_inten_dict1[samp_name] = inten_index_dict

    return correc_inten_dict1



def correction_tracer1_species2(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    na_dict = {'H': [0.00015, 0.99], 'C': [0.05, 0.95], 'S': [0.030872, 0.046832, 0.922297], 'O': [0.00205, 0.00038, 0.99757], 'N': [0.2, 0.8]}

    samp_lab_dict = algo.samp_label_dcit(iso_tracers, merged_df)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    # this onwards tracer C, N goes
    iso_tracers = trac_atoms

    formula_dict = algo.formuladict(merged_df)

    fragments_dict = algo.fragmentsdict_model(merged_df)
    correc_inten_dict2 = {}
    for samp_name, lab_dict in samp_lab_dict.iteritems():
        iso_tracer = iso_tracers[0]

        no_atom_tracer = formula_dict[iso_tracer]
        #sorted tuples by tracer 2
        sorted_keys = lab_dict.keys()
        sorted_keys.sort(key = lambda x: x[1])
        # get intensities for one tracer only
        keys_tracer1 = sorted_keys[:no_atom_tracer+1]
        # sort tuples by tracer 1 00, 10, 20, 30, 40, 50..soon
        keys_tracer1.sort(key = lambda x: x[0])

        keys_tracer2 = list(set(sorted_keys) - set(keys_tracer1))
        keys_tracer2.sort(key = lambda x: x[0])

        intens = []

        for keys in keys_tracer2:
            intens.append(lab_dict[keys])

        intensities = numpy.concatenate(numpy.array(intens))
        print 'matrix2'
        print formula_dict
        print iso_tracer
        icorr = algo.perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = False)

        inten_index_dict = {}
        for i in range(0, len(icorr)):
            inten_index_dict[keys_tracer2[i]] = icorr[i]

        correc_inten_dict2[samp_name] = inten_index_dict

    return correc_inten_dict2


def correction_tracer2(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False):
    na_dict = {'H': [0.00015, 0.99], 'C': [0.05, 0.95], 'S': [0.030872, 0.046832, 0.922297], 'O': [0.00205, 0.00038, 0.99757], 'N': [0.2, 0.8]}

    formula_dict = algo.formuladict(merged_df)
    fragments_dict = algo.fragmentsdict_model(merged_df)

    correc_inten_dict1 = correction_tracer1_species1(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False)
    print correc_inten_dict1
    correc_inten_dict2 = correction_tracer1_species2(merged_df, iso_tracers, eleme_corr, na_dict, optimization = False)

    trac_atoms = algo.get_atoms_from_tracers(iso_tracers)
    #iso_tracers = trac_atoms
    iso_tracer = trac_atoms[1]
    no_atom_tracer = formula_dict[iso_tracer]

    corr_intensities_dict = {}
    for samp_name, lab_dict in correc_inten_dict1.iteritems():
        intens_idx_dict = {}
        for corr_key, corr_val in lab_dict.iteritems():
            intens = []

            for orig_key, orig_value in correc_inten_dict2[samp_name].iteritems():

                if corr_key == orig_key[0]:
                    #intens.append([(corr_key, corr_val), (orig_key, orig_value)])
                    #if orig_key[1] == 0:
                    intens.append((orig_key, corr_val))
                else:
                    intens.append((orig_key, orig_value))
            intens.sort(key = lambda x:x[0])

            #intensities = []
            #for i in range(0, len(intens)):
                #intensities.append(intens[i][1])
            intensities = [intens[0][1], intens[1][1]]
            #print intensities

            icorr = algo.perform_correction(formula_dict, iso_tracer, eleme_corr, no_atom_tracer, na_dict, intensities, optimization = False)

            for i in range(0,len(icorr)):
                intens_idx_dict[(corr_key, i)] = icorr[i]
        corr_intensities_dict[samp_name] = intens_idx_dict
        print corr_intensities_dict
    sample_list = algo.check_samples_ouputdict(corr_intensities_dict)
    # { 0: { sample1 : val, sample2: val }, 1: {}, ...}
    lab_samp_dict = algo.label_sample_dict(sample_list, corr_intensities_dict)

    nacorr_dict_model = algo.fragmentdict_model(iso_tracers, fragments_dict, lab_samp_dict)

    return nacorr_dict_model







