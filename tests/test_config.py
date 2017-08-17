import corna.config as con

def test_config_variables():
	
	assert con.NAME_COL == 'Name'
	assert con.FORMULA_COL == 'Formula'
	assert con.LABEL_COL == 'Label'
	assert con.INTENSITY_COL == 'Intensity'
	assert con.SAMPLE_COL == 'Sample Name'
	assert con.PARENT_COL == 'Unlabeled Fragment'
	assert con.FRAG_COL == 'frag_keys'
	assert con.MASSINFO_COL == 'Mass Info'
	assert con.ISOTRACER_COL == 'Isotopic Tracer'
	assert con.PARENT_FORMULA_COL == 'Parent Formula'
	assert con.COHORT_COL == 'Cohort Name'
	assert con.MQ_FRAGMENT_COL == 'Component Name'
	assert con.MQ_SAMPLE_NAME == 'Original Filename'
	assert con.MQ_COHORT_NAME == 'Sample Name'
	assert con.BACKGROUND_COL == 'Background Sample'
