import pysam
import csv
import linkana.settings as lka_const
from collections import OrderedDict
from linkana.template import LinkAnaBase
from linkana.db.connectors import SummarizeAnnovarDB
from linkana.db.connectors import VcfDB
from linkana.db.connectors import FamilyDB
from linkana.db.connectors import ZYGOSITY_UNKNOWN
from linkana.db.connectors import ZYGOSITY_NONE


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
        return {"patient code": self.patient_code}


class AbstractSummarizeAnnovarDB(LinkAnaBase):
    """

    #1. an abstract connection to Summarize Annovar databases(not yet implemented)
    #2. able to handle many SummarizeAnnovarDB connectors(not yet implemented)
    3. a mutation annotation record can be accessed using mutation key

    """

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.__connector = None
        self.__mutations = {}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'Connector': self.__get_connector(),
                    })

    def __get_connector(self):
        return self.__connector

    def add_connector(self, summarize_annovar_db_connector):
        self.__connector = summarize_annovar_db_connector
        self.__need_update = True

    def __update_mutaitions_table(self):
        self.__mutations = {}
        #create table
        for record in self.__connector.records:
            self.__mutations[record.key] = record
        self.__need_update = False

    @property
    def mutations(self):
        if self.__need_update:
            self.__update_mutaitions_table()
        return self.__mutations


class AbstractVcfDB(LinkAnaBase):
    """

    1. an abstract connection to VCF databases
    2. able to handle many VcfDB connectors
    3. build up 2D mutations table (mutation, patient)
    4. provide accesses to the content of VcfDB
        - using mutation key
        - using patient code
    5. provide a filtering function
        - common mutations given patient code(s)

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
            #create table
            for record in connector.records:
                mutation_genotype_fields = {}
                for i in xrange(len(header.patient_codes)):
                    patient_code = header.patient_codes[i]
                    genotype_fields = record.genotype_fields[i]
                    #add pointer to patient record(column)
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

    def common_mutations(self, patient_codes):
        """

        return dict of mutations that are found in all patient
        given patient codes

        """

        common_mutations = {}
        for mutation_key in self.mutations:
            mutation = self.mutations[mutation_key]
            common_mutation = True
            for patient_code in patient_codes:
                zygosity = mutation.genotype_fields[patient_code].zygosity
                if zygosity == ZYGOSITY_UNKNOWN:
                    common_mutation = False
                    break
                if zygosity == ZYGOSITY_NONE:
                    common_mutation = False
                    break
            if common_mutation:
                common_mutations[mutation_key] = mutation
        return common_mutations


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


class AbstractFamilyDB(LinkAnaBase):
    """

    #1. an abstract connection to Family databases(not yet implemented)
    #2. able to handle many FamilyDB connectors(not yet implemented)
    3. a family (members) record can be accessed by family code

    """

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.__connector = None
        self.__families = {}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'Connectors': self.__get_connector(),
                    })

    def __get_connector(self):
        return self.__connector

    def add_connector(self, family_db_connector):
        self.__connector = family_db_connector
        self.__need_update = True

    def __update_families_table(self):
        self.__families = {}
        #create table
        for record in self.__connector.records:
            self.__families[record.family_code] = record
        self.__need_update = False

    @property
    def families(self):
        if self.__need_update:
            self.__update_families_table()
        return self.__families


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
