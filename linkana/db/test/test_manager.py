import os
import csv
import linkana.settings as lka_const
from linkana.db.test.template import SafeDBTester
from linkana.db.connectors import SummarizeAnnovarDB
from linkana.db.connectors import VcfDB
from linkana.db.connectors import FamilyDB
from linkana.db.manager import AbstractSummarizeAnnovarDB
from linkana.db.manager import AbstractVcfDB
from linkana.db.manager import AbstractFamilyDB
from linkana.db.manager import DBManager
from linkana.settings import TYPE1_ALL
from linkana.settings import TYPE2_RECTAL
from linkana.settings import TYPE2_NON_RECTAL
from linkana.settings import TYPE3_COLON
from linkana.settings import TYPE3_NON_COLON
from linkana.settings import TYPE4_CAFAM
from linkana.settings import TYPE4_NON_CAFAM


class TestAbstractSummarizeAnnovarDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'AbstractSummarizeAnnovarDB'

    def __create_db_instance(self):
        abs_sa_db = AbstractSummarizeAnnovarDB()
        return abs_sa_db

    def test_mutations(self):
        """ to check if mutations are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_sa_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.tab.csv')
        sa_db = SummarizeAnnovarDB()
        sa_db.open_db(test_file)
        abs_sa_db.add_connector(sa_db)
        mutations = abs_sa_db.mutations
        # *************** test keys ******************
        self.assertEqual(len(mutations.keys()),
                         9,
                         'Incorrect number of mutation keys')
        self.assertTrue('18|12702705|G|C' in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12697298|G|T' in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12702536|T|G' not in mutations,
                         'Incorrect mutation key')
        # *************** test contents ******************
        test_mutation = mutations['18|12702537|T|G']
        self.assertEqual(len(mutations),
                         9,
                         'Incorrect number of mutations')
        self.assertEqual(test_mutation.func,
                         'exonic',
                         'Incorrect Annovar content at "Func" column')
        self.assertEqual(test_mutation.gene,
                         'CEP76',
                         'Incorrect Annovar content at "Gene" column')
        self.assertEqual(test_mutation.exonic_func,
                         'synonymous SNV',
                         'Incorrect Annovar content at "ExonicFunc" column')
        self.assertEqual(test_mutation.dbsnp137,
                         'rs146647843',
                         'Incorrect Annovar content at "dbSNP137" column')
        self.assertEqual(test_mutation.avsift,
                         '0.45',
                         'Incorrect Annovar content at "AVSIFT" column')
        self.assertEqual(test_mutation.ljb_phylop,
                         '0.994193',
                         'Incorrect Annovar content at "LJB_PhyloP" column')
        self.assertEqual(test_mutation.ljb_sift_pred,
                         'D',
                         'Incorrect Annovar content at "LJB_SIFT_Pred" column')
        self.assertEqual(test_mutation.ljb_polyphen2,
                         '0.966',
                         'Incorrect Annovar content at "LJB_PolyPhen2" column')
        self.assertEqual(test_mutation.ljb_lrt_pred,
                         'D',
                         'Incorrect Annovar content at "LJB_LRT_Pred" column')
        self.assertEqual(test_mutation.ljb_gerp,
                         '4.62',
                         'Incorrect Annovar content at "LJB_GERP++" column')


class TestAbstractVcfDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'AbstractVcfDB'

    def __create_db_instance(self, patient_codes=None):
        abs_vcf_db = AbstractVcfDB(patient_codes)
        return abs_vcf_db

    def test_mutations_from_two_VcfDB(self):
        """ to check if mutations are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom1 = 18
        test_begin_pos1 = 12702537
        test_end_pos1 = '12703020'
        vcf_db1 = VcfDB()
        vcf_db1.open_db(test_file, test_chrom1, test_begin_pos1, test_end_pos1)
        abs_vcf_db.add_connector(vcf_db1)
        test_chrom2 = 18
        test_begin_pos2 = 12884105
        test_end_pos2 = 12884315
        vcf_db2 = VcfDB()
        vcf_db2.open_db(test_file, test_chrom2, test_begin_pos2, test_end_pos2)
        abs_vcf_db.add_connector(vcf_db2)
        mutations = abs_vcf_db.mutations
        # *************** test keys ******************
        self.assertEqual(len(mutations.keys()),
                         10,
                         'Incorrect number of mutation keys')
        self.assertTrue('18|12702705' in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12884315' in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12702536' not in mutations,
                         'Incorrect mutation key')
        # *************** test contents ******************
        self.assertEqual(len(mutations),
                         10,
                         'Incorrect number of mutations')
        self.assertEqual(mutations['18|12884315'].ref,
                         'C',
                         'Incorrect mutation content')
        self.assertEqual(mutations['18|12702610'].vcf_id,
                         'rs4797701',
                         'Incorrect mutation content')
        self.assertEqual(mutations['18|12884105'].genotype_fields['354/06'].raw_content,
                         '0/0:12,0:12:30.09:0,30,377',
                         'Invalid data in genotype field')
        self.assertEqual(mutations['18|12884105'].genotype_fields['398-05o'].raw_content,
                         './.',
                         'Invalid data in genotype field')
        self.assertEqual(mutations['18|12884105'].genotype_fields['Co866'].raw_content,
                         '0/0:14,0:14:33.10:0,33,394',
                         'Invalid data in genotype field')
        ## *************** test global access within mutations table ******************
        #test_genotype_field = mutations['18|12884105'].genotype_fields['co1053']
        #self.assertEqual(test_genotype_field.patient.genotype_fields['18|12702705'].raw_content,
        #                 '0/1:7,6:13:99:168,0,232',
        #                 'Incorrect mutations table access')

    def test_mutations_with_target_patients(self):
        """

        With target patients specified, the mutations table should have only
        mutations from the target patients,
        and should filter out the blank (.\.) ones

        """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance(["729-05o", "Co1207", "Co1368"])
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12702537
        test_end_pos = '12703020'
        vcf_db = VcfDB()
        vcf_db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos, patient_codes=["729-05o", "Co1207", "Co1368"])
        abs_vcf_db.add_connector(vcf_db)
        mutations = abs_vcf_db.mutations
        # *************** test keys ******************
        self.assertEqual(len(mutations.keys()),
                         4,
                         'Incorrect number of mutation keys')
        self.assertTrue('18|12702537' not in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12702705' in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12884315' not in mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12702536' not in mutations,
                         'Incorrect mutation key')
        # *************** test contents ******************
        self.assertEqual(len(mutations),
                         4,
                         'Incorrect number of mutations')
        self.assertEqual(len(mutations['18|12702705'].genotype_fields),
                         3,
                         'Incorrect number of genotype fields')
        self.assertEqual(mutations['18|12702705'].genotype_fields['Co1207'].raw_content,
                         './.',
                         'Invalid data in genotype field')
        self.assertEqual(mutations['18|12702610'].genotype_fields['729-05o'].raw_content,
                         '0/1:12,16:28:99:271,0,248',
                         'Invalid data in genotype field')
        self.assertEqual(mutations['18|12702705'].genotype_fields['Co1368'].raw_content,
                         '0/1:7,6:13:99:135,0,210',
                         'Invalid data in genotype field')

    def test_patients(self):
        """ to check if patients are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom1 = 18
        test_begin_pos1 = 12702537
        test_end_pos1 = '12703020'
        vcf_db1 = VcfDB()
        vcf_db1.open_db(test_file, test_chrom1, test_begin_pos1, test_end_pos1)
        abs_vcf_db.add_connector(vcf_db1)
        test_chrom2 = 18
        test_begin_pos2 = 12884105
        test_end_pos2 = 12884315
        vcf_db2 = VcfDB()
        vcf_db2.open_db(test_file, test_chrom2, test_begin_pos2, test_end_pos2)
        abs_vcf_db.add_connector(vcf_db2)
        patients = abs_vcf_db.patients
        # *************** test keys ******************
        self.assertEqual(len(patients),
                         77,
                         'Incorrect number of patients')
        self.assertTrue('1052/05' in patients.keys(),
                         'Incorrect patient code')
        self.assertTrue('398-05o' in patients.keys(),
                         'Incorrect patient code')
        self.assertTrue('Co866' in patients.keys(),
                         'Incorrect patient code')
        self.assertTrue('co131' in patients.keys(),
                         'Incorrect patient code')
        ## *************** test contents ******************
        #genotype_fields = abs_vcf_db.patients['co1053'].genotype_fields
        #test_genotype_field = genotype_fields['18|12702537']
        #self.assertEqual(test_genotype_field.vcf_mutations,
        #                 'Unknown',
        #                 'Invalid data in genotype field')
        #test_genotype_field = genotype_fields['18|12702610']
        #self.assertEqual(test_genotype_field.vcf_mutations,
        #                 [{'ref': 'G', 'alt': 'A'}],
        #                 'Invalid data in genotype field')
        #test_genotype_field = genotype_fields['18|12702705']
        #self.assertEqual(test_genotype_field.vcf_mutations,
        #                 [{'ref': 'G', 'alt': 'C'}],
        #                 'Invalid data in genotype field')
        #test_genotype_field = genotype_fields['18|12702730']
        #self.assertEqual(test_genotype_field.vcf_mutations,
        #                 'Unknown',
        #                 'Invalid data in genotype field')
        #test_genotype_field = genotype_fields['18|12703020']
        #self.assertEqual(test_genotype_field.vcf_mutations,
        #                 'Unknown',
        #                 'Invalid data in genotype field')
        ## *************** test global access within mutations table ******************
        #test_genotype_field = abs_vcf_db.patients['co131'].genotype_fields['18|12884105']
        #self.assertEqual(test_genotype_field.mutation.genotype_fields['Co866'].raw_content,
        #                 '0/0:14,0:14:33.10:0,33,394',
        #                 'Incorrect mutations table access')

    def test_common_mutations1(self):
        """

        to check if actual mutations from one patient
        are correctly retrieved

        """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        vcf_db = VcfDB()
        vcf_db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        abs_vcf_db.add_connector(vcf_db)
        common_mutations = abs_vcf_db.common_mutations(['Co1591'])
        # *************** test keys ******************
        self.assertEqual(len(common_mutations.keys()),
                         5,
                         'Incorrect number of common mutation keys')
        self.assertTrue('18|12512255' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512281' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512294' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512309' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512370' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512385' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513526' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513529' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513535' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513545' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513570' in common_mutations,
                         'Incorrect common mutation key')

    def test_common_mutations2(self):
        """

        to check if common mutations between two patients
        are correctly retrieved

        """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        vcf_db = VcfDB()
        vcf_db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        abs_vcf_db.add_connector(vcf_db)
        common_mutations = abs_vcf_db.common_mutations(['134/06', 'Co1584'])
        # *************** test keys ******************
        self.assertEqual(len(common_mutations.keys()),
                         4,
                         'Incorrect number of common mutation keys')
        self.assertTrue('18|12512255' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512281' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512294' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512309' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512370' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512385' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513526' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513529' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513535' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513545' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513570' not in common_mutations,
                         'Incorrect common mutation key')

    def test_common_mutations3(self):
        """

        to check if common mutations between three patients
        are correctly retrieved

        """

        self.init_test(self.current_func_name)
        abs_vcf_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        vcf_db = VcfDB()
        vcf_db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        abs_vcf_db.add_connector(vcf_db)
        common_mutations = abs_vcf_db.common_mutations(['134/06', 'Co1584', 'Co1591'])
        # *************** test keys ******************
        self.assertEqual(len(common_mutations.keys()),
                         3,
                         'Incorrect number of common mutation keys')
        self.assertTrue('18|12512255' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512281' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512294' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512309' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512370' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|12512385' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513526' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513529' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513535' in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513545' not in common_mutations,
                         'Incorrect common mutation key')
        self.assertTrue('18|14513570' not in common_mutations,
                         'Incorrect common mutation key')

class TestAbstractFamilyDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'AbstractFamilyDB'

    def __create_db_instance(self):
        abs_fam_db = AbstractFamilyDB()
        return abs_fam_db

    def test_families(self):
        """ to check if mutations are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_fam_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        fam_db = FamilyDB()
        fam_db.open_db(test_file)
        abs_fam_db.add_connector(fam_db)
        families = abs_fam_db.families
        # *************** test keys ******************
        self.assertEqual(len(families.keys()),
                         7,
                         'Incorrect number of families keys')
        self.assertTrue('8' in families,
                         'Incorrect families key')
        self.assertTrue('231' in families,
                         'Incorrect families key')
        self.assertTrue('347' not in families,
                         'Incorrect families key')
        # *************** test contents ******************
        test_family = families['425']
        self.assertEqual(len(test_family.patient_codes),
                         3,
                         'Incorrect number of members')
        self.assertEqual(test_family.type2,
                         'RECTAL',
                         'Incorrect family type2')
        self.assertEqual(test_family.type3,
                         '',
                         'Incorrect family type3')
        self.assertEqual(test_family.type4,
                         'CAFAM',
                         'Incorrect family type4')
        patient_codes = test_family.patient_codes
        self.assertEqual(len(patient_codes),
                         3,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[0],
                         'Co1458',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[1],
                         'Co1595',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[2],
                         'Co866',
                         'Incorrect patient code')


    def test_group_members_count(self):
        """

        to check if number of members in each group are correctly counted

        """

        self.init_test(self.current_func_name)
        abs_fam_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        fam_db = FamilyDB()
        fam_db.open_db(test_file)
        abs_fam_db.add_connector(fam_db)
        test_group_members_count = abs_fam_db.group_members_count
        # *************** test group members count ******************
        self.assertEqual(test_group_members_count[TYPE1_ALL],
                         76,
                         'Invaild number of members in group: '+TYPE1_ALL)
        self.assertEqual(test_group_members_count[TYPE2_RECTAL],
                         37,
                         'Invaild number of members in group: '+TYPE2_RECTAL)
        self.assertEqual(test_group_members_count[TYPE2_NON_RECTAL],
                         39,
                         'Invaild number of members in group: '+TYPE2_NON_RECTAL)
        self.assertEqual(test_group_members_count[TYPE3_COLON],
                         21,
                         'Invaild number of members in group: '+TYPE3_COLON)
        self.assertEqual(test_group_members_count[TYPE3_NON_COLON],
                         55,
                         'Invaild number of members in group: '+TYPE3_NON_COLON)
        self.assertEqual(test_group_members_count[TYPE4_CAFAM],
                         37,
                         'Invaild number of members in group: '+TYPE4_CAFAM)
        self.assertEqual(test_group_members_count[TYPE4_NON_CAFAM],
                         39,
                         'Invaild number of members in group: '+TYPE4_NON_CAFAM)

