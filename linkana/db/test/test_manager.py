import os
import csv
import linkana.settings as lka_const
from linkana.db.test.template import SafeDBTester
from linkana.db.manager import SNPRecord
from linkana.db.manager import SNPItem
from linkana.db.manager import SNPManager
from linkana.db.manager import MemberItem
from linkana.db.manager import MemberManager
from linkana.db.manager import FamilyItem
from linkana.db.manager import DBManager


class TestSNPManager(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'SNPManager'

    def __create_snp_mgr_instance(self):
        snp_mgr = SNPManager()
        return snp_mgr

    def test_add_snp(self):
        self.init_test('test_add_snp')
        snp_mgr = self.__create_snp_mgr_instance()
        test_file1 = os.path.join(self.data_dir,
                                 'test_add_snp1.csv')
        test_file2 = os.path.join(self.data_dir,
                                 'test_add_snp2.csv')
        csv_records = csv.reader(open(test_file1, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            snp_mgr.add_snp(SNPRecord(csv_record))
        csv_records = csv.reader(open(test_file2, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            snp_mgr.add_snp(SNPRecord(csv_record))
        self.assertEqual(len(snp_mgr),
                         30,
                         "Incorrect number of records are being fetched")
        self.assertEqual(snp_mgr['18|000018534948'].info.marker,
                         'rs201390233',
                         "Incorrect marker")
        self.assertEqual(snp_mgr['18|000019079877'].info.gene,
                         'GREB1L',
                         "Incorrect gene name")
        self.assertEqual(snp_mgr['18|000014542791'].count,
                         2,
                         "Incorrect snp count")

    def test_get_items_by_gene(self):
        self.init_test('test_get_items_by_gene')
        snp_mgr = self.__create_snp_mgr_instance()
        test_file1 = os.path.join(self.data_dir,
                                 'test_get_items_by_gene1.csv')
        test_file2 = os.path.join(self.data_dir,
                                 'test_get_items_by_gene2.csv')
        csv_records = csv.reader(open(test_file1, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            snp_mgr.add_snp(SNPRecord(csv_record))
        csv_records = csv.reader(open(test_file2, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            snp_mgr.add_snp(SNPRecord(csv_record))
        items = list(snp_mgr.get_items_by_gene('POTEC'))
        self.assertEqual(len(items),
                         3,
                         "Incorrect number of items being fetched")


class TestMemberItem(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'MemberItem'

    def __create_member_item_instance(self, chrom, fam_code, member_code):
        member_item = MemberItem(chrom, fam_code, member_code)
        return member_item

    def test_init(self):
        self.init_test('test_add_snp')
        member_item = self.__create_member_item_instance('dummy_chrom18',
                                                         'dummy_fam_code003',
                                                         'dummy_member_code17')
        self.assertEqual(member_item.pkey,
                         'dummy_chrom18|dummy_fam_code003|dummy_member_code17',
                         'Invalid key')
        self.assertEqual(member_item.chrom,
                         'dummy_chrom18',
                         'Invalid chromosome')
        self.assertEqual(member_item.fam_code,
                         'dummy_fam_code003',
                         'Invalid family code')
        self.assertEqual(member_item.member_code,
                         'dummy_member_code17',
                         'Invalid member code')

    def test_add_snp(self):
        self.init_test('test_add_snp')
        member_item = self.__create_member_item_instance('dummy_chrom',
                                                         'dummy_fam_code',
                                                         'dummy_member_code')
        test_file = os.path.join(self.data_dir,
                                 'test_add_snp.csv')
        csv_records = csv.reader(open(test_file, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            member_item.add_snp_key(SNPItem(SNPRecord(csv_record)).pkey)
        self.assertEqual(len(member_item.snps),
                         10,
                         'Incorrect number of snps')
        self.assertEqual(member_item.snps[2],
                         '18|000014757901',
                         'Invalid key')


class TestMemberManager(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'MemberManager'

    def __create_member_mgr_instance(self):
        member_mgr = MemberManager()
        return member_mgr

    def __mocup_member(self, chrom, fam_code, member_code, snp_csv):
        member_item = MemberItem(chrom, fam_code, member_code)
        csv_records = csv.reader(open(snp_csv, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            member_item.add_snp_key(SNPItem(SNPRecord(csv_record)).pkey)
        return member_item

    def test_add_member(self):
        self.init_test('test_add_snp')
        member_mgr = self.__create_member_mgr_instance()
        test_file1 = os.path.join(self.data_dir,
                                  'test_add_member1.csv')
        test_file2 = os.path.join(self.data_dir,
                                  'test_add_member2.csv')
        member_mgr.add_member(self.__mocup_member('chr9',
                                                  'family001',
                                                  'member05',
                                                  test_file1))
        member_mgr.add_member(self.__mocup_member('chr9',
                                                  'family002',
                                                  'member14',
                                                  test_file2))
        self.assertEqual(len(member_mgr),
                         2,
                         "Incorrect number of members")
        self.assertTrue('chr9|family001|member05' in member_mgr.keys(),
                        "Invalid key")


class TestFamilyItem(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'FamilyItem'

    def __create_family_item_instance(self, chrom, fam_code):
        family_item = FamilyItem(chrom, fam_code)
        return family_item

    def __mocup_member(self, chrom, fam_code, member_code, snp_csv):
        member_item = MemberItem(chrom, fam_code, member_code)
        csv_records = csv.reader(open(snp_csv, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            member_item.add_snp_key(SNPItem(SNPRecord(csv_record)).pkey)
        return member_item

    def test_init(self):
        self.init_test('test_init')
        family_item = self.__create_family_item_instance('dummy_chrom01',
                                                         'dummy_fam_code01')
        self.assertEqual(family_item.chrom,
                         'dummy_chrom01',
                         'Invalid chromosome')
        self.assertEqual(family_item.fam_code,
                         'dummy_fam_code01',
                         'Invalid family code')
        self.assertEqual(family_item.pkey,
                         'dummy_chrom01|dummy_fam_code01',
                         'Invalid key')

#    def test_member_key(self):
#        self.init_test('test_member_key')
#        family_item = self.__create_family_item_instance('dummy_chrom2',
#                                                         'dummy_fam_code23')
#        self.assertEqual(family_item.member_key('member02'),
#                         'dummy_chrom2|dummy_fam_code23|member02',
#                         'Incorrect member key')

    def test_add_member_key(self):
        self.init_test('test_add_member_key')
        test_chrom = 'dummy_chrom02'
        test_fam_code = 'dummy_fam_code02'
        family_item = self.__create_family_item_instance(test_chrom,
                                                         test_fam_code)
        test_file1 = os.path.join(self.data_dir,
                                  'test_add_member_key1.csv')
        test_file2 = os.path.join(self.data_dir,
                                  'test_add_member_key2.csv')
        member_item1 = self.__mocup_member(test_chrom,
                                           test_fam_code,
                                           'member001',
                                           test_file1)
        member_item2 = self.__mocup_member(test_chrom,
                                           test_fam_code,
                                           'member002',
                                           test_file2)
        family_item.add_member_key(member_item1.pkey)
        family_item.add_member_key(member_item2.pkey)
        self.assertEqual(len(family_item.member_keys),
                         2,
                         'Incorrect number of member keys')
        self.assertEqual(family_item.member_keys[0],
                         'dummy_chrom02|dummy_fam_code02|member001',
                         'Invalid member key')


class TestDBManager(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'DBManager'

    def __create_db_mgr_instance(self):
        db_mgr = DBManager()
        return db_mgr

    def test_add_mutation(self):
        self.init_test('test_add_mutation')
        db_mgr = self.__create_db_mgr_instance()
        test_file1 = os.path.join(self.data_dir,
                                 'test_add_mutation1.csv')
        test_file2 = os.path.join(self.data_dir,
                                 'test_add_mutation2.csv')
        csv_records = csv.reader(open(test_file1, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            db_mgr.add_mutation(SNPRecord(csv_record))
        csv_records = csv.reader(open(test_file2, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            db_mgr.add_mutation(SNPRecord(csv_record))
        self.assertEqual(len(db_mgr.snp_mgr),
                         30,
                         "Incorrect number of records are being fetched")
        self.assertEqual(db_mgr.snp_mgr['18|000018534948'].info.marker,
                         'rs201390233',
                         "Incorrect marker")
        self.assertEqual(db_mgr.snp_mgr['18|000019079877'].info.gene,
                         'GREB1L',
                         "Incorrect gene name")
        self.assertEqual(db_mgr.snp_mgr['18|000014542791'].count,
                         2,
                         "Incorrect snp count")
#        for csv_record in csv_records:
#            if (isFloat(csv_record[col_maf]) and (float(csv_record[col_maf])<=0.1)) or (csv_record[col_maf]=='') :
#               if (csv_record[col_exonic_func] != 'synonymous SNV'):
#                   self.__add_mutation(csv_record)
#        dm.load_data(test_file)
#        self.assertEqual(len(dm.manager),
#                         10,
#                         'SNPManager does not load VCF data correctly')
