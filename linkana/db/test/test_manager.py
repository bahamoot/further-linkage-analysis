import os
import csv
import linkana.settings as lka_const
from linkana.db.test.template import SafeDBTester
from linkana.db.connectors import VcfDB
from linkana.db.manager import AbstractVcfDB


class TestAbstractVcfDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'AbstractVcfDB'

    def __create_db_instance(self):
        abs_db = AbstractVcfDB()
        return abs_db

    def test_mutations(self):
        """ to check if mutations are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom1 = 18
        test_begin_pos1 = 12702537
        test_end_pos1 = '12703020'
        vcf_db1 = VcfDB()
        vcf_db1.open_db(test_file, test_chrom1, test_begin_pos1, test_end_pos1)
        abs_db.add_connector(vcf_db1)
        test_chrom2 = 18
        test_begin_pos2 = 12884105
        test_end_pos2 = 12884315
        vcf_db2 = VcfDB()
        vcf_db2.open_db(test_file, test_chrom2, test_begin_pos2, test_end_pos2)
        abs_db.add_connector(vcf_db2)
        mutations = abs_db.mutations
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
        # *************** test global access within mutations table ******************
        test_genotype_field = mutations['18|12884105'].genotype_fields['co1053']
        self.assertEqual(test_genotype_field.patient.genotype_fields['18|12702705'].raw_content,
                         '0/1:7,6:13:99:168,0,232',
                         'Incorrect mutations table access')

    def test_patients(self):
        """ to check if patients are correctly retrieved """

        self.init_test(self.current_func_name)
        abs_db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom1 = 18
        test_begin_pos1 = 12702537
        test_end_pos1 = '12703020'
        vcf_db1 = VcfDB()
        vcf_db1.open_db(test_file, test_chrom1, test_begin_pos1, test_end_pos1)
        abs_db.add_connector(vcf_db1)
        test_chrom2 = 18
        test_begin_pos2 = 12884105
        test_end_pos2 = 12884315
        vcf_db2 = VcfDB()
        vcf_db2.open_db(test_file, test_chrom2, test_begin_pos2, test_end_pos2)
        abs_db.add_connector(vcf_db2)
        patients = abs_db.patients
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
        # *************** test contents ******************
        genotype_fields = abs_db.patients['co1053'].genotype_fields
        test_genotype_field = genotype_fields['18|12702537']
        self.assertEqual(test_genotype_field.vcf_mutations,
                         'Unknown',
                         'Invalid data in genotype field')
        test_genotype_field = genotype_fields['18|12702610']
        self.assertEqual(test_genotype_field.vcf_mutations,
                         [{'ref': 'G', 'alt': 'A'}],
                         'Invalid data in genotype field')
        test_genotype_field = genotype_fields['18|12702705']
        self.assertEqual(test_genotype_field.vcf_mutations,
                         [{'ref': 'G', 'alt': 'C'}],
                         'Invalid data in genotype field')
        test_genotype_field = genotype_fields['18|12702730']
        self.assertEqual(test_genotype_field.vcf_mutations,
                         'Unknown',
                         'Invalid data in genotype field')
        test_genotype_field = genotype_fields['18|12703020']
        self.assertEqual(test_genotype_field.vcf_mutations,
                         'Unknown',
                         'Invalid data in genotype field')
        # *************** test global access within mutations table ******************
        test_genotype_field = abs_db.patients['co131'].genotype_fields['18|12884105']
        self.assertEqual(test_genotype_field.mutation.genotype_fields['Co866'].raw_content,
                         '0/0:14,0:14:33.10:0,33,394',
                         'Incorrect mutations table access')

