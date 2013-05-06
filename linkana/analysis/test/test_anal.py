import os
import csv
import linkana.settings as lka_const
from linkana.analysis.test.template import SafeAnalysisTester
from linkana.analysis.anal import Analyzer


class TestAnalyzer(SafeAnalysisTester):

    def __init__(self, test_name):
        SafeAnalysisTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'Analyzer'

    def __create_analyzer_instance(self):
        analyzer = Analyzer()
        return analyzer

    def test_init(self):
        self.init_test('test_init')
        analyzer = self.__create_analyzer_instance()

    def test_parse_dir_path(self):
        self.init_test('test_parse_dir_path')
        analyzer = self.__create_analyzer_instance()
        test_dir = os.path.join(self.data_dir, 'test_parse_dir_path')
        path1 = os.path.join(test_dir, 'Co35.tab.csv')
        dir_info = analyzer.parse_dir_path(path1)
        self.assertTrue(dir_info is None,
                        'Incorrect directory name parsing')
        path2 = os.path.join(test_dir, 'family0008_chr18')
        dir_info = analyzer.parse_dir_path(path2)
        self.assertEqual(dir_info['fam_code'],
                         '0008',
                         'Incorrect family code parsing')
        self.assertEqual(dir_info['chrom'],
                         '18',
                         'Incorrect chromosome parsing')
        self.assertEqual(dir_info['dir_path'],
                         path2,
                         'Incorrect full directory path')

    def test_get_dirs_list(self):
        self.init_test('test_get_dirs_list')
        analyzer = self.__create_analyzer_instance()
        test_dir = os.path.join(self.data_dir,
                                'test_get_dirs_list')
        dirs_list = analyzer.get_dirs_list(test_dir)
        self.assertEqual(len(dirs_list),
                         3,
                         'Incorrect number of directories')

    def test_parse_file_name(self):
        self.init_test('test_parse_file_name')
        analyzer = self.__create_analyzer_instance()
        file_info = analyzer.parse_file_name('fam0918_chr18.xls')
        self.assertTrue(file_info is None,
                        'Incorrect file name parsing')
        file_info = analyzer.parse_file_name('fam0918_common_mutations.tab.csv')
        self.assertTrue(file_info is None,
                        'Incorrect file name parsing')
        file_info = analyzer.parse_file_name('134-06.tab.csv')
        self.assertEqual(file_info['member_code'],
                         '134-06',
                         'Incorrect member code parsing')
        self.assertEqual(file_info['file_name'],
                         '134-06.tab.csv',
                         'Incorrect file name parsing')
        file_info = analyzer.parse_file_name('602-05o.tab.csv')
        self.assertEqual(file_info['member_code'],
                         '602-05o',
                         'Incorrect member code parsing')
        self.assertEqual(file_info['file_name'],
                         '602-05o.tab.csv',
                         'Incorrect file name parsing')
        file_info = analyzer.parse_file_name('Co1373.tab.csv')
        self.assertEqual(file_info['member_code'],
                         'Co1373',
                         'Incorrect member code parsing')
        self.assertEqual(file_info['file_name'],
                         'Co1373.tab.csv',
                         'Incorrect file name parsing')

    def test_get_files_list(self):
        self.init_test('test_get_files_list')
        analyzer = self.__create_analyzer_instance()
        test_dir = os.path.join(self.data_dir,
                                'test_get_files_list')
        files_list = analyzer.get_files_list(test_dir)
        self.assertEqual(len(files_list),
                         4,
                         'Incorrect number of files')
        self.assertEqual(files_list[0]['file_path'],
                         os.path.join(test_dir, 'Co1373.tab.csv'),
                         'Incorrect full file path')

    def test_load_csv2db(self):
        self.init_test('test_load_csv2db')
        analyzer = self.__create_analyzer_instance()
        test_dir = os.path.join(self.data_dir,
                                'test_load_csv2db')
        test_file = os.path.join(test_dir,
                                 'test_load_csv2db.csv')
        analyzer.load_csv2db(test_file)
        self.assertEqual(len(analyzer.db_mgr.snp_mgr),
                         37,
                         'Incorrect number of SNPs are loaded')
        test_snp = analyzer.db_mgr.snp_mgr['18|000014803745']
        self.assertEqual(test_snp.info.chrom,
                         '18',
                         'Invalid chromosome')
        self.assertEqual(test_snp.info.start_pos,
                         '14803745',
                         'Invalid start position')

    def test_load_one_member_data(self):
        self.init_test('test_load_one_member_data')
        analyzer = self.__create_analyzer_instance()
        test_dir = os.path.join(self.data_dir,
                                'test_load_one_member_data')
        analyzer.load_one_member_data(test_dir)
        self.assertEqual(len(analyzer.db_mgr.snp_mgr),
                         11,
                         'Incorrect number of SNPs are loaded')
