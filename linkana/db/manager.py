import pysam
import csv
import linkana.settings as lka_const
from collections import OrderedDict
from linkana.template import LinkAnaBase
from linkana.db.connectors import SummarizeAnnovarDB
from linkana.db.connectors import VcfDB
from linkana.db.connectors import FamilyDB


class PatientRecord(object):
    """ to automatically parse VCF data"""

    def __init__(self):
        self.genotype_fields = {}
        self.patient_code = ''

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.get_raw_repr())

    def get_raw_repr(self):
        return "Patient record"
#        return {'raw content': self.raw_content,
#                'raw genotype': self.raw_gt,
#                'vcf mutations': self.vcf_mutations,
#                'annovar mutations': self.annovar_mutations,
#                'zygosity': self.zygosity,
#                }

class AbstractVcfDB(LinkAnaBase):
    """

    1. an abstract connection to VCF databases
    2. able to handle many VcfDB connectors
    2. build up 2D mutations table (mutation, patient)
    3. provide access to the content of VcfDB
        - mutation perspective
        - patient perspective

    """

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.__connectors = []
        self.__mutations = {}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'Connectors': self.__get_connectors(),
                    })

    def __get_connectors(self):
        return self.__connectors

    def add_connector(self, vcf_db_connector):
        self.__connectors.append(vcf_db_connector)
        self.__need_update = True

    def __update_mutaitions_table(self):
        """

        assume that all overlapped records from different VcfDBs
        have the same content

        """

        self.__mutations = {}
        self.__patients = {}
        for connector in self.__connectors:
            header = connector.header
            #init patients content
            for patient_code in header.patient_codes:
                if patient_code not in self.__patients:
                    self.__patients[patient_code] = PatientRecord()
                    self.__patients[patient_code].patient_code = patient_code
            for record in connector.records:
                mutation_genotype_fields = {}
                for i in xrange(len(header.patient_codes)):
                    patient_code = header.patient_codes[i]
                    genotype_fields = record.genotype_fields[i]
                    #add pointer to patient record(column)
                    #genotype_fields.patient = 20
                    genotype_fields.patient = self.__patients[patient_code]
                    #add pointer to mutation record(row)
                    genotype_fields.mutation = record
                    #give mutation an access to genotype field using patient code as a key
                    mutation_genotype_fields[patient_code] = genotype_fields
                    #give patient an access to genotype field using mutaion key as a key
                    self.__patients[patient_code].genotype_fields[record.key] = genotype_fields
                record.genotype_fields = mutation_genotype_fields
                self.__mutations[record.key] = record
        self.__need_update = False

#    @property
#    def mutation_keys(self):
#        for connector in self.__connectors:
#            for record in connector.records:
#                yield record.key
#
#    @property
#    def patient_codes(self):
#        """ assume that all VcfDB are from the same set of patients """
#        return self.__connectors[0].header.patient_codes
#
    @property
    def patients(self):
        if self.__need_update:
            self.__update_mutaitions_table()

        return self.__patients

    @property
    def mutations(self):
        if self.__need_update:
            self.__update_mutaitions_table()

        return self.__mutations

#    def get_patients(self, patient_code):
#        if self.__need_update:
#            self.__update_mutaitions_table()
#        for connector in self.__connectors:
#            header = connector.header
#            patient_idx = header.patient_codes.index(patient_code)
#            for record in connector.records:
#                yield record.genotype_fields[patient_idx]


class DBManager(LinkAnaBase):
    """

    1. to handle all the connection to all databases
    2. to provide the simplest interface to downstream classes
        - provide abstract connection for each db type

    """

    def __init__(self):
        LinkAnaBase.__init__(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'SummarizeAnnovarDB': self.__get_summarize_annovar_db_connection(),
                    'VcfDB': self.__get_vcf_db_connection(),
                    'FamilyDB': self.__get_family_db_connection(),
                    })

    def __get_summarize_annovar_db_connection(self):
        return 'Not yet implemented'

    def __get_vcf_db_connection(self):
        return 'Not yet implemented'

    def __get_family_db_connection(self):
        return 'Not yet implemented'

    def __connect_summarize_annovar_db(self, csv_file, delimiter='\t'):
        return 'Not yet implemented'

    def __connect_vcf_db(self, vcf_db_gz_file, chrom, begin_pos, end_pos):
        return 'Not yet implemented'

    def __connect_family_db(self, family_db_file):
        return 'Not yet implemented'

    @property
    def summarize_annovar_db(self):
        return 'Not yet implemented'

    @property
    def vcf_db(self):
        return 'Not yet implemented'

    @property
    def family_db(self):
        return 'Not yet implemented'
