import pysam
import csv
import linkana.settings as lka_const
from linkana.template import LinkAnaBase
from linkana.misc.script import get_raw_vcf_gz_header

SUMMARIZE_ANNOVAR_DB_0_IDX_FUNC = 0
SUMMARIZE_ANNOVAR_DB_0_IDX_GENE = 1
SUMMARIZE_ANNOVAR_DB_0_IDX_EXONICFUNC = 2
SUMMARIZE_ANNOVAR_DB_0_IDX_AACHANGE = 3
SUMMARIZE_ANNOVAR_DB_0_IDX_CONSERVED = 4
SUMMARIZE_ANNOVAR_DB_0_IDX_SEGDUP = 5
SUMMARIZE_ANNOVAR_DB_0_IDX_ESP6500_ALL = 6
SUMMARIZE_ANNOVAR_DB_0_IDX_1000G2012APR_ALL = 7
SUMMARIZE_ANNOVAR_DB_0_IDX_DBSNP137 = 8
SUMMARIZE_ANNOVAR_DB_0_IDX_AVSIFT = 9
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_PHYLOP = 10
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_PHYLOP_PRED = 11
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_SIFT = 12
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_SIFT_PRED = 13
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_POLYPHEN2 = 14
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_POLYPHEN2_PRED = 15
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_LRT = 16
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_LRT_PRED = 17
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_MT = 18
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_MT_PRED = 19
SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_GERP = 20
SUMMARIZE_ANNOVAR_DB_0_IDX_CHROM = 21
SUMMARIZE_ANNOVAR_DB_0_IDX_START = 22
SUMMARIZE_ANNOVAR_DB_0_IDX_END = 23
SUMMARIZE_ANNOVAR_DB_0_IDX_REF = 24
SUMMARIZE_ANNOVAR_DB_0_IDX_OBS = 25
SUMMARIZE_ANNOVAR_DB_0_IDX_OTHER_INFO2 = 27

VCF_DB_0_IDX_CHROM = 0
VCF_DB_0_IDX_POS = 1
VCF_DB_0_IDX_ID = 2
VCF_DB_0_IDX_REF = 3
VCF_DB_0_IDX_ALT = 4
VCF_DB_0_IDX_QUAL = 5
VCF_DB_0_IDX_FILTER = 6
VCF_DB_0_IDX_INFO = 7
VCF_DB_0_IDX_FORMAT = 8
VCF_DB_0_IDX_OTHERS = 9

