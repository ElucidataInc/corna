import pytest
from corna.file_parser import MavenParser
from corna.file_parser import fp
import corna.config as conf


#class TestParser:
	#path = ''
	#mavenparser_obj = MavenParser(path)

def test_checks_class(self):
	assert isinstance(self.mavenparser_obj, MavenParser)

def test_read_file(self):
	with pytest.raises(IOError):
		file_in = self.mavenparser_obj.read_input_data(self.path)

def test_cols():
	with pytest.raises(KeyError):
		colnames = fp

