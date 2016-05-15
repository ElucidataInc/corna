from scipy.misc import comb
import math

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

#def background_correction(sample_name, combined_fragment, unlabeled_fragment):
