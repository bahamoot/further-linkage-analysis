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
        """ to check if mutations are correctly counted """

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
        mutations = abs_db.get_mutations()
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
        self.assertEqual(mutations['18|12884105'].patient_contents['354/06'].raw_content,
                         '0/0:12,0:12:30.09:0,30,377',
                         'Incorrect patient content')
        self.assertEqual(mutations['18|12884105'].patient_contents['398-05o'].raw_content,
                         './.',
                         'Incorrect patient content')
        self.assertEqual(mutations['18|12884105'].patient_contents['Co866'].raw_content,
                         '0/0:14,0:14:33.10:0,33,394',
                         'Incorrect patient content')

    def test_patient_codes_count(self):
        """ to check if patient codes are correctly counted """

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
        self.assertEqual(len(list(abs_db.patient_codes)),
                         77,
                         'Incorrect number of patients')

    def test_patient_codes(self):
        """ to check if patient codes are correctly retrieved """

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
        patient_codes = abs_db.patient_codes
        self.assertEqual(patient_codes[0],
                         '1052/05',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[5],
                         '398-05o',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[69],
                         'Co866',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[76],
                         'co131',
                         'Incorrect patient code')


