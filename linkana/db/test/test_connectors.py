import os
import csv
import linkana.settings as lka_const
from linkana.db.test.template import SafeDBTester
from linkana.db.connectors import SummarizeAnnovarDB


class TestSummarizeAnnovarDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'SummarizeAnnovarDB'

    def __create_db_instance(self):
        db = SummarizeAnnovarDB()
        return db

    def test_header(self):
        """ to check if header generated by Summarize_Annovar.pl is correctly read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.tab.csv')
        db.open_db(test_file)
        header = db.header
        self.assertEqual(header.key,
                         None,
                         'Incorrect header key? Header shouldn')
        self.assertEqual(header.func,
                         'Func',
                         'Incorrect header at "Func" column')
        self.assertEqual(header.gene,
                         'Gene',
                         'Incorrect header at "Gene" column')
        self.assertEqual(header.exonic_func,
                         'ExonicFunc',
                         'Incorrect header at "ExonicFunc" column')
        self.assertEqual(header.aa_change,
                         'AAChange',
                         'Incorrect header at "AAChange" column')
        self.assertEqual(header.conserved,
                         'Conserved',
                         'Incorrect header at "Conserved" column')
        self.assertEqual(header.seg_dup,
                         'SegDup',
                         'Incorrect header at "SegDup" column')
        self.assertEqual(header.esp6500_all,
                         'ESP6500_ALL',
                         'Incorrect header at "ESP6500_ALL" column')
        self.assertEqual(header.maf,
                         '1000g2012apr_ALL',
                         'Incorrect header at "1000g2012apr_ALL" column')
        self.assertEqual(header.dbsnp137,
                         'dbSNP137',
                         'Incorrect header at "dbSNP137" column')
        self.assertEqual(header.avsift,
                         'AVSIFT',
                         'Incorrect header at "AVSIFT" column')
        self.assertEqual(header.ljb_phylop,
                         'LJB_PhyloP',
                         'Incorrect header at "LJB_PhyloP" column')
        self.assertEqual(header.ljb_phylop_pred,
                         'LJB_PhyloP_Pred',
                         'Incorrect header at "LJB_PhyloP_Pred" column')
        self.assertEqual(header.ljb_sift,
                         'LJB_SIFT',
                         'Incorrect header at "LJB_SIFT" column')
        self.assertEqual(header.ljb_sift_pred,
                         'LJB_SIFT_Pred',
                         'Incorrect header at "LJB_SIFT_Pred" column')
        self.assertEqual(header.ljb_polyphen2,
                         'LJB_PolyPhen2',
                         'Incorrect header at "LJB_PolyPhen2" column')
        self.assertEqual(header.ljb_polyphen2_pred,
                         'LJB_PolyPhen2_Pred',
                         'Incorrect header at "LJB_PolyPhen2_Pred" column')
        self.assertEqual(header.ljb_lrt,
                         'LJB_LRT',
                         'Incorrect header at "LJB_LRT" column')
        self.assertEqual(header.ljb_lrt_pred,
                         'LJB_LRT_Pred',
                         'Incorrect header at "LJB_LRT_Pred" column')
        self.assertEqual(header.ljb_mt,
                         'LJB_MutationTaster',
                         'Incorrect header at "LJB_MutationTaster" column')
        self.assertEqual(header.ljb_mt_pred,
                         'LJB_MutationTaster_Pred',
                         'Incorrect header at "LJB_MutationTaster_Pred" column')
        self.assertEqual(header.ljb_gerp,
                         'LJB_GERP++',
                         'Incorrect header at "LJB_GERP++" column')
        self.assertEqual(header.chrom,
                         'Chr',
                         'Incorrect header at "Chr" column')
        self.assertEqual(header.start_pos,
                         'Start',
                         'Incorrect header at "Start" column')
        self.assertEqual(header.end_pos,
                         'End',
                         'Incorrect header at "End" column')
        self.assertEqual(header.ref,
                         'Ref',
                         'Incorrect header at "Ref" column')
        self.assertEqual(header.obs,
                         'Obs',
                         'Incorrect header at "Obs" column')

    def test_records_count(self):
        """ to check if all records are read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.tab.csv')
        db.open_db(test_file)
        self.assertEqual(len(list(db.records)),
                         9,
                         'Incorrect number of records')

    def test_record_content(self):
        """ to check content in each record generated by Summarize_Annovar.pl is correctly read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.tab.csv')
        db.open_db(test_file)
        records = db.records
        records.next()
        record = records.next()
        self.assertEqual(record.key,
                         '18|12702537',
                         'Incorrect record key')
        self.assertEqual(record.func,
                         'exonic',
                         'Incorrect content at "Func" column')
        self.assertEqual(record.gene,
                         'CEP76',
                         'Incorrect content at "Gene" column')
        self.assertEqual(record.exonic_func,
                         'synonymous SNV',
                         'Incorrect content at "ExonicFunc" column')
        self.assertEqual(record.aa_change,
                         'CEP76:NM_001271989:exon4:c.A405C:p.S135S,CEP76:NM_024899:exon5:c.A630C:p.S210S',
                         'Incorrect content at "AAChange" column')
        self.assertEqual(record.conserved,
                         '671;Name=lod=713',
                         'Incorrect content at "Conserved" column')
        self.assertEqual(record.seg_dup,
                         '',
                         'Incorrect content at "SegDup" column')
        self.assertEqual(record.esp6500_all,
                         '0.000308',
                         'Incorrect content at "ESP6500_ALL" column')
        self.assertEqual(record.maf,
                         '0.0014',
                         'Incorrect content at "1000g2012apr_ALL" column')
        self.assertEqual(record.dbsnp137,
                         'rs146647843',
                         'Incorrect content at "dbSNP137" column')
        self.assertEqual(record.avsift,
                         '0.45',
                         'Incorrect content at "AVSIFT" column')
        self.assertEqual(record.ljb_phylop,
                         '0.994193',
                         'Incorrect content at "LJB_PhyloP" column')
        self.assertEqual(record.ljb_phylop_pred,
                         'C',
                         'Incorrect content at "LJB_PhyloP_Pred" column')
        self.assertEqual(record.ljb_sift,
                         '0',
                         'Incorrect content at "LJB_SIFT" column')
        self.assertEqual(record.ljb_sift_pred,
                         'D',
                         'Incorrect content at "LJB_SIFT_Pred" column')
        self.assertEqual(record.ljb_polyphen2,
                         '0.966',
                         'Incorrect content at "LJB_PolyPhen2" column')
        self.assertEqual(record.ljb_polyphen2_pred,
                         'B',
                         'Incorrect content at "LJB_PolyPhen2_Pred" column')
        self.assertEqual(record.ljb_lrt,
                         '1',
                         'Incorrect content at "LJB_LRT" column')
        self.assertEqual(record.ljb_lrt_pred,
                         'D',
                         'Incorrect content at "LJB_LRT_Pred" column')
        self.assertEqual(record.ljb_mt,
                         '0.999744',
                         'Incorrect content at "LJB_MutationTaster" column')
        self.assertEqual(record.ljb_mt_pred,
                         'D',
                         'Incorrect content at "LJB_MutationTaster_Pred" column')
        self.assertEqual(record.ljb_gerp,
                         '4.62',
                         'Incorrect content at "LJB_GERP++" column')
        self.assertEqual(record.chrom,
                         '18',
                         'Incorrect content at "Chr" column')
        self.assertEqual(record.start_pos,
                         '12697298',
                         'Incorrect content at "Start" column')
        self.assertEqual(record.end_pos,
                         '12697298',
                         'Incorrect content at "End" column')
        self.assertEqual(record.ref,
                         'T',
                         'Incorrect content at "Ref" column')
        self.assertEqual(record.obs,
                         'G',
                         'Incorrect content at "Obs" column')