class SummarizeAnnovarDBRecord(object):
    """ to automatically parse record generated by summarized_annovar.pl """

    def __init__(self, rec):
        self.__rec = rec

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_raw_repr())

    def get_raw_repr(self):
        return {'Func': self.func,
                'Gene': self.gene,
                'ExonicFunc': self.exonic_func,
                'AAChange': self.aa_change,
                'Conserved': self.conserved,
                'SegDup': self.seg_dup,
                'ESP6500_ALL': self.esp6500_all,
                '1000g2012apr_ALL': self.maf,
                'dbSNP137': self.dbsnp137,
                'AVSIFT': self.avsift,
                'LJB_PhyloP': self.ljb_phylop,
                'LJB_PhyloP_Pred': self.ljb_phylop_pred,
                'LJB_SIFT': self.ljb_sift,
                'LJB_SIFT_Pred': self.ljb_sift_pred,
                'LJB_PolyPhen2': self.ljb_polyphen2,
                'LJB_PolyPhen2_Pred': self.ljb_polyphen2_pred,
                'LJB_LRT': self.ljb_lrt,
                'LJB_LRT_Pred': self.ljb_lrt_pred,
                'LJB_MutationTaster': self.ljb_mt,
                'LJB_MutationTaster_Pred': self.ljb_mt_pred,
                'LJB_GERP++': self.ljb_gerp,
                'Chr': self.chrom,
                'Start': self.start_pos,
                'End': self.end_pos,
                'Ref': self.ref,
                'Obs': self.obs,
                }

    @property
    def func(self):
        """ Func """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_FUNC]

    @property
    def gene(self):
        """ Gene """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_GENE]

    @property
    def exonic_func(self):
        """ ExonicFunc """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_EXONICFUNC]

    @property
    def aa_change(self):
        """ AAChange """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_AACHANGE]

    @property
    def conserved(self):
        """ conserved """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_CONSERVED]

    @property
    def seg_dup(self):
        """ SegDup """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_SEGDUP]

    @property
    def esp6500_all(self):
        """ ESP6500_ALL """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_ESP6500_ALL]

    @property
    def maf(self):
        """ 1000g2012apr_ALL """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_1000G2012APR_ALL]

    @property
    def dbsnp137(self):
        """ dbSNP137 """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_DBSNP137]

    @property
    def avsift(self):
        """ AVSIFT """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_AVSIFT]

    @property
    def ljb_phylop(self):
        """ LJB_PhyloP """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_PHYLOP]

    @property
    def ljb_phylop_pred(self):
        """ LJB_PhyloP_Pred """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_PHYLOP_PRED]

    @property
    def ljb_sift(self):
        """ LJB_SIFT """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_SIFT]

    @property
    def ljb_sift_pred(self):
        """ LJB_SIFT_Pred """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_SIFT_PRED]

    @property
    def ljb_polyphen2(self):
        """ LJB_PolyPhen2 """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_POLYPHEN2]

    @property
    def ljb_polyphen2_pred(self):
        """ LJB_PolyPhen2_Pred """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_POLYPHEN2_PRED]

    @property
    def ljb_lrt(self):
        """ LJB_LRT """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_LRT]

    @property
    def ljb_lrt_pred(self):
        """ LJB_LRT_Pred """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_LRT_PRED]

    @property
    def ljb_mt(self):
        """ LJB_MutationTaster """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_MT]

    @property
    def ljb_mt_pred(self):
        """ LJB_MutationTaster_Pred """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_MT_PRED]

    @property
    def ljb_gerp(self):
        """ LJB_GERP++ """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_LJB_GERP]

    @property
    def chrom(self):
        """ Chr """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_CHROM]

    @property
    def start_pos(self):
        """ Start """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_START]

    @property
    def end_pos(self):
        """ End """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_END]

    @property
    def ref(self):
        """ Ref """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_REF]

    @property
    def obs(self):
        """ Obs """
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_OBS]

    @property
    def other_info2(self):
        return self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_OTHER_INFO2]


class SummarizeAnnovarDBHeaderRecord(SummarizeAnnovarDBRecord):
    """ to automatically parse header generated by summarized_annovar.pl """

    def __init__(self, rec):
        SummarizeAnnovarDBRecord.__init__(self, rec)

    def get_raw_repr(self):
        new_raw_repr = SummarizeAnnovarDBRecord.get_raw_repr(self)
        new_raw_repr['Key'] = self.key
        return new_raw_repr

    @property
    def key(self):
        return None

class SummarizeAnnovarDBContentRecord(SummarizeAnnovarDBRecord):
    """ to automatically parse content record generated by summarized_annovar.pl """

    def __init__(self, rec):
        SummarizeAnnovarDBRecord.__init__(self, rec)

    def get_raw_repr(self):
        new_raw_repr = SummarizeAnnovarDBRecord.get_raw_repr(self)
        new_raw_repr['Key'] = self.key
        return new_raw_repr

    @property
    def key(self):
        key_fmt = "{chrom}|{vcf_pos}"
        return key_fmt.format(chrom=self.chrom,
                              vcf_pos=self.other_info2.split('|')[1])


class SummarizeAnnovarDB(object):
    """ to connect to the database produced by summarize_annovar.pl"""

    def __init__(self):
        self.__csv_file = None
        self.__delimiter = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'csv_file': self.__csv_file,
                    'delimiter': self.__delimiter,
                    })

    def __open_db(self, csv_file, delimiter='\t'):
        self.__csv_file = csv_file
        self.__delimiter = delimiter

    def open_db(self, csv_file, delimiter='\t'):
        return self.__open_db(csv_file, delimiter)

    @property
    def header(self):
        csv_file = open(self.__csv_file, 'rb')
        csv_records = csv.reader(csv_file, delimiter=self.__delimiter)
        header_csv = csv_records.next()
        return SummarizeAnnovarDBHeaderRecord(header_csv)

    @property
    def records(self):
        csv_file = open(self.__csv_file, 'rb')
        csv_records = csv.reader(csv_file, delimiter=self.__delimiter)
        csv_records.next()
        for csv_record in csv_records:
            yield SummarizeAnnovarDBContentRecord(csv_record)


