import os
import csv
import linkana.settings as lka_const
from linkana.db.test.template import SafeDBTester
from linkana.db.connectors import SummarizeAnnovarDB
from linkana.db.connectors import VcfDB
from linkana.db.connectors import FamilyDB


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
                         'Incorrect Annovar header key? Header shouldn')
        self.assertEqual(header.func,
                         'Func',
                         'Incorrect Annovar header at "Func" column')
        self.assertEqual(header.gene,
                         'Gene',
                         'Incorrect Annovar header at "Gene" column')
        self.assertEqual(header.exonic_func,
                         'ExonicFunc',
                         'Incorrect Annovar header at "ExonicFunc" column')
        self.assertEqual(header.aa_change,
                         'AAChange',
                         'Incorrect Annovar header at "AAChange" column')
        self.assertEqual(header.conserved,
                         'Conserved',
                         'Incorrect Annovar header at "Conserved" column')
        self.assertEqual(header.seg_dup,
                         'SegDup',
                         'Incorrect Annovar header at "SegDup" column')
        self.assertEqual(header.esp6500_all,
                         'ESP6500_ALL',
                         'Incorrect Annovar header at "ESP6500_ALL" column')
        self.assertEqual(header.maf,
                         '1000g2012apr_ALL',
                         'Incorrect Annovar header at "1000g2012apr_ALL" column')
        self.assertEqual(header.dbsnp137,
                         'dbSNP137',
                         'Incorrect Annovar header at "dbSNP137" column')
        self.assertEqual(header.avsift,
                         'AVSIFT',
                         'Incorrect Annovar header at "AVSIFT" column')
        self.assertEqual(header.ljb_phylop,
                         'LJB_PhyloP',
                         'Incorrect Annovar header at "LJB_PhyloP" column')
        self.assertEqual(header.ljb_phylop_pred,
                         'LJB_PhyloP_Pred',
                         'Incorrect Annovar header at "LJB_PhyloP_Pred" column')
        self.assertEqual(header.ljb_sift,
                         'LJB_SIFT',
                         'Incorrect Annovar header at "LJB_SIFT" column')
        self.assertEqual(header.ljb_sift_pred,
                         'LJB_SIFT_Pred',
                         'Incorrect Annovar header at "LJB_SIFT_Pred" column')
        self.assertEqual(header.ljb_polyphen2,
                         'LJB_PolyPhen2',
                         'Incorrect Annovar header at "LJB_PolyPhen2" column')
        self.assertEqual(header.ljb_polyphen2_pred,
                         'LJB_PolyPhen2_Pred',
                         'Incorrect Annovar header at "LJB_PolyPhen2_Pred" column')
        self.assertEqual(header.ljb_lrt,
                         'LJB_LRT',
                         'Incorrect Annovar header at "LJB_LRT" column')
        self.assertEqual(header.ljb_lrt_pred,
                         'LJB_LRT_Pred',
                         'Incorrect Annovar header at "LJB_LRT_Pred" column')
        self.assertEqual(header.ljb_mt,
                         'LJB_MutationTaster',
                         'Incorrect Annovar header at "LJB_MutationTaster" column')
        self.assertEqual(header.ljb_mt_pred,
                         'LJB_MutationTaster_Pred',
                         'Incorrect Annovar header at "LJB_MutationTaster_Pred" column')
        self.assertEqual(header.ljb_gerp,
                         'LJB_GERP++',
                         'Incorrect Annovar header at "LJB_GERP++" column')
        self.assertEqual(header.chrom,
                         'Chr',
                         'Incorrect Annovar header at "Chr" column')
        self.assertEqual(header.start_pos,
                         'Start',
                         'Incorrect Annovar header at "Start" column')
        self.assertEqual(header.end_pos,
                         'End',
                         'Incorrect Annovar header at "End" column')
        self.assertEqual(header.ref,
                         'Ref',
                         'Incorrect Annovar header at "Ref" column')
        self.assertEqual(header.obs,
                         'Obs',
                         'Incorrect Annovar header at "Obs" column')

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
        test_record = records.next()
        self.assertEqual(test_record.key,
                         '18|12702537',
                         'Incorrect record key')
        self.assertEqual(test_record.func,
                         'exonic',
                         'Incorrect Annovar content at "Func" column')
        self.assertEqual(test_record.gene,
                         'CEP76',
                         'Incorrect Annovar content at "Gene" column')
        self.assertEqual(test_record.exonic_func,
                         'synonymous SNV',
                         'Incorrect Annovar content at "ExonicFunc" column')
        self.assertEqual(test_record.aa_change,
                         'CEP76:NM_001271989:exon4:c.A405C:p.S135S,CEP76:NM_024899:exon5:c.A630C:p.S210S',
                         'Incorrect Annovar content at "AAChange" column')
        self.assertEqual(test_record.conserved,
                         '671;Name=lod=713',
                         'Incorrect Annovar content at "Conserved" column')
        self.assertEqual(test_record.seg_dup,
                         '',
                         'Incorrect Annovar content at "SegDup" column')
        self.assertEqual(test_record.esp6500_all,
                         '0.000308',
                         'Incorrect Annovar content at "ESP6500_ALL" column')
        self.assertEqual(test_record.maf,
                         '0.0014',
                         'Incorrect Annovar content at "1000g2012apr_ALL" column')
        self.assertEqual(test_record.dbsnp137,
                         'rs146647843',
                         'Incorrect Annovar content at "dbSNP137" column')
        self.assertEqual(test_record.avsift,
                         '0.45',
                         'Incorrect Annovar content at "AVSIFT" column')
        self.assertEqual(test_record.ljb_phylop,
                         '0.994193',
                         'Incorrect Annovar content at "LJB_PhyloP" column')
        self.assertEqual(test_record.ljb_phylop_pred,
                         'C',
                         'Incorrect Annovar content at "LJB_PhyloP_Pred" column')
        self.assertEqual(test_record.ljb_sift,
                         '0',
                         'Incorrect Annovar content at "LJB_SIFT" column')
        self.assertEqual(test_record.ljb_sift_pred,
                         'D',
                         'Incorrect Annovar content at "LJB_SIFT_Pred" column')
        self.assertEqual(test_record.ljb_polyphen2,
                         '0.966',
                         'Incorrect Annovar content at "LJB_PolyPhen2" column')
        self.assertEqual(test_record.ljb_polyphen2_pred,
                         'B',
                         'Incorrect Annovar content at "LJB_PolyPhen2_Pred" column')
        self.assertEqual(test_record.ljb_lrt,
                         '1',
                         'Incorrect Annovar content at "LJB_LRT" column')
        self.assertEqual(test_record.ljb_lrt_pred,
                         'D',
                         'Incorrect Annovar content at "LJB_LRT_Pred" column')
        self.assertEqual(test_record.ljb_mt,
                         '0.999744',
                         'Incorrect Annovar content at "LJB_MutationTaster" column')
        self.assertEqual(test_record.ljb_mt_pred,
                         'D',
                         'Incorrect Annovar content at "LJB_MutationTaster_Pred" column')
        self.assertEqual(test_record.ljb_gerp,
                         '4.62',
                         'Incorrect Annovar content at "LJB_GERP++" column')
        self.assertEqual(test_record.chrom,
                         '18',
                         'Incorrect Annovar content at "Chr" column')
        self.assertEqual(test_record.start_pos,
                         '12697298',
                         'Incorrect Annovar content at "Start" column')
        self.assertEqual(test_record.end_pos,
                         '12697298',
                         'Incorrect Annovar content at "End" column')
        self.assertEqual(test_record.ref,
                         'T',
                         'Incorrect Annovar content at "Ref" column')
        self.assertEqual(test_record.obs,
                         'G',
                         'Incorrect Annovar content at "Obs" column')


class TestVcfDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'VcfDB'

    def __create_db_instance(self):
        db = VcfDB()
        return db

    def test_header(self):
        """ to see if VcfDB can correctly retrieve and translate VCF header """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12702537
        test_end_pos = '12703020'
        db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        header = db.header
        self.assertEqual(header.chrom,
                         'CHROM',
                         'Incorrect Vcf header at "CHROM" column')
        self.assertEqual(header.pos,
                         'POS',
                         'Incorrect Vcf header at "POS" column')
        self.assertEqual(header.vcf_id,
                         'ID',
                         'Incorrect Vcf header at "ID" column')
        self.assertEqual(header.ref,
                         'REF',
                         'Incorrect Vcf header at "REF" column')
        self.assertEqual(header.alt,
                         'ALT',
                         'Incorrect Vcf header at "ALT" column')
        self.assertEqual(header.qual,
                         'QUAL',
                         'Incorrect Vcf header at "QUAL" column')
        self.assertEqual(header.vcf_filter,
                         'FILTER',
                         'Incorrect Vcf header at "FILTER" column')
        self.assertEqual(header.info,
                         'INFO',
                         'Incorrect Vcf header at "INFO" column')
        self.assertEqual(header.vcf_format,
                         'FORMAT',
                         'Incorrect Vcf header at "FORMAT" column')
        patient_codes = header.patient_codes
        self.assertEqual(len(patient_codes),
                         77,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[2],
                         '134/06',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[10],
                         '602-05o',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[74],
                         'co1053',
                         'Incorrect patient code')

    def test_records_count(self):
        """ to check if all records are read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12702537
        test_end_pos = '12703020'
        db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        self.assertEqual(len(list(db.records)),
                         6,
                         'Incorrect number of records retrieved by VcfDB')

    def test_record_content1(self):
        """ to see if VcfDB can correctly retrieve raw VCF contents """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12702537
        test_end_pos = '12703020'
        db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        records = db.records
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.key,
                         '18|12702610',
                         'Incorrect record key')
        self.assertEqual(test_record.chrom,
                         '18',
                         'Incorrect Vcf content at "CHROM" column')
        self.assertEqual(test_record.pos,
                         '12702610',
                         'Incorrect Vcf content at "POS" column')
        self.assertEqual(test_record.vcf_id,
                         'rs4797701',
                         'Incorrect Vcf content at "ID" column')
        self.assertEqual(test_record.ref,
                         'G',
                         'Incorrect Vcf content at "REF" column')
        self.assertEqual(test_record.alt,
                         'A',
                         'Incorrect Vcf content at "ALT" column')
        self.assertEqual(test_record.qual,
                         '1945.51',
                         'Incorrect Vcf content at "QUAL" column')
        self.assertEqual(test_record.vcf_filter,
                         'PASS',
                         'Incorrect Vcf content at "FILTER" column')
        self.assertEqual(test_record.info,
                         'AC=29;AF=0.322;AN=90;DB;DP=1635;Dels=0.00;HRun=0;MQ0=0;VQSLOD=5.1293;culprit=QD;set=Intersection',
                         'Incorrect Vcf content at "INFO" column')
        self.assertEqual(test_record.vcf_format,
                         'GT:AD:DP:GQ:PL',
                         'Incorrect Vcf content at "FORMAT" column')
        patient_contents = test_record.patient_contents
        self.assertEqual(len(patient_contents),
                         77,
                         'Incorrect number of patient contents being read')
        self.assertEqual(patient_contents[2].raw_content,
                         '0/0:16,0:16:42.10:0,42,475',
                         'Incorrect patient raw content')
        self.assertEqual(patient_contents[10].raw_content,
                         '0/1:13,31:43:99:695,0,138',
                         'Incorrect patient raw content')
        self.assertEqual(patient_contents[74].raw_content,
                         '0/1:23,21:44:99:360,0,571',
                         'Incorrect patient raw content')

    def test_record_content2(self):
        """ to see if VcfDB can correctly parse VCF contents """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12512309
        test_end_pos = 14513570
        db.open_db(test_file, test_chrom, test_begin_pos, test_end_pos)
        records = db.records
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.key,
                         '18|12512370',
                         'Incorrect record key')
        self.assertEqual(test_record.patient_contents[1].raw_content,
                         '0/1:1,0:1:1.76',
                         'Incorrect patient raw content')
        self.assertEqual(test_record.patient_contents[1].raw_gt,
                         '0/1',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[1].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TACT'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[1].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TACT'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[1].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[2].raw_gt,
                         '2/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[2].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[2].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[2].zygosity,
                         'hom',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[3].raw_gt,
                         '0/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[3].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[3].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[3].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[5].raw_gt,
                         './.',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[5].vcf_mutations,
                         'Unknown',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[5].annovar_mutations,
                         'Unknown',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[5].zygosity,
                         'Unknown',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[10].raw_gt,
                         '.',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[10].vcf_mutations,
                         'Unknown',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[10].annovar_mutations,
                         'Unknown',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[10].zygosity,
                         'Unknown',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[12].raw_gt,
                         '0/3',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[12].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[12].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[12].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[15].raw_gt,
                         '0/0',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[15].vcf_mutations,
                         'None',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[15].annovar_mutations,
                         'None',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[15].zygosity,
                         'None',
                         'Incorrect zygosity')
        test_record = records.next()
        self.assertEqual(test_record.allele_count,
                         [34, 31],
                         'Incorrect allele count')
        self.assertEqual(test_record.patient_count,
                         [23, 23],
                         'Incorrect patient count')
        self.assertEqual(test_record.genotype_count,
                         114,
                         'Incorrect genotype count')
        self.assertEqual(test_record.patient_contents[62].raw_gt,
                         '1/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[62].vcf_mutations,
                         [{'ref': 'CAA', 'alt': 'C'}, {'ref': 'CAA', 'alt': 'CA'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[62].annovar_mutations,
                         [{'ref': 'AA', 'alt': '-'}, {'ref': 'A', 'alt': '-'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[62].zygosity,
                         'het',
                         'Incorrect zygosity')
        test_record = records.next()
        self.assertEqual(test_record.allele_count,
                         [16],
                         'Incorrect allele count')
        self.assertEqual(test_record.patient_count,
                         [14],
                         'Incorrect patient count')
        self.assertEqual(test_record.genotype_count,
                         78,
                         'Incorrect genotype count')
        self.assertEqual(test_record.key,
                         '18|14513526',
                         'Incorrect record key')
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.allele_count,
                         [18, 27, 16],
                         'Incorrect allele count')
        self.assertEqual(test_record.patient_count,
                         [11, 21, 10],
                         'Incorrect patient count')
        self.assertEqual(test_record.genotype_count,
                         86,
                         'Incorrect genotype count')
        self.assertEqual(test_record.patient_contents[6].raw_gt,
                         '0/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[6].vcf_mutations,
                         [{'ref': 'T', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[6].annovar_mutations,
                         [{'ref': '-', 'alt': 'ATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[6].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.patient_contents[9].raw_gt,
                         '3/3',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.patient_contents[9].vcf_mutations,
                         [{'ref': 'T', 'alt': 'TAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.patient_contents[9].annovar_mutations,
                         [{'ref': '-', 'alt': 'AC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.patient_contents[9].zygosity,
                         'hom',
                         'Incorrect zygosity')


class TestFamilyDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'FamilyDB'

    def __create_db_instance(self):
        db = FamilyDB()
        return db

    def test_records_count(self):
        """ to check if all records are read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        db.open_db(test_file)
        self.assertEqual(len(list(db.records)),
                         6,
                         'Incorrect number of records retrieved by FamilyDB')

    def test_records(self):
        """ to see if FamilyDB can correctly retrieve family informaiton """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        db.open_db(test_file)
        records = db.records
        records.next()
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.family_code,
                         '348',
                         'Incorrect family code')
        patient_codes = test_record.patient_codes
        self.assertEqual(len(patient_codes),
                         2,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[0],
                         'Co846',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[1],
                         'Co857',
                         'Incorrect patient code')

