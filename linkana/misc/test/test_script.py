import os
import filecmp
import unittest
import linkana.settings as lka_const
from linkana.misc.test.template import SafeMiscTester
from linkana.misc.script import summarize_annovar


class TestScript(SafeMiscTester):

    def __init__(self, test_name):
        SafeMiscTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'script'

    def __create_script_instance(self):
        pass

    @unittest.skip("temporary disable due to long testing time")
    def test_summarize_annovar(self):
#        self.individual_debug = True
        self.init_test('test_summarize_annovar')
        test_chrom = '18'
        test_begin_marker = 'rs146647843'
        test_end_marker = 'rs117978838'
        test_tabix_file = os.path.join(self.data_dir,
                                       'test_summarize_annovar.vcf.gz')
        test_working_dir = self.working_dir
        test_out_prefix = 'test_summarize_annovar_out'
        summarize_annovar(test_chrom,
                          test_begin_marker,
                          test_end_marker,
                          test_tabix_file,
                          test_working_dir,
                          test_out_prefix,
                          )
        expected_tmp_avdb_file = os.path.join(self.data_dir,
                                              'expected_tmp_avdb')
        tmp_avdb_file = os.path.join(test_working_dir,
                                     test_out_prefix + '_tmp_avdb')
        self.assertTrue(filecmp.cmp(tmp_avdb_file, 
                                    expected_tmp_avdb_file),
                        "avdb file is incorrectly prepared")
        expected_avdb_file = os.path.join(self.data_dir,
                                          'expected_avdb')
        avdb_file = os.path.join(test_working_dir,
                                 test_out_prefix + '.avdb')
        self.assertTrue(filecmp.cmp(avdb_file, 
                                    expected_avdb_file),
                        "avdb file is incorrectly produced")
        expected_tab_csv_file = os.path.join(self.data_dir,
                                             'expected_tab_csv')
        tab_csv_file = os.path.join(test_working_dir,
                                    test_out_prefix + '.tab.csv')
        self.assertTrue(filecmp.cmp(tab_csv_file, 
                                    expected_tab_csv_file),
                        "incorrect csv output file")


