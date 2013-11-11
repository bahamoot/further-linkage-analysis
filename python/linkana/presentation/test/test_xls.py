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

    def __create_xls_instance(self, report_code='ma'):
        ma = MutationAnnotator(report_code)
        return ma

    def test_annotate_group_stat1(self):
        """ to check if the group stat calculation is correct"""

        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
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
        self.assertEqual(test_mutation.stats_type1_ac,
                         [16],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.stats_type1_pc,
                         [12],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.stats_type1_pp,
                         [0.32],
                         'Incorrect type1 patient percentage')
        self.assertEqual(test_mutation.stats_type1_gc,
                         37,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.stats_type1_gp,
                         0.49,
                         'Incorrect type1 genotype percentage')
        self.assertEqual(test_mutation.stats_type2_ac,
                         [14],
                         'Incorrect type2 allele count')
        self.assertEqual(test_mutation.stats_type2_pc,
                         [10],
                         'Incorrect type2 patient count')
        self.assertEqual(test_mutation.stats_type2_pp,
                         [0.42],
                         'Incorrect type2 patient percentage')
        self.assertEqual(test_mutation.stats_type2_gc,
                         24,
                         'Incorrect type2 genotype count')
        self.assertEqual(test_mutation.stats_type2_gp,
                         0.65,
                         'Incorrect type2 genotype percentage')
        self.assertEqual(test_mutation.stats_type3_ac,
                         [1],
                         'Incorrect type3 allele count')
        self.assertEqual(test_mutation.stats_type3_pc,
                         [1],
                         'Incorrect type3 patient count')
        self.assertEqual(test_mutation.stats_type3_pp,
                         [0.1],
                         'Incorrect type3 patient percentage')
        self.assertEqual(test_mutation.stats_type3_gc,
                         10,
                         'Incorrect type3 genotype count')
        self.assertEqual(test_mutation.stats_type3_gp,
                         0.48,
                         'Incorrect type3 genotype percentage')
        self.assertEqual(test_mutation.stats_type4_ac,
                         [6],
                         'Incorrect type4 allele count')
        self.assertEqual(test_mutation.stats_type4_pc,
                         [4],
                         'Incorrect type4 patient count')
        self.assertEqual(test_mutation.stats_type4_pp,
                         [0.57],
                         'Incorrect type4 patient percentage')
        self.assertEqual(test_mutation.stats_type4_gc,
                         7,
                         'Incorrect type4 genotype count')
        self.assertEqual(test_mutation.stats_type4_gp,
                         0.19,
                         'Incorrect type4 genotype percentage')

    def test_annotate_group_stat2(self):
        """ 

        to check if the group stat calculation is correct
        if number of patients in family file is not equal to that in vcf

        """

        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
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
        self.assertEqual(test_mutation.stats_type1_ac,
                         [28],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.stats_type1_pc,
                         [14],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.stats_type1_pp,
                         [1],
                         'Incorrect type1 patient percentage')
        self.assertEqual(test_mutation.stats_type1_gc,
                         14,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.stats_type1_gp,
                         1,
                         'Incorrect type1 genotype percentage')

    def test_annotate_group_stat3(self):
        """ 

        to check if the group stat calculation is correct
        if there are several alternate alleles

        """

        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        test_mutation = ma.vcf_mutations['18|12512385']
        self.assertEqual(test_mutation.stats_type1_ac,
                         [34, 31],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.stats_type1_pc,
                         [23, 23],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.stats_type1_pp,
                         [0.4, 0.4],
                         'Incorrect type1 patient percentage')
        self.assertEqual(test_mutation.stats_type1_gc,
                         57,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.stats_type1_gp,
                         0.75,
                         'Incorrect type1 genotype percentage')
        test_mutation = ma.vcf_mutations['18|14513526']
        self.assertEqual(test_mutation.stats_type1_ac,
                         [15],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.stats_type1_pc,
                         [13],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.stats_type1_pp,
                         [0.34],
                         'Incorrect type1 patient percentage')
        self.assertEqual(test_mutation.stats_type1_gc,
                         38,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.stats_type1_gp,
                         0.5,
                         'Incorrect type1 genotype percentage')
        test_mutation = ma.vcf_mutations['18|14513535']
        self.assertEqual(test_mutation.stats_type1_ac,
                         [18, 27, 15],
                         'Incorrect type1 allele count')
        self.assertEqual(test_mutation.stats_type1_pc,
                         [11, 21, 9],
                         'Incorrect type1 patient count')
        self.assertEqual(test_mutation.stats_type1_pp,
                         [0.26, 0.5, 0.21],
                         'Incorrect type1 patient percentage')
        self.assertEqual(test_mutation.stats_type1_gc,
                         42,
                         'Incorrect type1 genotype count')
        self.assertEqual(test_mutation.stats_type1_gp,
                         0.55,
                         'Incorrect type1 genotype percentage')

    def test_get_xls_records_genome(self):
        """ to check if the exporting content is correctly fetched """

        self.init_test(self.current_func_name)
#        ma = self.__create_xls_instance()
#        test_sa_file = os.path.join(self.data_dir,
#                                    self.current_func_name + '.tab.csv')
#        test_vcf_file = os.path.join(self.data_dir,
#                                     self.current_func_name + '.vcf.gz')
#        test_chrom = 18
#        test_begin_pos = 12750499
#        test_end_pos = 12793745
#        test_fam_file = os.path.join(self.data_dir,
#                                     self.current_func_name + '.txt')
#        db_man = DBManager()
#        db_man.connect_summarize_annovar_db(test_sa_file)
#        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
#        db_man.connect_family_db(test_fam_file)
#
#        ma.db_manager = db_man

        self.info('')
        self.info('')
        self.info('')
        self.info('')
        self.info('')
        self.info('*************************** Have to test this **********************************')
        self.info('')
        self.info('')
        self.info('')
        self.info('')

    @unittest.skip("too much txt print out")
    def test_export_xls1(self):
        """ to check if mutation annotation from one family is correctly exported """

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
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
        ma.export_xls(self.working_dir)

    def test_export_family_xls1(self):
        """ to check if mutation annotation from one family is correctly exported """

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
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

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
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

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('8', self.working_dir)

    def test_export_family_xls4(self):
        """

        to check if mutation annotation from families
        with several alternate alleles is correctly exported

        """

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('91', self.working_dir)
        ma.export_family_xls('296', self.working_dir)

    @unittest.skip("temporary disable due to long testing time")
    def test_export_family_xls5(self):
        """

        for almost real data, to check if mutation annotation
        from one family is correctly exported

        """

        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance('chr18')
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 10707433
        test_end_pos = 20607819
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        db_man.connect_summarize_annovar_db(test_sa_file)
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('918', self.working_dir)
        ma.export_family_xls('8', self.working_dir)

    def test_export_family_with_exon_filter(self):
        self.individual_debug = True
        self.init_test(self.current_func_name)
        ma = self.__create_xls_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = ""
        test_begin_pos = 12512309
        test_end_pos = 14513570
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man = DBManager()
        self.dbg("export family xls4: before connect summarize annovar")
        db_man.connect_summarize_annovar_db(test_sa_file)
        self.dbg("export family xls4: before connect vcf db")
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        self.dbg("export family xls4: before connect family db")
        db_man.connect_family_db(test_fam_file)

        ma.db_manager = db_man
        ma.export_family_xls('91', self.working_dir)
        ma.export_family_xls('296', self.working_dir)
