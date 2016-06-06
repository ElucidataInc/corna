import numpy
import math

formula = 'C4H5O5'


p = [0.9893, 0.0107]

f0 = [4,0]
corr_C_m0 = math.factorial(sum(f0)) * ((p[0] ** f0[0]) / math.factorial(f0[0])) * ((p[1] ** f0[1]) / math.factorial(f0[1]))

f1 = [3,1]
corr_C_m1 = math.factorial(sum(f1)) * ((p[0] ** f1[0]) / math.factorial(f1[0])) * ((p[1] ** f1[1]) / math.factorial(f1[1]))

f2 = [2,2]
corr_C_m2 = math.factorial(sum(f2)) * ((p[0] ** f2[0]) / math.factorial(f2[0])) * ((p[1] ** f2[1]) / math.factorial(f2[1]))

f3 = [1,3]
corr_C_m3 = math.factorial(sum(f3)) * ((p[0] ** f3[0]) / math.factorial(f3[0])) * ((p[1] ** f3[1]) / math.factorial(f3[1]))

f4 = [0, 4]
corr_C_m4 = math.factorial(sum(f4)) * ((p[0] ** f4[0]) / math.factorial(f4[0])) * ((p[1] ** f4[1]) / math.factorial(f4[1]))

corr_vec_C = [corr_C_m0, corr_C_m1, corr_C_m2, corr_C_m3, corr_C_m4]



p = [0.99985, 0.00015]
corr_H_m0 = math.factorial(sum(f0)) * ((p[0] ** f0[0]) / math.factorial(f0[0])) * ((p[1] ** f0[1]) / math.factorial(f0[1]))

f1 = [3,1]
corr_H_m1 = math.factorial(sum(f1)) * ((p[0] ** f1[0]) / math.factorial(f1[0])) * ((p[1] ** f1[1]) / math.factorial(f1[1]))

f2 = [2,2]
corr_H_m2 = math.factorial(sum(f2)) * ((p[0] ** f2[0]) / math.factorial(f2[0])) * ((p[1] ** f2[1]) / math.factorial(f2[1]))

f3 = [1,3]
corr_H_m3 = math.factorial(sum(f3)) * ((p[0] ** f3[0]) / math.factorial(f3[0])) * ((p[1] ** f3[1]) / math.factorial(f3[1]))

f4 = [0, 4]
corr_H_m4 = math.factorial(sum(f4)) * ((p[0] ** f4[0]) / math.factorial(f4[0])) * ((p[1] ** f4[1]) / math.factorial(f4[1]))

corr_vec_H = [corr_H_m0, corr_H_m1, corr_H_m2, corr_H_m3, corr_H_m4]

p = [0.99757, 0.00038, 0.00205]




