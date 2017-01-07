import pandas as pd

import corna.output as out
from corna.isotopomer import Infopacket
from corna.model import Fragment
from corna.inputs.multiquant_parser import Multiquantkey
import corna.isotopomer as iso


def output_constants():
    nest_dict = {out.OutKey(name='L-Methionine', formula='C5H10NO2S'):
                     {'N15_0_C13_5': {'sample_1': 3.156529191428407e-08},
                      'N15_0_C13_4': {'sample_1': -4.6457232333485042e-06},
                      'N15_0_C13_1': {'sample_1': 0.055358607526132128},
                      'N15_0_C13_0': {'sample_1': 0.26081351241574013},
                      'N15_0_C13_3': {'sample_1': 0.00010623115401093528},
                      'N15_0_C13_2': {'sample_1': 0.0045440397693722904},
                      'N15_1_C13_0': {'sample_1': 0.064545716018271096},
                      'N15_1_C13_1': {'sample_1': 0.013283380798059349},
                      'N15_1_C13_2': {'sample_1': 0.00084379489120955248},
                      'N15_1_C13_3': {'sample_1': 6.1161350126415117e-05},
                      'N15_1_C13_4': {'sample_1': -1.8408545189878132e-06},
                      'N15_1_C13_5': {'sample_1': 0.60114017085422033}}}

    acetic_frag = Fragment('Acetic', 'H4C2O2', label_dict={'C13': 1, 'C13': 2})

    fragment_dict = {'Acetic_C13_1': Infopacket(frag='H4C2O2', data={'sample_1': 1}, unlabeled=False, name='Acetic'),
                     'Acetic_C13_2': Infopacket(frag='H4C2O2', data={'sample_1': 0}, unlabeled=False, name='Acetic')}
    metabolite_dict = {('Acetic', 'H4C2O2'): fragment_dict}

    metabolite_dict = {('L-Methionine', 'C5H10NO2S'):
                           {'C13_1': {'sample_1': 3.18407678e-07}, 'C13_0': {'sample_1': 0.48557866}}}

    df = pd.DataFrame({'Sample': {0: 'sample_1', 1: 'sample_1', 2: 'sample_1', 3: 'sample_1', 4: 'sample_1',
                                  5: 'sample_1', 6: 'sample_1', 7: 'sample_1', 8: 'sample_1', 9: 'sample_1',
                                  10: 'sample_1', 11: 'sample_1'}, 'Formula': {0: 'C5H10NO2S', 1: 'C5H10NO2S',
                                                                               2: 'C5H10NO2S', 3: 'C5H10NO2S',
                                                                               4: 'C5H10NO2S', 5: 'C5H10NO2S',
                                                                               6: 'C5H10NO2S', 7: 'C5H10NO2S',
                                                                               8: 'C5H10NO2S', 9: 'C5H10NO2S',
                                                                               10: 'C5H10NO2S', 11: 'C5H10NO2S'},
                       'Intensity': {0: 3.156529191428407e-08, 1: -4.6457232333485042e-06, 2: 0.055358607526132128,
                                     3: 0.26081351241574013, 4: 0.00010623115401093528, 5: 0.0045440397693722904,
                                     6: 0.064545716018271096, 7: 0.013283380798059349, 8: 0.00084379489120955248,
                                     9: 6.1161350126415117e-05, 10: -1.8408545189878132e-06, 11: 0.60114017085422033},
                       'Name': {0: 'L-Methionine', 1: 'L-Methionine', 2: 'L-Methionine', 3: 'L-Methionine',
                                4: 'L-Methionine', 5: 'L-Methionine', 6: 'L-Methionine', 7: 'L-Methionine',
                                8: 'L-Methionine', 9: 'L-Methionine', 10: 'L-Methionine', 11: 'L-Methionine'},
                       'Label': {0: 'N15_0_C13_5', 1: 'N15_0_C13_4', 2: 'N15_0_C13_1', 3: 'N15_0_C13_0',
                                 4: 'N15_0_C13_3', 5: 'N15_0_C13_2', 6: 'N15_1_C13_0', 7: 'N15_1_C13_1',
                                 8: 'N15_1_C13_2', 9: 'N15_1_C13_3', 10: 'N15_1_C13_4', 11: 'N15_1_C13_5'}})
    return nest_dict, df


