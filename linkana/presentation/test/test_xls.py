import os
import csv
import unittest
import linkana.settings as lka_const
from linkana.presentation.test.template import SafePresentationTester
from linkana.presentation.xls import MutationAnnotator
from linkana.db.manager import DBManager
from linkana.settings import TYPE1_ALL
from linkana.settings import TYPE2_RECTAL
from linkana.settings import TYPE2_NON_RECTAL
from linkana.settings import TYPE3_COLON
from linkana.settings import TYPE3_NON_COLON
from linkana.settings import TYPE4_CAFAM
from linkana.settings import TYPE4_NON_CAFAM

class TestMutationAnnotator(SafePresentationTester):

    def __init__(self, test_name):
        SafePresentationTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'MutationAnnotator'

    def __create_db_instance(self):
        ma = MutationAnnotator('chr18')
        return ma

    def test_annotate_group_stat1(self):
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
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['allele_count'],
                         [16],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['patient_count'],
                         [12],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['genotype_count'],
                         37,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE2_RECTAL]['allele_count'],
                         [14],
                         'Incorrect type2 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE2_RECTAL]['patient_count'],
                         [10],
                         'Incorrect type2 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE2_RECTAL]['genotype_count'],
                         24,
                         'Incorrect type2 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE2_NON_RECTAL]['allele_count'],
                         [2],
                         'Incorrect non-type2 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE2_NON_RECTAL]['patient_count'],
                         [2],
                         'Incorrect non-type2 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE2_NON_RECTAL]['genotype_count'],
                         13,
                         'Incorrect non-type2 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE3_COLON]['allele_count'],
                         [1],
                         'Incorrect type3 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE3_COLON]['patient_count'],
                         [1],
                         'Incorrect type3 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE3_COLON]['genotype_count'],
                         10,
                         'Incorrect type3 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_COLON]['allele_count'],
                         [15],
                         'Incorrect non-type3 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_COLON]['patient_count'],
                         [11],
                         'Incorrect non-type3 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE3_NON_COLON]['genotype_count'],
                         27,
                         'Incorrect non-type3 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE4_CAFAM]['allele_count'],
                         [6],
                         'Incorrect type4 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE4_CAFAM]['patient_count'],
                         [4],
                         'Incorrect type4 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE4_CAFAM]['genotype_count'],
                         7,
                         'Incorrect type4 genotype count')
        self.assertEqual(test_mutation.group_stat[TYPE4_NON_CAFAM]['allele_count'],
                         [10],
                         'Incorrect non-type4 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE4_NON_CAFAM]['patient_count'],
                         [8],
                         'Incorrect non-type4 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE4_NON_CAFAM]['genotype_count'],
                         30,
                         'Incorrect non-type4 genotype count')

    def test_annotate_group_stat2(self):
        """ 

        to check if the group stat calculation is correct
        if number of patients in family file is not equal to that in vcf

        """

        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 11853000
        test_end_pos = 11854000
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        test_mutation = ma.vcf_mutations['18|11853053']
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['allele_count'],
                         [28],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['patient_count'],
                         [14],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.group_stat[TYPE1_ALL]['genotype_count'],
                         14,
                         'Incorrect type1 genotype count')

    def test_export_family_xls1(self):
        """ to check if mutation annotation from one family is correctly exported """

        print 
        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12750499
        test_end_pos = 12793745
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('12', self.working_dir)

    def test_export_family_xls2(self):
        """ to check if mutation annotation from one family is correctly exported """

        print 
        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
#        test_chrom = 18
#        test_begin_pos = 12750499
#        test_end_pos = 12793745
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
#        test_chrom = 18
#        test_begin_pos = 12512384
#        test_end_pos = 12512386
#        test_end_pos = 12793469
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('296', self.working_dir)

    def test_export_family_xls3(self):
        """ to check if mutation annotation from one family is correctly exported """

        print 
        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
#        test_chrom = 18
#        test_begin_pos = 12750499
#        test_end_pos = 12793745
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
#        test_chrom = 18
#        test_begin_pos = 12512384
#        test_end_pos = 12512386
#        test_end_pos = 12793469
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('8', self.working_dir)

    @unittest.skip("temporary disable due to long testing time")
    def test_export_family_xls4(self):
        """ to check if mutation annotation from one family is correctly exported """

        print 
        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 10707433
#        test_end_pos = 10800000
        test_end_pos = 20607819
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('918', self.working_dir)
