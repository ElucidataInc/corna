import helpers as hl
import pandas as pd


class MavenParser():

    #def __init__(self):
        #self.path = path


    def read_input_data(self, path):
        """
        This function reads the input data file. The file can be
        csv or xlsx

        Args:
            path to input data file

        Returns:
            input data in the form of pandas dataframe
        """

        input_data = hl.read_file(path)

        return input_data


    def read_metadata(self, path):
        """
        This function reads the metadata file. The file can be
        csv or xlsx

        Args:
            path to metadata file

        Returns:
            metadata in the form of pandas dataframe
        """

        metadata = hl.read_file(path)

        return metadata



    def melt_merge_df(self, df1, df2, left_on="variable", right_on="sample"):
        """
        This function combines the input file dataframe and the metadata
        file dataframe

        Args:
            input_data : input data in form of pandas dataframe

            metadata : metadata in the form of pandas dataframe

        Returns:
            combined_data : dataframe with input data and metadata combined
        """
        id = ["Name", "Formula", "Label"]

        value = [x for x in df1.columns.tolist() if x not in id]

        long_form = pd.melt(df1, id_vars=id, value_vars=value)

        merged_df = pd.merge(long_form, df2, how="left", left_on=left_on,
                                 right_on=right_on)

        merged_df.drop(right_on, axis=1, inplace=True)

        merged_df.rename(columns={"variable":"sample_name"}, inplace=True)

        return merged_df








path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
input_data = MavenParser().read_input_data(path_input)
metadata = MavenParser().read_metadata(path_metadata)
merged_df = MavenParser().melt_merge_df(input_data, metadata)

filter_df = hl.filter_df(merged_df, 'sample_name', 'sample_1')
print filter_df

# input dict : input file + metadata file - convert them to pandas df
# input json : input file + metadata file - convert them to pandas df + combine + output format
