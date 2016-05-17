import corna


path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data/'

mq_files = corna.read_multiquant(path_dir)

mq_metadata = corna.read_multiquant_metadata(path_dir + '/mq_metadata.xlsx')

merge_mq_metdata = corna.merge_mq_metadata(mq_files, mq_metadata)
print merge_mq_metdata


