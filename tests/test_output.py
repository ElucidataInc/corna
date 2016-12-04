import pytest
import pandas as pd
import numpy as np
import numpy.testing as npt
import corna.config as conf
import corna.output as out
from corna.isotopomer import Infopacket
from corna.model import Fragment

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

acetic_frag = Fragment('Acetic','H4C2O2',label_dict={'C13':1, 'C13':2})
#fragments_dict = {'Acetic_C13_0': Infopacket(frag=acetic_frag, data={'sample_1': np.array([ 0.3624])},
#                                 unlabeled=True, name='Acetic')}

fragment_dict = {'Acetic_C13_1': Infopacket(frag='H4C2O2', data={'sample_1': 1}, unlabeled=False, name='Acetic'),
  				 'Acetic_C13_2': Infopacket(frag='H4C2O2', data={'sample_1': 0}, unlabeled=False, name='Acetic')}
metabolite_dict = {('Acetic', 'H4C2O2'):fragment_dict}

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

def test_convert_to_df():
	out_df =  out.convert_dict_df(nest_dict)
	out_df = out_df[['Formula', 'Intensity', 'Label', 'Name', 'Sample']]
	npt.assert_array_equal(out_df, df)
