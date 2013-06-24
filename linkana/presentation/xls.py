import os
import xlwt
import linkana.settings as lka_const
from linkana.template import LinkAnaBase

TYPE3_CAFAM = 'CAFAM'
TYPE3_NON_CAFAM = 'NON_CAFAM'

MA_COL_0_IDX_FUNC = 0
MA_COL_0_IDX_GENE = 1
MA_COL_0_IDX_EXONICFUNC = 2
MA_COL_0_IDX_AACHANGE = 3
MA_COL_0_IDX_CONSERVED = 4
MA_COL_0_IDX_SEGDUP = 5
MA_COL_0_IDX_ESP6500_ALL = 6
MA_COL_0_IDX_1000G2012APR_ALL = 7
MA_COL_0_IDX_DBSNP137 = 8
MA_COL_0_IDX_ALL_STAT_AC = 9
MA_COL_0_IDX_ALL_STAT_PC = 10
MA_COL_0_IDX_ALL_STAT_GC = 11
MA_COL_0_IDX_IN_STAT_AC = 12
MA_COL_0_IDX_IN_STAT_PC = 13
MA_COL_0_IDX_IN_STAT_GC = 14
MA_COL_0_IDX_AVSIFT = 15
MA_COL_0_IDX_LJB_PHYLOP = 16
MA_COL_0_IDX_LJB_PHYLOP_PRED = 17
MA_COL_0_IDX_LJB_SIFT = 18
MA_COL_0_IDX_LJB_SIFT_PRED = 19
MA_COL_0_IDX_LJB_POLYPHEN2 = 20
MA_COL_0_IDX_LJB_POLYPHEN2_PRED = 21
MA_COL_0_IDX_LJB_LRT = 22
MA_COL_0_IDX_LJB_LRT_PRED = 23
MA_COL_0_IDX_LJB_MT = 24
MA_COL_0_IDX_LJB_MT_PRED = 25
MA_COL_0_IDX_LJB_GERP = 26
MA_COL_0_IDX_CHROM = 27
MA_COL_0_IDX_START = 28
MA_COL_0_IDX_END = 29
MA_COL_0_IDX_REF = 30
MA_COL_0_IDX_OBS = 31
MA_COL_0_IDX_ZYGOSITY = 32


