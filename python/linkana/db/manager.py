import linkana.settings as lka_const
import gc
from linkana.template import LinkAnaBase
from linkana.db.connectors.sadb import SummarizeAnnovarDB
from linkana.db.connectors.vcfdb import VcfDB
from linkana.db.connectors.familydb import FamilyDB
from linkana.db.connectors.vcfdb import ZYGOSITY_UNKNOWN
from linkana.db.connectors.vcfdb import ZYGOSITY_NONE
from linkana.settings import TYPE1_ALL
from linkana.settings import TYPE2_RECTAL
from linkana.settings import TYPE2_NON_RECTAL
from linkana.settings import TYPE3_COLON
from linkana.settings import TYPE3_NON_COLON
from linkana.settings import TYPE4_CAFAM
from linkana.settings import TYPE4_NON_CAFAM


class PatientRecord(LinkAnaBase):
    """ to automatically parse VCF data"""

    def __init__(self):
        self.genotype_fields = {}
        self.patient_code = ''
        self.type2 = None
        self.type3 = None
        self.type4 = None

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

    def get_raw_repr(self):
        return str({'Connector': self.__get_connector(),
                    })

    def __get_connector(self):
        return self.__connector

    def add_connector(self, summarize_annovar_db_connector):
        self.__connector = summarize_annovar_db_connector
        self.__need_update = True

    def __update_mutations_table(self):
        self.__mutations = {}
        #create table
        for record in self.__connector.records:
            self.__mutations[record.key] = record
        self.__need_update = False

    @property
    def mutations(self):
        if self.__need_update:
            self.__update_mutations_table()
        return self.__mutations


class AbstractVcfDB(LinkAnaBase):
    """

    1. an abstract connection to VCF databases
    XXXX 2. able to handle many VcfDB connectors
    XXXX 3. build up 2D mutations table (mutation, patient)
    4. provide accesses to the content of VcfDB
        - using mutation key
        - using patient code
    5. provide a filtering function
        - common mutations given patient code(s)

    """

    def __init__(self, patient_codes=None):
        LinkAnaBase.__init__(self)
        self.__connectors = []
        self.__mutations = {}
        self.__patient_codes = patient_codes

    def get_raw_repr(self):
        return str({'Connectors': self.__get_connectors(),
                    })

    def __get_connectors(self):
        return self.__connectors

    def add_connector(self, vcf_db_connector):
        self.__connectors.append(vcf_db_connector)
        self.__need_update = True

    def __update_mutations_table(self):
        """

        - It will ssume that all overlapped records from different VcfDBs
        have the same content
        - The table should have only mutations from the target patients,
        and should filter out the blank (.\.) ones

        """

        self.info("building VCF mutations table")
        self.__mutations = {}
        self.__patients = {}
        for connector in self.__connectors:
#            if self.patient_codes is not None:
#                #please add test to validate the patient codes
#                patient_codes = self.patient_codes
#            else:
#                header = connector.header
#                patient_codes = header.patient_codes
#                patient_codes_idx = range(patient_codes)
#            print "[debugging] target patient codes :", self.__patient_codes
            header = connector.header
            #init patients content
            for patient_code in header.patient_codes:
                if patient_code not in self.__patients:
                    self.__patients[patient_code] = PatientRecord()
                    self.__patients[patient_code].patient_code = patient_code
            #create table
            record_count = 0
#            self.debug(header.patient_codes)
            for record in connector.records:
                #check if there are mutations
                has_genotype = False
                for i in xrange(len(header.patient_codes)):
                    if record.genotype_fields[i].raw_gt != './.':
                        has_genotype = True
                if not has_genotype:
                    continue
                #add record to the table
                mutation_genotype_fields = {}
                for i in xrange(len(header.patient_codes)):
                    patient_code = header.patient_codes[i]
                    genotype_fields = record.genotype_fields[i]
                    #add pointer to patient record(column)
        #            genotype_fields.patient = self.__patients[patient_code]
                    #add pointer to mutation record(row)
        #            genotype_fields.mutation = record
                    #give mutation an access to genotype field using patient code as a key
                    mutation_genotype_fields[patient_code] = genotype_fields
                    #give patient an access to genotype field using mutaion key as a key
        #            self.__patients[patient_code].genotype_fields[record.key] = genotype_fields
                record.genotype_fields = mutation_genotype_fields
                del genotype_fields
                gc.collect()
                self.__mutations[record.key] = record
                record_count += 1
                if (record_count % 1000) == 0:
                    self.info("record count: " + str(record_count))
        self.__need_update = False

    def common_mutations(self, patient_codes, exom_only=False):
        """

        return dict of mutations that are found in all patient
        given patient codes

        """

        common_mutations = {}
        #iterate through all patients in all mutations and pick
        #only the common ones
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
            self.__update_mutations_table()
        return self.__patients

    @property
    def mutations(self):
        if self.__need_update:
            self.__update_mutations_table()
        return self.__mutations

    @property
    def patient_codes(self):
        return self.__patient_codes


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
        self.__group_members_count = {}

    def get_raw_repr(self):
        return str({'Connectors': self.__get_connector(),
                    })

    def __get_connector(self):
        return self.__connector

    def add_connector(self, family_db_connector):
        self.__connector = family_db_connector
        self.__need_update = True

    def __update_group_members_count(self):
        group_members_count = {}
        group_members_count[TYPE1_ALL] = 0
        group_members_count[TYPE2_RECTAL] = 0
        group_members_count[TYPE2_NON_RECTAL] = 0
        group_members_count[TYPE3_COLON] = 0
        group_members_count[TYPE3_NON_COLON] = 0
        group_members_count[TYPE4_CAFAM] = 0
        group_members_count[TYPE4_NON_CAFAM] = 0
        for record in self.__connector.records:
            if record.type2 == TYPE2_RECTAL:
                group_members_count[TYPE2_RECTAL] += len(record.patient_codes)
            else:
                group_members_count[TYPE2_NON_RECTAL] += len(record.patient_codes)
            if record.type3 == TYPE3_COLON:
                group_members_count[TYPE3_COLON] += len(record.patient_codes)
            else:
                group_members_count[TYPE3_NON_COLON] += len(record.patient_codes)
            if record.type4 == TYPE4_CAFAM:
                group_members_count[TYPE4_CAFAM] += len(record.patient_codes)
            else:
                group_members_count[TYPE4_NON_CAFAM] += len(record.patient_codes)
            group_members_count[TYPE1_ALL] += len(record.patient_codes)
        self.__group_members_count = group_members_count
        self.__need_update = False

    def __update_families_table(self):
        self.__families = {}
        #create table
        for record in self.__connector.records:
            self.__families[record.family_code] = record
        self.__need_update = False

    @property
    def group_members_count(self):
        if self.__need_update:
            self.__update_families_table()
            self.__update_group_members_count()
        return self.__group_members_count

    @property
    def families(self):
        if self.__need_update:
            self.__update_families_table()
            self.__update_group_members_count()
        return self.__families


