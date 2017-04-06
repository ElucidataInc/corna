import numpy.testing as npt
import corna.output as out
from data_constants import output_constants

def test_convert_to_df():
	nest_dict, df = output_constants()
	out_df =  out.convert_dict_df(nest_dict)
	out_df = out_df[['Formula', 'Intensity', 'Label', 'Name', 'Sample']]
	npt.assert_array_equal(out_df, df)
