import pysam
import csv
from linkana.template import LinkAnaBase
from linkana.misc.script import get_raw_vcf_gz_header
from collections import OrderedDict

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

VCF_GENOTYPE_FIELD_0_IDX_GT = 0

VCF_MUTATION_UNKNOWN = 'Unknown'
VCF_MUTATION_NONE = 'None'

ZYGOSITY_UNKNOWN = 'Unknown'
ZYGOSITY_NONE = 'None'
ZYGOSITY_HET = 'het'
ZYGOSITY_HOM = 'hom'


class VcfDBRecord(LinkAnaBase):
    """ to automatically parse a record from VCF file """

    def __init__(self, rec):
        if isinstance(rec, list):
            self.__rec = rec
        else:
            self.__rec = rec.split('\t')

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
    """ to automatically parse a VCF header """

    def __init__(self, rec, patient_codes=None):
        VcfDBRecord.__init__(self, rec)
        self.__patient_codes = patient_codes

    def get_raw_repr(self):
        new_raw_repr = VcfDBRecord.get_raw_repr(self)
        del new_raw_repr['OTHERS']
        new_raw_repr['PATIENT_CODES'] = self.patient_codes
        return new_raw_repr

    @property
    def patient_codes(self):
        if self.__patient_codes is None:
            return self.others
        else:
            return self.__patient_codes

    @property
    def genotype_idx(self):
        if self.__patient_codes is None:
            return range(len(self.others))
        else:
            return map(lambda x: self.others.index(x),
                       self.__patient_codes)


class GenotypeFieldRecord(LinkAnaBase):
    """ to automatically parse data from genotype field """

    def __init__(self, rec, ref, alt):
        self.__raw = rec
        self.__ref = ref
        self.__alt = alt.split(',')
        self.__rec = rec.split(':')

    def get_raw_repr(self):
        return {'raw content': self.raw_content,
                'raw genotype': self.raw_gt,
                'vcf mutations': self.vcf_mutations,
                'annovar mutations': self.annovar_mutations,
                'zygosity': self.zygosity,
                }

    def normalize_mutations(self, ref, alt):
        if len(ref) > len(alt):
            #deletion
            if ref.find(alt) != -1:
                return ref[len(alt):], '-'
        if len(ref) < len(alt):
            #insertion
            if alt.find(ref) != -1:
                return '-', alt[len(ref):]
        #else return what they were
        return ref, alt

    @property
    def raw_content(self):
        """ raw content """
        return self.__raw

    @property
    def raw_gt(self):
        """ raw genotype """
        return self.__rec[VCF_GENOTYPE_FIELD_0_IDX_GT]

    @property
    def vcf_mutations(self):
        raw_gt = self.raw_gt
        if raw_gt == './.':
            return VCF_MUTATION_UNKNOWN
        if raw_gt == '.':
            return VCF_MUTATION_UNKNOWN
        if raw_gt == '0/0':
            return VCF_MUTATION_NONE
        gt = raw_gt.split('/')
        mutations = []
        if gt[0] != '0':
            mutations.append({'ref': self.__ref, 'alt': self.__alt[int(gt[0])-1]})
        if (gt[1] != '0') and (gt[0] != gt[1]):
            mutations.append({'ref': self.__ref, 'alt': self.__alt[int(gt[1])-1]})
        return mutations

    @property
    def annovar_mutations(self):
        vcf_mutations = self.vcf_mutations
        if not isinstance(vcf_mutations, list):
            return vcf_mutations
        mutations = []
        for vcf_mutation in vcf_mutations:
            (ref, alt) = self.normalize_mutations(vcf_mutation['ref'],
                                                  vcf_mutation['alt'])
            mutations.append({'ref': ref, 'alt': alt})
        return mutations

    @property
    def zygosity(self):
        raw_gt = self.raw_gt
        if raw_gt == './.':
            return ZYGOSITY_UNKNOWN
        if raw_gt == '.':
            return ZYGOSITY_UNKNOWN
        if raw_gt == '0/0':
            return ZYGOSITY_NONE
        gt = raw_gt.split('/')
        if gt[0] != gt[1]:
            return ZYGOSITY_HET
        else:
            return ZYGOSITY_HOM


class VcfDBContentRecord(VcfDBRecord):
    """ to automatically parse a mutation record in VCF format """

    def __init__(self, rec, genotype_idx):
        VcfDBRecord.__init__(self, rec)
        self.__genotype_fields = None
        self.__stat = None
        self.__genotype_idx = genotype_idx
