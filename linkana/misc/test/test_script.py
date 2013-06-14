import os
import filecmp
import unittest
import linkana.settings as lka_const
from linkana.misc.test.template import SafeMiscTester
from linkana.misc.script import summarize_annovar
from linkana.misc.script import get_region
from linkana.misc.script import get_region_chrom
from linkana.misc.script import get_raw_vcf_gz_header


class TestScript(SafeMiscTester):

    def __init__(self, test_name):
        SafeMiscTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'script'

    def __create_script_instance(self):
        pass

#    def test_get_raw_vcf_gz_header(self):
#        """ to see if raw vcf header in vcf.gz format is correctly retrieved """
#
#        self.init_test(self.current_func_name)
#        test_file = os.path.join(self.data_dir,
#                                 self.current_func_name + '.vcf.gz')
#        test_begin_marker = 'rs146647843'
#        test_end_marker = 'rs117978838'
#        header = get_raw_vcf_gz_header(test_file)
#        print header

    def test_get_region(self):
        """

        to see if begin position and end position is correcly read for
        the given biomarkers

        """

        self.init_test(self.current_func_name)
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        test_begin_marker = 'rs146647843'
        test_end_marker = 'rs117978838'
        (begin_pos, end_pos) = get_region(test_begin_marker,
                                          test_end_marker,
                                          test_file,
                                          )
        self.assertEqual(begin_pos,
                         '12697297',
                         'Incorrect begin position')
        self.assertEqual(end_pos,
                         '12951877',
                         'Incorrect end position')

    def test_get_region_chrom(self):
        """

        to see if get_region_chrom can manage to find the correct reference file
        and it can correct read begin position and end position for
        the given biomarkers

        """

        self.init_test(self.current_func_name)
        test_ref_db_prefix = os.path.join(self.data_dir,
                                          self.current_func_name)
        test_chrom = '18'
        test_begin_marker = 'rs146647843'
        test_end_marker = 'rs117978838'
        (begin_pos, end_pos) = get_region_chrom(test_chrom,
                                                test_begin_marker,
                                                test_end_marker,
                                                test_ref_db_prefix,
                                                )
        self.assertEqual(begin_pos,
                         '12697297',
                         'Incorrect begin position')
        self.assertEqual(end_pos,
                         '12951877',
                         'Incorrect end position')

    @unittest.skip("temporary disable due to long testing time")
    def test_summarize_annovar(self):
#        self.individual_debug = True
        self.init_test(self.current_func_name)
        test_chrom = '18'
        test_begin_pos = '12697297'
        test_end_pos = '12951877'
        test_tabix_file = os.path.join(self.data_dir,
                                       self.current_func_name + '.vcf.gz')
        test_working_dir = self.working_dir
        test_out_prefix = 'test_summarize_annovar_out'
        summarize_annovar(test_chrom,
                          test_begin_pos,
                          test_end_pos,
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


