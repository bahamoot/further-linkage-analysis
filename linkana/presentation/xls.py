import linkana.settings as lka_const
from linkana.template import LinkAnaBase

TYPE3_CAFAM = 'CAFAM'
TYPE3_NON_CAFAM = 'NON_CAFAM'


class MutationAnnotator(LinkAnaBase):
    """

    Given Vcf, SummarizeAnnovar and patients information,
    this class is responsible for exporting them in "Daniel" xls format

    """

    def __init__(self):
        LinkAnaBase.__init__(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.__get_raw_repr())

    def __get_raw_repr(self):
        return "to be discussed"

    def __export_xls(self, directory):
        """ export mutations from all families to the given directory """
        pass

    def __annotate_patient_group(self):
        """ to identify patient group in patient record """
        vcf_patients = self.__vcf_patients
        families = self.__families
        for family_code in families:
            family = families[family_code]
            for patient_code in family.patient_codes:
                if family.type3 == TYPE3_CAFAM:
                    vcf_patients[patient_code].type3 = TYPE3_CAFAM
                else:
                    vcf_patients[patient_code].type3 = TYPE3_NON_CAFAM

    def __annotate_group_stat(self):
        """ calculate group stat for each mutation record """

        vcf_mutations = self.__vcf_mutations
        vcf_patients = self.__vcf_patients
        cafam_patient_codes = filter(lambda x: vcf_patients[x].type3 == TYPE3_CAFAM, vcf_patients)
        non_cafam_patient_codes = filter(lambda x: vcf_patients[x].type3 == TYPE3_NON_CAFAM, vcf_patients)
        for mutation_key in vcf_mutations:
            mutation = vcf_mutations[mutation_key]
            #calculate stat for CAFAM group
            cafam_genotypes = map(lambda x: mutation.genotype_fields[x],
                                  cafam_patient_codes)
            stat = mutation.calculate_stat(cafam_genotypes)
            mutation.group_stat[TYPE3_CAFAM] = stat
            #calculate stat for those outside CAFAM group
            non_cafam_genotypes = map(lambda x: mutation.genotype_fields[x],
                                      non_cafam_patient_codes)
            stat = mutation.calculate_stat(non_cafam_genotypes)
            mutation.group_stat[TYPE3_NON_CAFAM] = stat

    def __get_xls_record(self, patient_code):
        yield None

    @property
    def vcf_mutations(self):
        return self.__vcf_mutations

    @property
    def db_manager(self):
        return self.__db_manager

    @db_manager.setter
    def db_manager(self, value):
        self.__db_manager = value
        if not self.__db_manager.valid_patient_codes:
            self.throw("Invalid patient codes either in Vcf database or Family data. Please check")
        self.__sa_mutations = self.__db_manager.summarize_annovar_db.mutations
        self.__vcf_patients = self.__db_manager.vcf_db.patients
        self.__vcf_mutations = self.__db_manager.vcf_db.mutations
        self.__families = self.__db_manager.family_db.families
        self.__annotate_patient_group()
        self.__annotate_group_stat()

    @property
    def xls_header(self):
        pass


