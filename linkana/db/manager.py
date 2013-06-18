import pysam
import csv
import linkana.settings as lka_const
from linkana.template import LinkAnaBase
from linkana.db.connectors import SummarizeAnnovarDB
from linkana.db.connectors import VcfDB
from linkana.db.connectors import FamilyDB


class AbstractVcfDB(LinkAnaBase):
    """

    1. an abstract connection to VCF databases
    2. able to handle many VcfDB connectors
    3. provide access to the content of VcfDB
        - list of patient codes
        - list of mutation_keys
        - list of mutations content (in dictionary format)
        - list of patient content (in dictionary format)

    """

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.__connectors = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'Connectors': self.__get_connectors(),
                    })

    def __get_connectors(self):
        return self.__connectors

    def add_connector(self, vcf_db_connector):
        self.__connectors.append(vcf_db_connector)

    @property
    def mutation_keys(self):
        for connector in self.__connectors:
            for record in connector.records:
                yield record.key

    @property
    def patient_codes(self):
        """ assume that all VcfDB are from the same set of patients """
        return self.__connectors[0].header.patient_codes

    def get_mutations(self):
        """

        assume that all overlapped records from different VcfDBs
        have the same content

        """

        mutations = {}
        for connector in self.__connectors:
            header = connector.header
            for record in connector.records:
                patient_contents = {}
                for i in xrange(len(header.patient_codes)):
                    patient_contents[header.patient_codes[i]] = record.patient_contents[i]
                record.patient_contents = patient_contents
                mutations[record.key] = record
        return mutations

    @property
    def patient_contents(self, patient_code):
        return 'Not yet implementedi, interface should be revised'


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
