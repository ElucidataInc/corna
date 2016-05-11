import helpers as hl


class MavenParser():

	def __init__(self, path):
		self.path = path


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


	#def combine_data(self, input_data, metadata):
		"""
		This function combines the input file dataframe and the metadata
		file dataframe

		Args:
			input_data : input data in form of pandas dataframe

			metadata : metadata in the form of pandas dataframe

		Returns:
			combined_data : dataframe with input data and metadata combined
		"""

		#combined_data =




path_input = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/maven_output.csv'
path_metadata = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_Correction/Data/metadata.csv'
input_data = MavenParser(path_input).read_input_data(path_input)
print input_data
metadata = MavenParser(path_metadata).read_metadata(path_metadata)
print metadata

# To do:
# read input read_file csv/ xlsx
# read metadata file csv/ xlsx
# combine both dfs
# std form spotfire as output file

# input dict : input file + metadata file - convert them to pandas df
# input json : input file + metadata file - convert them to pandas df + combine + output format