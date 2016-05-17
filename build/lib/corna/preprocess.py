import math

import numpy
from scipy.misc import comb

import helpers as hl


def background_noise(parent_label, na, daughter_atoms, unlabel_intensity):
    if parent_label <= daughter_atoms:
        noise = unlabel_intensity*math.pow(na, parent_label)*comb(daughter_atoms, parent_label)
    else:
        noise = unlabel_intensity*math.pow(na, parent_label)
    return noise

def backround_subtraction(input_intensity, noise):
    intensity = input_intensity - noise
    if intensity < 0:
        return 0
    else:
        return intensity

def background(sample_name, input_fragment_value, unlabeled_fragment_value):
    parent_frag, daughter_frag = input_fragment_value[0]
    data = input_fragment_value[1]
    parent_label = parent_frag.get_num_labeled_atoms_tracer()
    na = hl.get_isotope_na(parent_frag.isotope)
    daughter_atoms = daughter_frag.get_number_of_atoms_isotope(parent_frag.isotope)
    input_intensities = data[sample_name]
    unlabeled_data = unlabeled_fragment_value[1]
    unlabeled_intensities = unlabeled_data[sample_name]
    background_list = []
    for i in range(len(input_intensities)):
        noise = background_noise(parent_label, na, daughter_atoms, unlabeled_intensities[i])
        background = backround_subtraction(input_intensities[i], noise)
        background_list.append(background)
    return background_list

def background_correction(bacground_list, sample_data):
    background = max(bacground_list)
    corrected_sample_data = {}
    for key, value in sample_data.iteritems():
        new_value = value - background
        new_value[new_value<0]=0
        corrected_sample_data[key] = new_value
    return corrected_sample_data

def bulk_background_correction(fragment_dict, list_of_samples, background_sample):
    input_fragments = []
    unlabeled_fragment = []
    corrected_fragments_dict = {}
    for key, value in fragment_dict.iteritems():
        unlabel = value[2]
        if unlabel:
            unlabeled_fragment.append((key,value))
        else:
            input_fragments.append((key,value))
    assert len(unlabeled_fragment) == 1
    for input_fragment in input_fragments:
        background_list = background(background_sample, input_fragment[1], unlabeled_fragment[0][1])
        sample_data = {}
        data = input_fragment[1][1]
        for sample_name in list_of_samples:
            sample_data[sample_name] = data[sample_name]
        corrected_sample_data = background_correction(background_list, sample_data)
        corrected_fragments_dict[input_fragment[0]] = [input_fragment[1][0], corrected_sample_data,
                                                       input_fragment[1][2]]
    return corrected_fragments_dict