import os
from linkana.db.connection.test.template import SafeDBTester
from linkana.db.connection.vcfdb import VcfDB


class TestVcfDB(SafeDBTester):

    def __init__(self, test_name):
        SafeDBTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'VcfDB'

    def __create_db_instance(self):
        db = VcfDB()
        return db

    def test_header_general(self):
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
        genotype_idx = header.genotype_idx
        self.assertEqual(len(genotype_idx),
                         77,
                         'Incorrect number of patients')

    def test_header_target_patients(self):
        """

        to see if VcfDB can correctly retrieve and translate VCF header for
        indicated patients

        """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = ""
        test_begin_pos = ""
        test_end_pos = ""
        db.open_db(test_file, patient_codes=["Br694", "Br697", "Br526", "Br710"])
        header = db.header
        patient_codes = header.patient_codes
        self.assertTrue("Br694" in patient_codes,
                        'Invalid target patient code')
        self.assertTrue("Br697" in patient_codes,
                        'Invalid target patient code')
        self.assertTrue("Br526" in patient_codes,
                        'Invalid target patient code')
        self.assertTrue("Br710" in patient_codes,
                        'Invalid target patient code')
        self.assertFalse("Co1368" in patient_codes,
                        'Invalid target patient code')
        genotype_idx = header.genotype_idx
        self.assertTrue(0 in genotype_idx,
                        'Invalid genotype index')
        self.assertTrue(12 in genotype_idx,
                        'Invalid genotype index')
        self.assertTrue(20 in genotype_idx,
                        'Invalid genotype index')
        self.assertTrue(30 in genotype_idx,
                        'Invalid genotype index')
        self.assertFalse(10 in genotype_idx,
                        'Invalid genotype index')

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

    def test_record_content_raw_vcf(self):
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
        genotype_fields = test_record.genotype_fields
        self.assertEqual(len(genotype_fields),
                         77,
                         'Incorrect number of patient contents being read')
        self.assertEqual(genotype_fields[2].raw_content,
                         '0/0:16,0:16:42.10:0,42,475',
                         'Incorrect patient raw content')
        self.assertEqual(genotype_fields[10].raw_content,
                         '0/1:13,31:43:99:695,0,138',
                         'Incorrect patient raw content')
        self.assertEqual(genotype_fields[74].raw_content,
                         '0/1:23,21:44:99:360,0,571',
                         'Incorrect patient raw content')

    def test_record_content_parse_vcf(self):
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
        self.assertEqual(test_record.genotype_fields[1].raw_content,
                         '0/1:1,0:1:1.76',
                         'Incorrect patient raw content')
        self.assertEqual(test_record.genotype_fields[1].raw_gt,
                         '0/1',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[1].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TACT'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[1].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TACT'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[1].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[2].raw_gt,
                         '2/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[2].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[2].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[2].zygosity,
                         'hom',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[3].raw_gt,
                         '0/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[3].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[3].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[3].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[5].raw_gt,
                         './.',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[5].vcf_mutations,
                         'Unknown',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[5].annovar_mutations,
                         'Unknown',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[5].zygosity,
                         'Unknown',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[10].raw_gt,
                         '.',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[10].vcf_mutations,
                         'Unknown',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[10].annovar_mutations,
                         'Unknown',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[10].zygosity,
                         'Unknown',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[12].raw_gt,
                         '0/3',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[12].vcf_mutations,
                         [{'ref': 'TACA', 'alt': 'TC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[12].annovar_mutations,
                         [{'ref': 'TACA', 'alt': 'TC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[12].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[15].raw_gt,
                         '0/0',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[15].vcf_mutations,
                         'None',
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[15].annovar_mutations,
                         'None',
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[15].zygosity,
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
                         57,
                         'Incorrect genotype count')
        self.assertEqual(test_record.genotype_fields[62].raw_gt,
                         '1/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[62].vcf_mutations,
                         [{'ref': 'CAA', 'alt': 'C'}, {'ref': 'CAA', 'alt': 'CA'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[62].annovar_mutations,
                         [{'ref': 'AA', 'alt': '-'}, {'ref': 'A', 'alt': '-'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[62].zygosity,
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
                         39,
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
                         43,
                         'Incorrect genotype count')
        self.assertEqual(test_record.genotype_fields[6].raw_gt,
                         '0/2',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[6].vcf_mutations,
                         [{'ref': 'T', 'alt': 'TATAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[6].annovar_mutations,
                         [{'ref': '-', 'alt': 'ATAC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[6].zygosity,
                         'het',
                         'Incorrect zygosity')
        self.assertEqual(test_record.genotype_fields[9].raw_gt,
                         '3/3',
                         'Incorrect patient raw genotype')
        self.assertEqual(test_record.genotype_fields[9].vcf_mutations,
                         [{'ref': 'T', 'alt': 'TAC'}],
                         'Incorrect vcf mutations')
        self.assertEqual(test_record.genotype_fields[9].annovar_mutations,
                         [{'ref': '-', 'alt': 'AC'}],
                         'Incorrect annovar mutations')
        self.assertEqual(test_record.genotype_fields[9].zygosity,
                         'hom',
                         'Incorrect zygosity')

    def test_record_content_whole_vcf(self):
        """ to see if VcfDB can correctly read one whole vcf file """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        db.open_db(test_file)
        self.assertEqual(len(list(db.records)),
                         18,
                         'Incorrect number of records retrieved by VcfDB')

    def test_record_content_whole_chrom(self):
        """ to see if VcfDB can correctly read one whole chromosome """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        db.open_db(test_file, chrom='X')
        self.assertEqual(len(list(db.records)),
                         3,
                         'Incorrect number of records retrieved by VcfDB')

    def test_record_content_target_patients(self):
        """

        to see if VcfDB can correctly read the db if target patients are indicated

        """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.vcf.gz')
        test_chrom = 18
        test_begin_pos = 12702537
        test_end_pos = '12703020'
        db.open_db(test_file, patient_codes=["Br694", "Br697", "Br526", "Br710"])
        records = db.records
        records.next()
        records.next()
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.key,
                         '5|180900413',
                         'Incorrect record key')
        self.assertEqual(test_record.chrom,
                         '5',
                         'Incorrect Vcf content at "CHROM" column')
        self.assertEqual(test_record.pos,
                         '180900413',
                         'Incorrect Vcf content at "POS" column')
        self.assertEqual(test_record.vcf_id,
                         '.',
                         'Incorrect Vcf content at "ID" column')
        self.assertEqual(test_record.ref,
                         'A',
                         'Incorrect Vcf content at "REF" column')
        self.assertEqual(test_record.alt,
                         'C',
                         'Incorrect Vcf content at "ALT" column')
        self.assertEqual(test_record.qual,
                         '47.41',
                         'Incorrect Vcf content at "QUAL" column')
        self.assertEqual(test_record.vcf_filter,
                         'HARD_TO_VALIDATE;LowQual',
                         'Incorrect Vcf content at "FILTER" column')
        genotype_fields = test_record.genotype_fields
        self.assertEqual(len(genotype_fields),
                         4,
                         'Incorrect number of patient contents being read')
        self.assertEqual(genotype_fields[2].raw_content,
                         '0/0:2,0:2:6.01:0,6,62',
                         'Incorrect patient raw content')
        self.assertEqual(genotype_fields[3].raw_content,
                         './.',
                         'Incorrect patient raw content')
