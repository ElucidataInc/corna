from scipy.misc import comb
import math

def background_noise(parent_label, na, daughter_atoms, unlabel_intensity):
    if parent_label <= daughter_atoms:
        noise = unlabel_intensity*math.pow(na, parent_label)*comb(daughter_atoms, parent_label)
    else:
        noise = unlabel_intensity*math.pow(na, parent_label)
    return noise