class VcfDBRecord(object):
    """ to automatically parse VCF data"""

    def __init__(self, rec):
        self.__rec = rec

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_raw_repr())

    def get_raw_repr(self):
        return {'CHROM': self.chrom,
                'POS': self.pos,
                'ID': self.vcf_id,
                'REF': self.ref,
                'ALT': self.alt,
                'QUAL': self.qual,
                'FILTER': self.vcf_filter,
                'INFO': self.info,
                'FORMAT': self.vcf_format,
                'OTHERS': self.others,
                }

    @property
    def chrom(self):
        """ CHROM """
        return self.__rec[VCF_DB_0_IDX_CHROM]

    @property
    def pos(self):
        """ POS """
        return self.__rec[VCF_DB_0_IDX_POS]

    @property
    def vcf_id(self):
        """ ID """
        return self.__rec[VCF_DB_0_IDX_ID]

    @property
    def ref(self):
        """ REF """
        return self.__rec[VCF_DB_0_IDX_REF]

    @property
    def alt(self):
        """ ALT """
        return self.__rec[VCF_DB_0_IDX_ALT]

    @property
    def qual(self):
        """ QUAL """
        return self.__rec[VCF_DB_0_IDX_QUAL]

    @property
    def vcf_filter(self):
        """ FILTER """
        return self.__rec[VCF_DB_0_IDX_FILTER]

    @property
    def info(self):
        """ INFO """
        return self.__rec[VCF_DB_0_IDX_INFO]

    @property
    def vcf_format(self):
        """ FORMAT """
        return self.__rec[VCF_DB_0_IDX_FORMAT]

    @property
    def others(self):
        return self.__rec[VCF_DB_0_IDX_OTHERS:len(self.__rec)+1]


class VcfDBHeaderRecord(VcfDBRecord):
    """ to automatically parse VCF header"""

    def __init__(self, rec):
        VcfDBRecord.__init__(self, rec)

    def get_raw_repr(self):
        new_raw_repr = VcfDBRecord.get_raw_repr(self)
        del new_raw_repr['OTHERS']
        new_raw_repr['PATIENT_CODES'] = self.patient_codes
        return new_raw_repr

    @property
    def patient_codes(self):
        return self.others

class VcfDBContentRecord(VcfDBRecord):
    """ to automatically parse VCF content record"""

    def __init__(self, rec):
        VcfDBRecord.__init__(self, rec)

    def get_raw_repr(self):
        new_raw_repr = VcfDBRecord.get_raw_repr(self)
        del new_raw_repr['OTHERS']
        new_raw_repr['PATIENT_CONTENTS'] = self.patient_contents
        new_raw_repr['Key'] = self.key
        return new_raw_repr

    @property
    def key(self):
        key_fmt = "{chrom}|{pos}"
        return key_fmt.format(chrom=self.chrom,
                              pos=self.pos)

    @property
    def patient_contents(self):
        return self.others


class VcfDB(object):
    """ to connect to merged vcf database """

    def __init__(self):
        self.__vcf_db_gz_file = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'vcf.gz file': self.__vcf_db_gz_file,
                    'chrom': self.__chrom,
                    'begin position': self.__begin_pos,
                    'end position': self.__end_pos,
                    })

    def __open_db(self, vcf_db_gz_file, chrom, begin_pos, end_pos):
        self.__vcf_db_gz_file = vcf_db_gz_file
        self.__chrom = chrom
        self.__begin_pos = begin_pos
        self.__end_pos = end_pos

    def open_db(self, vcf_db_gz_file, chrom, begin_pos, end_pos):
        return self.__open_db(vcf_db_gz_file, chrom, begin_pos, end_pos)

    @property
    def header(self):
        header = get_raw_vcf_gz_header(self.__vcf_db_gz_file)
        return VcfDBHeaderRecord(header.strip("#").strip().split('\t'))

    @property
    def records(self):
        tabix_file = pysam.Tabixfile(self.__vcf_db_gz_file)
        for line in tabix_file.fetch(int(self.__chrom),
                                     int(self.__begin_pos)-1,
                                     int(self.__end_pos)):
            yield VcfDBContentRecord(line.strip().split('\t'))

