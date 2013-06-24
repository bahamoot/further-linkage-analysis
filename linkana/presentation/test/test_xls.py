import os
import csv
import linkana.settings as lka_const
from linkana.presentation.test.template import SafePresentationTester
from linkana.presentation.xls import MutationAnnotator
from linkana.db.manager import DBManager
from linkana.presentation.xls import TYPE3_CAFAM
from linkana.presentation.xls import TYPE3_NON_CAFAM

class TestMutationAnnotator(SafePresentationTester):

    def __init__(self, test_name):
        SafePresentationTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'MutationAnnotator'

    def __create_db_instance(self):
        ma = MutationAnnotator()
        return ma

    def test_annotate_group_stat(self):
        """ to check if the group stat calculation is correct"""

        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12789246
        test_end_pos = 12793745
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        test_mutation = ma.vcf_mutations['18|12793222']
        self.assertEqual(test_mutation.group_stat[TYPE3_CAFAM]['allele_count'],
                         [6],
                         'Incorrect allele count')
        self.assertEqual(test_mutation.group_stat[TYPE3_CAFAM]['patient_count'],
                         [4],
                         'Incorrect patient count')
        self.assertEqual(test_mutation.group_stat[TYPE3_CAFAM]['genotype_count'],
                         14,
                         'Incorrect genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_CAFAM]['allele_count'],
                         [10],
                         'Incorrect allele count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_CAFAM]['patient_count'],
                         [8],
                         'Incorrect patient count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_CAFAM]['genotype_count'],
                         60,
                         'Incorrect genotype count')


