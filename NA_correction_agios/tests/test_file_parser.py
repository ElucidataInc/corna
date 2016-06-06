import pytest
from corna.file_parser import MavenParser


class TestParser:
	path = ''
	mavenparser_obj = MavenParser(path)

	def test_checks_class(self):
		assert isinstance(self.mavenparser_obj, MavenParser)

	def test_read_file(self):
		with pytest.raises(IOError):
			file_in = self.mavenparser_obj.read_input_data(self.path)