class MutationAnnotator(LinkAnaBase):
    """

    Given Vcf, SummarizeAnnovar and patients information,
    this class is responsible for exporting them in "Daniel" xls format

    """

    def __init__(self, report_code='ma'):
        LinkAnaBase.__init__(self)
        self.__report_code = report_code

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.__get_raw_repr())

    def __get_raw_repr(self):
        return "to be discussed"

    def __export_xls(self, directory=None):
        """ export mutations from all families to the given directory """
        pass

    def __add_csv_sheet(self, wb, sheet_name, patient_codes, st):
        ws = wb.add_sheet(sheet_name)
        #header
        ws.write(0, MA_COL_0_IDX_FUNC, 'Func')
        ws.write(0, MA_COL_0_IDX_GENE, 'Gene')
        ws.write(0, MA_COL_0_IDX_EXONICFUNC, 'ExonicFunc')
        ws.write(0, MA_COL_0_IDX_AACHANGE, 'AAChange')
        ws.write(0, MA_COL_0_IDX_CONSERVED, 'Conserved')
        ws.write(0, MA_COL_0_IDX_SEGDUP, 'SegDup')
        ws.write(0, MA_COL_0_IDX_ESP6500_ALL, 'ESP6500_ALL')
        ws.write(0, MA_COL_0_IDX_1000G2012APR_ALL, '1000g2012apr_ALL')
        ws.write(0, MA_COL_0_IDX_DBSNP137, 'dbSNP137')
        ws.write(0, MA_COL_0_IDX_ALL_STAT_AC, 'Allele Count (all)')
        ws.write(0, MA_COL_0_IDX_ALL_STAT_PC, 'Patient Count (all)')
        ws.write(0, MA_COL_0_IDX_ALL_STAT_GC, 'Genotype Count (all)')
        ws.write(0, MA_COL_0_IDX_IN_STAT_AC, 'Allele Count (group)')
        ws.write(0, MA_COL_0_IDX_IN_STAT_PC, 'Patient Count (group)')
        ws.write(0, MA_COL_0_IDX_IN_STAT_GC, 'Genoytpe Count (group)')
        ws.write(0, MA_COL_0_IDX_AVSIFT, 'AVSIFT')
        ws.write(0, MA_COL_0_IDX_LJB_PHYLOP, 'PhyloP')
        ws.write(0, MA_COL_0_IDX_LJB_PHYLOP_PRED, 'PhyloP prediction')
        ws.write(0, MA_COL_0_IDX_LJB_SIFT, 'SIFT')
        ws.write(0, MA_COL_0_IDX_LJB_SIFT_PRED, 'SIFT prediction')
        ws.write(0, MA_COL_0_IDX_LJB_POLYPHEN2, 'PolyPhen2')
        ws.write(0, MA_COL_0_IDX_LJB_POLYPHEN2_PRED, 'PolyPhen2 prediction')
        ws.write(0, MA_COL_0_IDX_LJB_LRT, 'LRT')
        ws.write(0, MA_COL_0_IDX_LJB_LRT_PRED, 'LRT prediction')
        ws.write(0, MA_COL_0_IDX_LJB_MT, 'Mutation Taster')
        ws.write(0, MA_COL_0_IDX_LJB_MT_PRED, 'Mutation Taster prediction')
        ws.write(0, MA_COL_0_IDX_LJB_GERP, 'GERP++')
        ws.write(0, MA_COL_0_IDX_CHROM, 'Chr')
        ws.write(0, MA_COL_0_IDX_START, 'Start')
        ws.write(0, MA_COL_0_IDX_END, 'End')
        ws.write(0, MA_COL_0_IDX_REF, 'Ref')
        ws.write(0, MA_COL_0_IDX_OBS, 'Obs')
        ws.write(0, MA_COL_0_IDX_ZYGOSITY, 'Zygosity')

        #content
        normal_style = xlwt.XFStyle()
        row = 0
        for xls_record in self.__get_xls_records(patient_codes):
            row += 1
            ws.write(row, MA_COL_0_IDX_FUNC, xls_record.func)
            ws.write(row, MA_COL_0_IDX_GENE, xls_record.gene, normal_style)
            ws.write(row, MA_COL_0_IDX_EXONICFUNC, xls_record.exonic_func, st)
            ws.write(row, MA_COL_0_IDX_AACHANGE, xls_record.aa_change)
            ws.write(row, MA_COL_0_IDX_CONSERVED, xls_record.conserved)
            ws.write(row, MA_COL_0_IDX_SEGDUP, xls_record.seg_dup)
            ws.write(row, MA_COL_0_IDX_ESP6500_ALL, xls_record.esp6500_all)
            ws.write(row, MA_COL_0_IDX_1000G2012APR_ALL, xls_record.maf)
            ws.write(row, MA_COL_0_IDX_DBSNP137, xls_record.dbsnp137)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_AC, xls_record.all_ac)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_PC, xls_record.all_pc)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_GC, xls_record.all_gc)
            ws.write(row, MA_COL_0_IDX_IN_STAT_AC, xls_record.group_ac)
            ws.write(row, MA_COL_0_IDX_IN_STAT_PC, xls_record.group_pc)
            ws.write(row, MA_COL_0_IDX_IN_STAT_GC, xls_record.group_gc)
            ws.write(row, MA_COL_0_IDX_AVSIFT, xls_record.avsift)
            ws.write(row, MA_COL_0_IDX_LJB_PHYLOP, xls_record.ljb_phylop)
            ws.write(row, MA_COL_0_IDX_LJB_PHYLOP_PRED, xls_record.ljb_phylop_pred)
            ws.write(row, MA_COL_0_IDX_LJB_SIFT, xls_record.ljb_sift)
            ws.write(row, MA_COL_0_IDX_LJB_SIFT_PRED, xls_record.ljb_sift_pred)
            ws.write(row, MA_COL_0_IDX_LJB_POLYPHEN2, xls_record.ljb_polyphen2)
            ws.write(row, MA_COL_0_IDX_LJB_POLYPHEN2_PRED, xls_record.ljb_polyphen2_pred)
            ws.write(row, MA_COL_0_IDX_LJB_LRT, xls_record.ljb_lrt)
            ws.write(row, MA_COL_0_IDX_LJB_LRT_PRED, xls_record.ljb_lrt_pred)
            ws.write(row, MA_COL_0_IDX_LJB_MT, xls_record.ljb_mt)
            ws.write(row, MA_COL_0_IDX_LJB_MT_PRED, xls_record.ljb_mt_pred)
            ws.write(row, MA_COL_0_IDX_LJB_GERP, xls_record.ljb_gerp)
            ws.write(row, MA_COL_0_IDX_CHROM, xls_record.chrom)
            ws.write(row, MA_COL_0_IDX_START, xls_record.start_pos)
            ws.write(row, MA_COL_0_IDX_END, xls_record.end_pos)
            ws.write(row, MA_COL_0_IDX_REF, xls_record.ref)
            ws.write(row, MA_COL_0_IDX_OBS, xls_record.obs)
            ws.write(row, MA_COL_0_IDX_ZYGOSITY, xls_record.zygosity)