#        self.group_stat = {}

    def get_raw_repr(self):
        new_raw_repr = VcfDBRecord.get_raw_repr(self)
        del new_raw_repr['OTHERS']
        new_raw_repr['GENOTYPE_FIELDS'] = self.genotype_fields
        new_raw_repr['Key'] = self.key
        return new_raw_repr

    def calculate_stat(self, genotype_fields=None):
        if genotype_fields is None:
            if type(self.genotype_fields) is dict:
                genotype_fields = map(lambda x: self.genotype_fields[x],
                                      self.genotype_fields)
            if type(self.genotype_fields) is list:
                genotype_fields = self.genotype_fields
        #init
        stat = {}
        stat['allele_count'] = [0 for i in range(len(self.alt.split(',')))]
        stat['patient_count'] = [0 for i in range(len(self.alt.split(',')))]
        stat['genotype_count'] = 0
        #count
        for genotype_field in genotype_fields:
            raw_gt = genotype_field.raw_gt
            if raw_gt == './.':
                continue
            if raw_gt == '.':
                continue
            #genotype_count
            stat['genotype_count'] += 1
            if raw_gt == '0/0':
                continue
            gt = raw_gt.split('/')
            #allele_count
            if gt[0] != '0':
                stat['allele_count'][int(gt[0])-1] += 1
            if gt[1] != '0':
                stat['allele_count'][int(gt[1])-1] += 1
            #patient_count
            if gt[0] != '0':
                stat['patient_count'][int(gt[0])-1] += 1
            if (gt[1] != '0') and (gt[0] != gt[1]):
                stat['patient_count'][int(gt[1])-1] += 1
        return stat

    def validate_stat(self):
        #parse info field
        raw_infos = self.info.split(';')
        infos = {}
        for raw_info in raw_infos:
            if raw_info.find('=') != -1:
                key, value = raw_info.split('=')
                infos[key] = value
        #validate allele_count
        if self.__stat['allele_count'] != map(lambda x: int(x), infos['AC'].split(',')):
            raise Exception("Invalid 'allele_count' calculation", self.__stat['allele_count'], infos['AC'].split(','))
        #validate genotype_count
        if self.__stat['genotype_count'] != (int(infos['AN'])/2):
            raise Exception("Invalid 'allele_count' calculation", self.__stat['genotype_count'], infos['AN']/2)

    @property
    def key(self):
        key_fmt = "{chrom}|{pos}"
        return key_fmt.format(chrom=self.chrom,
                              pos=self.pos)

    @property
    def genotype_fields(self):
        if self.__genotype_fields is not None:
            return self.__genotype_fields
        else:
            return map(lambda x: GenotypeFieldRecord(x, self.ref, self.alt),
                       map(lambda y: self.others[y], self.__genotype_idx))

    @genotype_fields.setter
    def genotype_fields(self, value):
        self.__genotype_fields = value

    #******* No real use. Existing just for validating the counting method *******
    @property
    def allele_count(self):
        if self.__stat is None:
            self.__stat = self.calculate_stat()
            self.validate_stat()
        return self.__stat['allele_count']

    @property
    def patient_count(self):
        if self.__stat is None:
            self.__stat = self.calculate_stat()
            self.validate_stat()
        return self.__stat['patient_count']

    @property
    def genotype_count(self):
        if self.__stat is None:
            self.__stat = self.calculate_stat()
            self.validate_stat()
        return self.__stat['genotype_count']


class VcfDB(LinkAnaBase):
    """ to connect to merged vcf database """

    def __init__(self):
        self.__vcf_db_gz_file = None
        self.__header = None

    def get_raw_repr(self):
        return str({'vcf.gz file': self.__vcf_db_gz_file,
                    'chrom': self.__chrom,
                    'begin position': self.__begin_pos,
                    'end position': self.__end_pos,
                    })

    def __open_db(self,
                  vcf_db_gz_file,
                  chrom=None,
                  begin_pos=None,
                  end_pos=None,
                  patient_codes=None,
                  ):
        self.__vcf_db_gz_file = vcf_db_gz_file
        self.__chrom = chrom
        self.__begin_pos = begin_pos
        self.__end_pos = end_pos
        self.__patient_codes = patient_codes

    def open_db(self,
                vcf_db_gz_file,
                chrom=None,
                begin_pos=None,
                end_pos=None,
                patient_codes=None,
                ):
        return self.__open_db(vcf_db_gz_file,
                              chrom,
                              begin_pos,
                              end_pos,
                              patient_codes,
                              )

    @property
    def tabix_params(self):
        params = OrderedDict()
        params["reference"]=self.__chrom
        if self.__begin_pos is not None:
            params["start"]=int(self.__begin_pos)-1
        if self.__end_pos is not None:
            params["end"]=int(self.__end_pos)
        fmt = "{key}: {val}"
        info = []
        for key in params:
            info.append(fmt.format(key=key, val=params[key]))
        self.info("[tabix params] " + "\t".join(info))
        return params

    @property
    def header(self):
        if self.__header is None:
            header = get_raw_vcf_gz_header(self.__vcf_db_gz_file)
            self.__header = VcfDBHeaderRecord(header.strip("#").strip(), self.__patient_codes)
        return self.__header

    @property
    def records(self):
        tabix_file = pysam.Tabixfile(self.__vcf_db_gz_file)
        genotype_idx = self.header.genotype_idx
        for line in tabix_file.fetch(**self.tabix_params):
            yield VcfDBContentRecord(line.strip(), genotype_idx)
