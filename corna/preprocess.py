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

