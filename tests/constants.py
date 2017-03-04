import os

dir_path = os.path.dirname(os.path.abspath(__file__))

maven_file = os.path.join(dir_path, "test_input_validation_data","test_maven_upload_acetic.csv")
metadata_file = os.path.join(dir_path, "test_input_validation_data","metadata_sample_test_maven.csv")
test_df_path_all_correct = os.path.join(dir_path, "test_input_validation_data","test_mergedf_all_correct.csv")
test_df_path_no_metadata = os.path.join(dir_path, "test_input_validation_data","test_mergedf_no_metadata.csv")
maven_file_intensity_incorrect = os.path.join(dir_path, "test_input_validation_data","test_maven_upload_acetic_intensity_incorrect.csv")
test_df_path_warning = os.path.join(dir_path, "test_input_validation_data","test_mergedf_warning.csv")
maven_file_path_extra_sample = os.path.join(dir_path, "test_input_validation_data","test_maven_upload_acetic_extra_sample.csv")
maven_file_path_empty_intersection = os.path.join(dir_path, "test_input_validation_data","test_maven_upload_acetic_empty_intersection.csv")