class TestDBManager(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'DBManager'

    def __create_db_instance(self, patient_codes=None):
        db_man = DBManager(patient_codes)
        return db_man

    def test_abstract(self):
        """

        to roughly check if all the abstract properties are
        properly implemented

        """

        self.init_test(self.current_func_name)
        db_man = self.__create_db_instance()
        test_sa_file = os.path.join(self.data_dir,
                                    self.current_func_name + '.tab.csv')
        db_man.connect_summarize_annovar_db(test_sa_file)
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.txt')
        db_man.connect_family_db(test_fam_file)
        # *************** test summarize annovar db ******************
        sa_mutations = db_man.summarize_annovar_db.mutations
        self.assertEqual(len(sa_mutations.keys()),
                         9,
                         'Incorrect number of mutation keys')
        self.assertTrue('18|12702705|G|C' in sa_mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12697298|G|T' in sa_mutations,
                         'Incorrect mutation key')
        self.assertTrue('18|12702536|T|G' not in sa_mutations,
                         'Incorrect mutation key')
        # *************** test vcf db ******************
        common_mutations = db_man.vcf_db.common_mutations(['134/06', 'Co1584', 'Co1591'])
        self.assertEqual(len(common_mutations.keys()),
                         3,
                         'Incorrect number of common mutation keys')
        self.assertTrue('18|12512255|T|G' not in common_mutations,
                         'Incorrect common mutation key')
        # *************** test family db ******************
        families = db_man.family_db.families
        test_family = families['478']
        self.assertEqual(len(test_family.patient_codes),
                         2,
                         'Incorrect number of members')
        self.assertEqual(test_family.type2,
                         'RECTAL',
                         'Incorrect family type2')
        self.assertEqual(test_family.type3,
                         '',
                         'Incorrect family type3')
        self.assertEqual(test_family.type4,
                         '',
                         'Incorrect family type4')
        patient_codes = test_family.patient_codes
        self.assertEqual(len(patient_codes),
                         2,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[0],
                         'Co1274',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[1],
                         'Co1207',
                         'Incorrect patient code')

    def test_valid_patient_codes(self):
        """

        To check if valid header can identify valid Vcf header line

        """

        self.init_test(self.current_func_name)
        db_man = self.__create_db_instance()
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '_1.txt')
        db_man.connect_vcf_db(test_vcf_file, test_chrom, test_begin_pos, test_end_pos)
        db_man.connect_family_db(test_fam_file)
        self.assertFalse(db_man.valid_patient_codes,
                        'Invalid patient code validation process')
        test_fam_file = os.path.join(self.data_dir,
                                     self.current_func_name + '_2.txt')
        db_man.connect_family_db(test_fam_file)
        self.assertTrue(db_man.valid_patient_codes,
                        'Invalid patient code validation process')

    def test_patient_codes(self):
        """

        To check if valid header can identify valid Vcf header line

        """

        self.init_test(self.current_func_name)
        db_man = self.__create_db_instance(patient_codes=["Co555", "Co1037", "Co1274"])
        test_vcf_file = os.path.join(self.data_dir,
                                     self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12510000
        test_end_pos = 14515000
        db_man.connect_vcf_db(test_vcf_file,
                              test_chrom,
                              test_begin_pos,
                              test_end_pos,
                              )
        common_mutations = db_man.vcf_db.common_mutations(['Co555'])
        tpcs = db_man.vcf_db.patient_codes
        self.assertTrue("Co555" in tpcs,
                        'Invalid target patient code')
        self.assertTrue("Co1037" in tpcs,
                        'Invalid target patient code')
        self.assertTrue("Co1274" in tpcs,
                        'Invalid target patient code')
        self.assertFalse("Co1368" in tpcs,
                        'Invalid target patient code')
