import corna.isotopomer as iso
from corna.model import Fragment

class TestFragmentClass:
    @classmethod
    def setup_class(cls):
        cls.fragment = Fragment('Glucose', 'C6H12O6')
        cls.frag_key = 'glucose_C6H12O6'
        cls.label_dict = {'C13':4}
        cls.label_key = 'C13_4'

    @classmethod
    def teardown_class(cls):
        del cls.fragment
        del cls.frag_key

    def test_create_fragment(self):
        assert isinstance(iso.create_fragment('glucose', 'C6H12O6')[self.frag_key], Fragment)

    def test_create_isotopomer_label(self):
        assert iso.create_isotopomer_label({self.frag_key: self.fragment}, self.label_dict)[0][self.frag_key]\
               == {self.label_key:self.label_dict}

    # def test_create_isotopomer_from_label():
    #     isotopomer, label_dicts, frag_dict = iso.create_isotopomers_from_label('glucose', 'C6H12O6', [{'C13':2}, {'C13':3}, {'C13':4}])
    #     frag = 'glucose_C6H12O6'
    #     assert isotopomer[frag] == ['C13_2', 'C13_3', 'C13_4']