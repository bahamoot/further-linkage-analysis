import os
import filecmp
import linkana.settings as lka_const
from linkana.test.template import SafeGeneralTester
from linkana.app import list_POTEC_gene_from_one_member


class TestApp(SafeGeneralTester):

    def __init__(self, test_name):
        SafeGeneralTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'app'

    def __create_app_instance(self):
        pass

    def test_list_POTEC_gene_from_one_member(self):
        self.init_test('test_list_POTEC_gene_from_one_member')
        out_file = os.path.join(self.working_dir,
                                'POTEC_out.txt')
        list_POTEC_gene_from_one_member(out_file)
        expected_out_file = os.path.join(self.data_dir,
                                         'expected_POTEC_list.txt')
        self.assertTrue(filecmp.cmp(out_file, expected_out_file),
                        "POTEC gene is correctly listed")
#        test_dir = os.path.join(self.data_dir, 'test_parse_dir_path')
#        path1 = os.path.join(test_dir, 'Co35.tab.csv')
#        dir_info = analyzer.parse_dir_path(path1)
#        self.assertTrue(dir_info is None,
#                        'Incorrect directory name parsing')
#        path2 = os.path.join(test_dir, 'family0008_chr18')
#        dir_info = analyzer.parse_dir_path(path2)
#        self.assertEqual(dir_info['fam_code'],
#                         '0008',
#                         'Incorrect family code parsing')
#        self.assertEqual(dir_info['chrom'],
#                         '18',
#                         'Incorrect chromosome parsing')
#        self.assertEqual(dir_info['dir_path'],
#                         path2,
#                         'Incorrect full directory path')