#        with open(csv_file, 'rb') as csvfile:
#            csv_records = list(csv.reader(csvfile, delimiter='\t'))
#            for row in xrange(len(csv_records)):
#                csv_record = csv_records[row]
#                csv_record = split_last_extra_info(explain_annotation(csv_record), sheet_name)
#                for col in xrange(len(csv_record)):
#                    if (isFloat(csv_record[7]) and (float(csv_record[7])<=0.1)) or (csv_record[7]=='') :
#                        if (csv_record[2] != 'synonymous SNV'):
#                            ws.write(row, col, csv_record[col], st)
#                        else:
#                            ws.write(row, col, csv_record[col])
#                    else:
#                        ws.write(row, col, csv_record[col])
        ws.set_panes_frozen(True)
        ws.set_horz_split_pos(1)
        ws.set_remove_splits(True)

    def __export_family_xls(self, family_code, directory=None):
        """ export mutations for one family to the given directory """
        file_name = 'family' + family_code + '_' + self.__report_code + '.xls'
        output_file = os.path.join(directory, file_name)

        wb = xlwt.Workbook()

        yellow_st = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
#        yellow_st = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
        for patient_code in self.__families[family_code].patient_codes:
            print
            print
            print patient_code
            self.__add_csv_sheet(wb, patient_code, [patient_code], yellow_st)
        print
        print
        self.__add_csv_sheet(wb, 'In common', self.__families[family_code].patient_codes, yellow_st)
        wb.save(output_file)

    def export_family_xls(self, family_code, directory=None):
        """ export mutations for one family to the given directory """
        return self.__export_family_xls(family_code, directory)

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

    @property
    def xls_header(self):
        pass

    def __get_xls_records(self, patient_codes):
        """ prepare data for one data sheet """
        xls_records = []
        group = self.__vcf_patients[patient_codes[0]].type3
        sa_key_fmt = "{vcf_mutation_key}|{ref}|{obs}"
        for vcf_mutation_key in self.__db_manager.vcf_db.common_mutations(patient_codes):
            vcf_mutation = self.__vcf_mutations[vcf_mutation_key]
            genotype_field = vcf_mutation.genotype_fields[patient_codes[0]]
            gt = genotype_field.raw_gt.split('/')
            annovar_mutations = genotype_field.annovar_mutations
            print gt
            print genotype_field
            print vcf_mutation.ref
            print vcf_mutation.alt
            print self.__vcf_mutations[vcf_mutation_key].group_stat[group]
            print "vcf_mutation.allele_count:", vcf_mutation.allele_count
            annovar_idx = 0
            if gt[0] != '0':
                sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
                                                    ref=annovar_mutations[annovar_idx]['ref'],
                                                    obs=annovar_mutations[annovar_idx]['alt'])
                annovar_idx += 1
                mutation = self.__sa_mutations[sa_mutation_key]
                mutation.zygosity = genotype_field.zygosity
                mutation.group_ac = vcf_mutation.group_stat[group]['allele_count'][int(gt[0])-1]
                mutation.group_pc = vcf_mutation.group_stat[group]['patient_count'][int(gt[0])-1]
                mutation.group_gc = vcf_mutation.group_stat[group]['genotype_count']
                mutation.all_ac = vcf_mutation.allele_count[int(gt[0])-1]
                mutation.all_pc = vcf_mutation.patient_count[int(gt[0])-1]
                mutation.all_gc = vcf_mutation.genotype_count
                xls_records.append(mutation)
            if (gt[1] != '0') and (gt[0] != gt[1]):
                sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
                                                    ref=annovar_mutations[annovar_idx]['ref'],
                                                    obs=annovar_mutations[annovar_idx]['alt'])
                mutation = self.__sa_mutations[sa_mutation_key]
                mutation.zygosity = genotype_field.zygosity
                mutation.group_ac = vcf_mutation.group_stat[group]['allele_count'][int(gt[1])-1]
                mutation.group_pc = vcf_mutation.group_stat[group]['patient_count'][int(gt[1])-1]
                mutation.group_gc = vcf_mutation.group_stat[group]['genotype_count']
                mutation.all_ac = vcf_mutation.allele_count[int(gt[1])-1]
                mutation.all_pc = vcf_mutation.patient_count[int(gt[1])-1]
                mutation.all_gc = vcf_mutation.genotype_count
                xls_records.append(mutation)
#            for annovar_mutation in genotype_field.annovar_mutations:
#                sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
#                                                    ref=annovar_mutation['ref'],
#                                                    obs=annovar_mutation['alt'])
#                print annovar_mutation
#            print mutation
#            print mutation.group_gc
        return sorted(xls_records, key=lambda record: record.maf, reverse=True)
#        xls_records = {}
#        for mutation_key in self.__db_manager.vcf_db.common_mutations(patient_codes):
#            xls_records[mutation_key] = self.__sa_mutations[mutation_key]
#        for mutation_key in xls_records:
#            print xls_records[mutation_key]
#        return xls_records

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