def algorithms_yale_constants():
    data_input = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1967.77,
                  'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1446.77,
                  'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 747.77,
                  'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1926.77,
                  'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 1969.77,
                  'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 661.77}

    data_unlabel = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 62610,
                    'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 58640,
                    'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 59950,
                    'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 62520,
                    'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 59690,
                    'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 57200}

    corrected_data_input = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': -55.07,
                            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': -456.52,
                            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': -1214.13,
                            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': -94.,
                            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 43.33,
                            'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': -1211.27}

    corrected_data_unlabel = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 64676.13,
                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 60575.12,
                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 61928.35,
                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 64583.16,
                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 61659.77,
                              'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 59087.6}

    unlabeled_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 185/79', 'O3P', '2PG 185/79', 'C3H6O7P'),
                                                          'C13_185.0_79.0', data_unlabel)

    input_fragment = iso.insert_data_to_fragment_mass(Multiquantkey('2PG 186/79', 'O3P', '2PG 185/79', 'C3H6O7P'),
                                                      'C13_186.0_79.0', data_input)

    parent_frag_input = input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][0]
    daughter_frag_input = input_fragment[('2PG 186/79_186.0', '2PG 186/79_79.0')][0][1]

    parent_frag_unlabeled = unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')][0][0]
    daughter_frag_unlabeled = unlabeled_fragment[('2PG 185/79_185.0', '2PG 185/79_79.0')][0][1]

    fragment_dict = dict(unlabeled_fragment, **input_fragment)

    corrected_fragment_dict = {(186.0, 79.0): iso.Infopacket(frag=[parent_frag_input, daughter_frag_input],
                                                             data=corrected_data_input, unlabeled=False,
                                                             name='2PG 185/79'),
                               (185.0, 79.0): iso.Infopacket(frag=[parent_frag_unlabeled, daughter_frag_unlabeled],
                                                             data=corrected_data_unlabel, unlabeled=True,
                                                             name='2PG 185/79')}

    unlabeled_fragment_dhap = iso.insert_data_to_fragment_mass(
        Multiquantkey('DHAP 169/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_169.0_97.0',
        {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 51670,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 52360,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 52540,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 56580,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 52580,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 58990})

    input_fragment_dhap = iso.insert_data_to_fragment_mass(
        Multiquantkey('DHAP 170/97', 'H2O4P', 'DHAP 169/97', 'C3H6O6P'), 'C13_170.0_97.0',
        {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 1292.67,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 901.67,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 1292.67,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 1468.67,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 1511.67,
         'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 1946.67})

    corrected_data_unlabel_dhap = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': 53375.11,
                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': 54087.88,
                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': 54273.82,
                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': 58447.14,
                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': 54315.14,
                                   'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 60936.67}

    corrected_data_input_dhap = {'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 1)': -384.00,
                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 17)': -806.37,
                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 33)': -412.71,
                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 49)': -366.16,
                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 65)': -190.21,
                                 'TA_SCS-ATP BCH_19May16_1June16.wiff (sample 81)': 42.83}

    parent_frag_input_dhap = input_fragment_dhap[('DHAP 170/97_170.0', 'DHAP 170/97_97.0')][0][0]
    daughter_frag_input_dhap = input_fragment_dhap[('DHAP 170/97_170.0', 'DHAP 170/97_97.0')][0][1]

    parent_frag_unlabeled_dhap = unlabeled_fragment_dhap[('DHAP 169/97_169.0', 'DHAP 169/97_97.0')][0][0]
    daughter_frag_unlabeled_dhap = unlabeled_fragment_dhap[('DHAP 169/97_169.0', 'DHAP 169/97_97.0')][0][1]

    corrected_fragment_dict_dhap = {
        (169.0, 97.0): iso.Infopacket(frag=[parent_frag_unlabeled_dhap, daughter_frag_unlabeled_dhap],
                                      data=corrected_data_unlabel_dhap, unlabeled=True, name='DHAP 169/97'),
        (170.0, 97.0): iso.Infopacket(frag=[parent_frag_input_dhap, daughter_frag_input_dhap],
                                      data=corrected_data_input_dhap, unlabeled=False, name='DHAP 169/97')}

    fragment_dict_dhap = dict(unlabeled_fragment_dhap, **input_fragment_dhap)

    metabolite_frag_dict = {'dhap': fragment_dict_dhap, '2pg': fragment_dict}
    corrected_metabolite_dict = {'dhap': corrected_fragment_dict_dhap, '2pg': corrected_fragment_dict}

    return parent_frag_input, daughter_frag_input, \
           fragment_dict, data_input, parent_frag_unlabeled, \
           daughter_frag_unlabeled, data_unlabel, corrected_fragment_dict, metabolite_frag_dict, corrected_fragment_dict_dhap, corrected_fragment_dict