class DBManager(LinkAnaBase):
    """

    1. to handle all the connection to all related databases
    2. to provide the simplest interface to downstream classes
        - provide abstract connection for each db type
    3. The algorithm is basically
        - Prior to getting the content, all connections are just lazy
          connected.
        - Once the content is requested, the actual connection parameter is
          computed, and the actual connection is linked. So the actual content
          is produced.

    """

    def __init__(self, patient_codes=None):
        LinkAnaBase.__init__(self)
        self.__abs_sa_db = AbstractSummarizeAnnovarDB()
        self.__abs_vcf_db = AbstractVcfDB(patient_codes)
        self.__abs_fam_db = AbstractFamilyDB()

    def get_raw_repr(self):
        return str({'SummarizeAnnovarDB': self.__get_summarize_annovar_db_connection(),
                    'VcfDB': self.__get_vcf_db_connection(),
                    'FamilyDB': self.__get_family_db_connection(),
                    })

    def __get_summarize_annovar_db_connection(self):
        return self.__abs_sa_db

    def __get_vcf_db_connection(self):
        return self.__abs_vcf_db

    def __get_family_db_connection(self):
        return self.__abs_fam_db

    def __connect_summarize_annovar_db(self, csv_file, delimiter='\t'):
        self.info("creating summarize-annovar db connection to " + csv_file)
        sa_db = SummarizeAnnovarDB()
        sa_db.open_db(csv_file, delimiter)
        self.__abs_sa_db.add_connector(sa_db)

    def connect_summarize_annovar_db(self, csv_file, delimiter='\t'):
        return self.__connect_summarize_annovar_db(csv_file, delimiter)

    def __connect_vcf_db(self,
                         vcf_db_gz_file,
                         chrom,
                         begin_pos,
                         end_pos,
                         patient_codes=None,
                         ):
        self.info("creating vcf db connection to " + vcf_db_gz_file)
        #self.info("\t\tchrom: " + str(chrom) + "\tbegin pos: " + str(begin_pos) + "\tend_pos:" + str(end_pos))
        vcf_db = VcfDB()
        vcf_db.open_db(vcf_db_gz_file,
                       chrom,
                       begin_pos,
                       end_pos,
                       patient_codes=patient_codes,
                       )
        self.__abs_vcf_db.add_connector(vcf_db)

    def connect_vcf_db(self,
                       vcf_db_gz_file,
                       chrom,
                       begin_pos,
                       end_pos,
                       patient_codes=None,
                       ):
        return self.__connect_vcf_db(vcf_db_gz_file,
                                     chrom,
                                     begin_pos,
                                     end_pos,
                                     patient_codes=patient_codes,
                                     )

    def __connect_family_db(self, family_db_file):
        self.info("creating family db connection to " + family_db_file)
        fam_db = FamilyDB()
        fam_db.open_db(family_db_file)
        self.__abs_fam_db.add_connector(fam_db)

    def connect_family_db(self, family_db_file):
        return self.__connect_family_db(family_db_file)

    @property
    def summarize_annovar_db(self):
        return self.__abs_sa_db

    @property
    def vcf_db(self):
        return self.__abs_vcf_db

    @property
    def family_db(self):
        return self.__abs_fam_db

    @property
    def valid_patient_codes(self):
        """

        to check if members that appear in family file are also in
        Vcf database

        """

        vcf_patients = self.vcf_db.patients
        families = self.family_db.families

        for family_code in families:
            for patient_code in families[family_code].patient_codes:
                if patient_code not in vcf_patients:
                    self.info("patient code " + patient_code + " not found")
                    return False
        return True
