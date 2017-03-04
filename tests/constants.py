import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

MAVEN_FILE = os.path.join(DIR_PATH, "test_input_validation_data", "test_maven_upload_acetic.csv")

METADATA_FILE = os.path.join(DIR_PATH, "test_input_validation_data", "metadata_sample_test_maven.csv")

TEST_DF_PATH_ALL_CORRECT = os.path.join(DIR_PATH, "test_input_validation_data", "test_mergedf_all_correct.csv")

TEST_DF_PATH_NO_METADATA = os.path.join(DIR_PATH, "test_input_validation_data", "test_mergedf_no_metadata.csv")

MAVEN_FILE_INTENSITY_INCORRECT = os.path.join(DIR_PATH, "test_input_validation_data",
                                              "test_maven_upload_acetic_intensity_incorrect.csv")

TEST_DF_PATH_WARNING = os.path.join(DIR_PATH, "test_input_validation_data", "test_mergedf_warning.csv")

MAVEN_FILE_PATH_EXTRA_SAMPLE = os.path.join(DIR_PATH, "test_input_validation_data",
                                            "test_maven_upload_acetic_extra_sample.csv")

MAVEN_FILE_PATH_EMPTY_INTERSECTION = os.path.join(DIR_PATH, "test_input_validation_data",
                                                  "test_maven_upload_acetic_empty_intersection.csv")

MAVEN_FILE_PATH_DUPLICATE_ENTRY = os.path.join(DIR_PATH, "test_input_validation_data",
                                               "test_maven_upload_duplicate_entry.csv")
