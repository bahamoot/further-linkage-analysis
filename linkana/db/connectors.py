import csv
import linkana.settings as lka_const
from linkana.template import LinkAnaBase

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


class SummarizeAnnovarDBRecord(object):
    """ to automatically parse SNP data"""

    def __init__(self, rec):
        self.__rec = rec

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'Key': self.key,
                    'Func': self.func,
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
                    })

    @property
    def key(self):
        if len(self.__rec) == (SUMMARIZE_ANNOVAR_DB_0_IDX_OTHER_INFO2):
            return None
        else:
            key_fmt = "{chrom}|{vcf_pos}"
            return key_fmt.format(chrom=self.chrom,
                                  vcf_pos=self.__rec[SUMMARIZE_ANNOVAR_DB_0_IDX_OTHER_INFO2].split('|')[1])

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


class SummarizeAnnovarDB(object):
    """ to connect to the database produced by summarize_annovar.pl"""

    def __init__(self):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'SummarizeAnnovar'

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
        return SummarizeAnnovarDBRecord(header_csv)

    @property
    def records(self):
        csv_file = open(self.__csv_file, 'rb')
        csv_records = csv.reader(csv_file, delimiter=self.__delimiter)
        csv_records.next()
        for csv_record in csv_records:
            yield SummarizeAnnovarDBRecord(csv_record)

