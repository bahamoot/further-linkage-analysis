import os
import xlwt
import linkana.settings as lka_const
from linkana.template import LinkAnaBase
from linkana.settings import TYPE1_ALL
from linkana.settings import TYPE2_RECTAL
from linkana.settings import TYPE2_NON_RECTAL
from linkana.settings import TYPE3_COLON
from linkana.settings import TYPE3_NON_COLON
from linkana.settings import TYPE4_CAFAM
from linkana.settings import TYPE4_NON_CAFAM

ezxf = xlwt.easyxf

MA_COL_0_IDX_FUNC = 0
MA_COL_0_IDX_GENE = 1
MA_COL_0_IDX_EXONICFUNC = 2
MA_COL_0_IDX_AACHANGE = 3
MA_COL_0_IDX_1000G2012APR_ALL = 4
MA_COL_0_IDX_DBSNP137 = 5
MA_COL_0_IDX_ALL_STAT_AC = 6
MA_COL_0_IDX_ALL_STAT_PC = 7
MA_COL_0_IDX_ALL_STAT_PP = 8
MA_COL_0_IDX_ALL_STAT_GC = 9
MA_COL_0_IDX_ALL_STAT_GP = 10
MA_COL_0_IDX_TYPE2_STAT_AC = 11
MA_COL_0_IDX_TYPE2_STAT_PC = 12
MA_COL_0_IDX_TYPE2_STAT_PP = 13
MA_COL_0_IDX_TYPE2_STAT_GC = 14
MA_COL_0_IDX_TYPE2_STAT_GP = 15
MA_COL_0_IDX_TYPE3_STAT_AC = 16
MA_COL_0_IDX_TYPE3_STAT_PC = 17
MA_COL_0_IDX_TYPE3_STAT_PP = 18
MA_COL_0_IDX_TYPE3_STAT_GC = 19
MA_COL_0_IDX_TYPE3_STAT_GP = 20
MA_COL_0_IDX_TYPE4_STAT_AC = 21
MA_COL_0_IDX_TYPE4_STAT_PC = 22
MA_COL_0_IDX_TYPE4_STAT_PP = 23
MA_COL_0_IDX_TYPE4_STAT_GC = 24
MA_COL_0_IDX_TYPE4_STAT_GP = 25
MA_COL_0_IDX_AVSIFT = 26
MA_COL_0_IDX_LJB_PHYLOP = 27
MA_COL_0_IDX_LJB_PHYLOP_PRED = 28
MA_COL_0_IDX_LJB_SIFT = 29
MA_COL_0_IDX_LJB_SIFT_PRED = 30
MA_COL_0_IDX_LJB_POLYPHEN2 = 31
MA_COL_0_IDX_LJB_POLYPHEN2_PRED = 32
MA_COL_0_IDX_LJB_LRT = 33
MA_COL_0_IDX_LJB_LRT_PRED = 34
MA_COL_0_IDX_LJB_MT = 35
MA_COL_0_IDX_LJB_MT_PRED = 36
MA_COL_0_IDX_LJB_GERP = 37
MA_COL_0_IDX_CONSERVED = 38
MA_COL_0_IDX_SEGDUP = 39
MA_COL_0_IDX_ESP6500_ALL = 40
MA_COL_0_IDX_CHROM = 41
MA_COL_0_IDX_START = 42
MA_COL_0_IDX_END = 43
MA_COL_0_IDX_REF = 44
MA_COL_0_IDX_OBS = 45
MA_COL_0_IDX_ZYGOSITY = 46

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


class MutationAnnotator(LinkAnaBase):
    """

    Given Vcf, SummarizeAnnovar and patients information,
    this class is responsible for exporting them in "Daniel" xls format

    """

    def __init__(self, report_code='ma', exom_only=False):
        LinkAnaBase.__init__(self)
        self.__exom_only=exom_only
        self.__report_code = report_code

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.__get_raw_repr())

    def __get_raw_repr(self):
        return "to be discussed"

    def __export_xls(self, directory):
        """ export mutations from all families to the given directory """

        for family_code in self.__families:
            self.__export_family_xls(family_code, directory)

    def export_xls(self, directory):
        """ export mutations from all families to the given directory """

        return self.__export_xls(directory)

    def __write_header(self, ws,
                       header_type1,
                       header_type2,
                       header_type3,
                       header_type4,):
        default_heading_xf = ezxf('align: wrap on, vert centre, horiz center')
        ws.write_merge(0,2,
                       MA_COL_0_IDX_FUNC, MA_COL_0_IDX_FUNC,
                       'Func', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_GENE, MA_COL_0_IDX_GENE,
                       'Gene', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_EXONICFUNC, MA_COL_0_IDX_EXONICFUNC,
                       'ExonicFunc', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_AACHANGE, MA_COL_0_IDX_AACHANGE,
                       'AAChange', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_CONSERVED, MA_COL_0_IDX_CONSERVED,
                       'Conserved', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_SEGDUP, MA_COL_0_IDX_SEGDUP,
                       'SegDup', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_ESP6500_ALL, MA_COL_0_IDX_ESP6500_ALL,
                       'ESP6500_ALL', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_1000G2012APR_ALL, MA_COL_0_IDX_1000G2012APR_ALL,
                       '1000g2012apr_ALL', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_DBSNP137, MA_COL_0_IDX_DBSNP137,
                       'dbSNP137', default_heading_xf)

        ws.write_merge(0, 0,
                       MA_COL_0_IDX_ALL_STAT_AC, MA_COL_0_IDX_ALL_STAT_GP,
                       header_type1, default_heading_xf)
        ws.write_merge(1, 2,
                       MA_COL_0_IDX_ALL_STAT_AC, MA_COL_0_IDX_ALL_STAT_AC,
                       'No of alleles mutated', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_ALL_STAT_PC, MA_COL_0_IDX_ALL_STAT_PP,
                       'Patients with mutation', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_ALL_STAT_PC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_ALL_STAT_PP,
                 '%', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_ALL_STAT_GC, MA_COL_0_IDX_ALL_STAT_GP,
                       'Informative patients', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_ALL_STAT_GC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_ALL_STAT_GP,
                 '%', default_heading_xf)

        ws.write_merge(0, 0,
                       MA_COL_0_IDX_TYPE2_STAT_AC, MA_COL_0_IDX_TYPE2_STAT_GP,
                       header_type2, default_heading_xf)
        ws.write_merge(1, 2,
                       MA_COL_0_IDX_TYPE2_STAT_AC, MA_COL_0_IDX_TYPE2_STAT_AC,
                       'No of alleles mutated', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE2_STAT_PC, MA_COL_0_IDX_TYPE2_STAT_PP,
                       'Patients with mutation', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE2_STAT_PC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE2_STAT_PP,
                 '%', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE2_STAT_GC, MA_COL_0_IDX_TYPE2_STAT_GP,
                       'Informative patients', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE2_STAT_GC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE2_STAT_GP,
                 '%', default_heading_xf)

        ws.write_merge(0, 0,
                       MA_COL_0_IDX_TYPE3_STAT_AC, MA_COL_0_IDX_TYPE3_STAT_GP,
                       header_type3, default_heading_xf)
        ws.write_merge(1, 2,
                       MA_COL_0_IDX_TYPE3_STAT_AC, MA_COL_0_IDX_TYPE3_STAT_AC,
                       'No of alleles mutated', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE3_STAT_PC, MA_COL_0_IDX_TYPE3_STAT_PP,
                       'Patients with mutation', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE3_STAT_PC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE3_STAT_PP,
                 '%', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE3_STAT_GC, MA_COL_0_IDX_TYPE3_STAT_GP,
                       'Informative patients', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE3_STAT_GC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE3_STAT_GP,
                 '%', default_heading_xf)

        ws.write_merge(0, 0,
                       MA_COL_0_IDX_TYPE4_STAT_AC, MA_COL_0_IDX_TYPE4_STAT_GP,
                       header_type4, default_heading_xf)
        ws.write_merge(1, 2,
                       MA_COL_0_IDX_TYPE4_STAT_AC, MA_COL_0_IDX_TYPE4_STAT_AC,
                       'No of alleles mutated', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE4_STAT_PC, MA_COL_0_IDX_TYPE4_STAT_PP,
                       'Patients with mutation', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE4_STAT_PC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE4_STAT_PP,
                 '%', default_heading_xf)
        ws.write_merge(1, 1,
                       MA_COL_0_IDX_TYPE4_STAT_GC, MA_COL_0_IDX_TYPE4_STAT_GP,
                       'Informative patients', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE4_STAT_GC,
                 'No', default_heading_xf)
        ws.write(2,
                 MA_COL_0_IDX_TYPE4_STAT_GP,
                 '%', default_heading_xf)

        ws.write_merge(0, 2,
                       MA_COL_0_IDX_AVSIFT, MA_COL_0_IDX_AVSIFT,
                       'AVSIFT', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_PHYLOP, MA_COL_0_IDX_LJB_PHYLOP,
                       'PhyloP', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_PHYLOP_PRED, MA_COL_0_IDX_LJB_PHYLOP_PRED,
                       'PhyloP prediction', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_SIFT, MA_COL_0_IDX_LJB_SIFT,
                       'SIFT', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_SIFT_PRED, MA_COL_0_IDX_LJB_SIFT_PRED,
                       'SIFT prediction', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_POLYPHEN2, MA_COL_0_IDX_LJB_POLYPHEN2,
                       'PolyPhen2', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_POLYPHEN2_PRED, MA_COL_0_IDX_LJB_POLYPHEN2_PRED,
                       'PolyPhen2 prediction', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_LRT, MA_COL_0_IDX_LJB_LRT,
                       'LRT', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_LRT_PRED, MA_COL_0_IDX_LJB_LRT_PRED,
                       'LRT prediction', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_MT, MA_COL_0_IDX_LJB_MT,
                       'Mutation Taster', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_MT_PRED, MA_COL_0_IDX_LJB_MT_PRED,
                       'Mutation Taster prediction', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_LJB_GERP, MA_COL_0_IDX_LJB_GERP,
                       'GERP++', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_CHROM, MA_COL_0_IDX_CHROM,
                       'Chr', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_START, MA_COL_0_IDX_START,
                       'Start', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_END, MA_COL_0_IDX_END,
                       'End', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_REF, MA_COL_0_IDX_REF,
                       'Ref', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_OBS, MA_COL_0_IDX_OBS,
                       'Obs', default_heading_xf)
        ws.write_merge(0, 2,
                       MA_COL_0_IDX_ZYGOSITY, MA_COL_0_IDX_ZYGOSITY,
                       'Zygosity', default_heading_xf)
        ws.row(1).height = 720

    def __add_csv_sheet(self, wb,
                        family_code,
                        sheet_name,
                        patient_codes,
                        highlight_st,
                        ):
        group_members_count =  self.__group_members_count
        family = self.__families[family_code]
        group_header_fmt = "{group_txt} ({patients_count} patients)"
        header_type1 = group_header_fmt.format(group_txt='All',
                                               patients_count=group_members_count[TYPE1_ALL])
        header_type2 = group_header_fmt.format(group_txt='Group "Rectal Family"',
                                               patients_count=group_members_count[TYPE2_RECTAL])
        header_type3 = group_header_fmt.format(group_txt='Group "Colon Family"',
                                               patients_count=group_members_count[TYPE3_COLON])
        header_type4 = group_header_fmt.format(group_txt='Group "Cancer Family"',
                                               patients_count=group_members_count[TYPE4_CAFAM])

        ws = wb.add_sheet(sheet_name)
        self.__write_header(ws, header_type1, header_type2, header_type3, header_type4)

        #content
        row = 2
        default_st = xlwt.XFStyle()
        for xls_record in self.__get_xls_records(patient_codes):
            row += 1
            if (isFloat(xls_record.maf) and (float(xls_record.maf)<=0.1)) or (xls_record.maf=='') :
                if (xls_record.exonic_func != 'synonymous SNV'):
                    st = highlight_st
            else:
                st = default_st
            ws.write(row, MA_COL_0_IDX_FUNC, xls_record.func, st)
            ws.write(row, MA_COL_0_IDX_GENE, xls_record.gene, st)
            ws.write(row, MA_COL_0_IDX_EXONICFUNC, xls_record.exonic_func, st)
            ws.write(row, MA_COL_0_IDX_AACHANGE, xls_record.aa_change, st)
            ws.write(row, MA_COL_0_IDX_CONSERVED, xls_record.conserved, st)
            ws.write(row, MA_COL_0_IDX_SEGDUP, xls_record.seg_dup, st)
            ws.write(row, MA_COL_0_IDX_ESP6500_ALL, xls_record.esp6500_all, st)
            ws.write(row, MA_COL_0_IDX_1000G2012APR_ALL, xls_record.maf, st)
            ws.write(row, MA_COL_0_IDX_DBSNP137, xls_record.dbsnp137, st)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_AC, xls_record.stat_type1_ac, st)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_PC, xls_record.stat_type1_pc, st)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_PP, xls_record.stat_type1_pp, st)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_GC, xls_record.stat_type1_gc, st)
            ws.write(row, MA_COL_0_IDX_ALL_STAT_GP, xls_record.stat_type1_gp, st)
            ws.write(row, MA_COL_0_IDX_TYPE2_STAT_AC, xls_record.stat_type2_ac, st)
            ws.write(row, MA_COL_0_IDX_TYPE2_STAT_PC, xls_record.stat_type2_pc, st)
            ws.write(row, MA_COL_0_IDX_TYPE2_STAT_PP, xls_record.stat_type2_pp, st)
            ws.write(row, MA_COL_0_IDX_TYPE2_STAT_GC, xls_record.stat_type2_gc, st)
            ws.write(row, MA_COL_0_IDX_TYPE2_STAT_GP, xls_record.stat_type2_gp, st)
            ws.write(row, MA_COL_0_IDX_TYPE3_STAT_AC, xls_record.stat_type3_ac, st)
            ws.write(row, MA_COL_0_IDX_TYPE3_STAT_PC, xls_record.stat_type3_pc, st)
            ws.write(row, MA_COL_0_IDX_TYPE3_STAT_PP, xls_record.stat_type3_pp, st)
            ws.write(row, MA_COL_0_IDX_TYPE3_STAT_GC, xls_record.stat_type3_gc, st)
            ws.write(row, MA_COL_0_IDX_TYPE3_STAT_GP, xls_record.stat_type3_gp, st)
            ws.write(row, MA_COL_0_IDX_TYPE4_STAT_AC, xls_record.stat_type4_ac, st)
            ws.write(row, MA_COL_0_IDX_TYPE4_STAT_PC, xls_record.stat_type4_pc, st)
            ws.write(row, MA_COL_0_IDX_TYPE4_STAT_PP, xls_record.stat_type4_pp, st)
            ws.write(row, MA_COL_0_IDX_TYPE4_STAT_GC, xls_record.stat_type4_gc, st)
            ws.write(row, MA_COL_0_IDX_TYPE4_STAT_GP, xls_record.stat_type4_gp, st)
            ws.write(row, MA_COL_0_IDX_AVSIFT, xls_record.avsift, st)
            ws.write(row, MA_COL_0_IDX_LJB_PHYLOP, xls_record.ljb_phylop, st)
            ws.write(row, MA_COL_0_IDX_LJB_PHYLOP_PRED, xls_record.ljb_phylop_pred, st)
            ws.write(row, MA_COL_0_IDX_LJB_SIFT, xls_record.ljb_sift, st)
            ws.write(row, MA_COL_0_IDX_LJB_SIFT_PRED, xls_record.ljb_sift_pred, st)
            ws.write(row, MA_COL_0_IDX_LJB_POLYPHEN2, xls_record.ljb_polyphen2, st)
            ws.write(row, MA_COL_0_IDX_LJB_POLYPHEN2_PRED, xls_record.ljb_polyphen2_pred, st)
            ws.write(row, MA_COL_0_IDX_LJB_LRT, xls_record.ljb_lrt, st)
            ws.write(row, MA_COL_0_IDX_LJB_LRT_PRED, xls_record.ljb_lrt_pred, st)
            ws.write(row, MA_COL_0_IDX_LJB_MT, xls_record.ljb_mt, st)
            ws.write(row, MA_COL_0_IDX_LJB_MT_PRED, xls_record.ljb_mt_pred, st)
            ws.write(row, MA_COL_0_IDX_LJB_GERP, xls_record.ljb_gerp, st)
            ws.write(row, MA_COL_0_IDX_CHROM, xls_record.chrom, st)
            ws.write(row, MA_COL_0_IDX_START, int(xls_record.start_pos), st)
            ws.write(row, MA_COL_0_IDX_END, int(xls_record.end_pos), st)
            ws.write(row, MA_COL_0_IDX_REF, xls_record.ref, st)
            ws.write(row, MA_COL_0_IDX_OBS, xls_record.obs, st)
            ws.write(row, MA_COL_0_IDX_ZYGOSITY, xls_record.zygosity, st)
        ws.col(MA_COL_0_IDX_ALL_STAT_AC).width = 1900
        ws.col(MA_COL_0_IDX_ALL_STAT_PC).width = 1900
        ws.col(MA_COL_0_IDX_ALL_STAT_PP).width = 1900
        ws.col(MA_COL_0_IDX_ALL_STAT_GC).width = 1900
        ws.col(MA_COL_0_IDX_ALL_STAT_GP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE2_STAT_AC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE2_STAT_PC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE2_STAT_PP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE2_STAT_GC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE2_STAT_GP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE3_STAT_AC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE3_STAT_PC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE3_STAT_PP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE3_STAT_GC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE3_STAT_GP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE4_STAT_AC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE4_STAT_PC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE4_STAT_PP).width = 1900
        ws.col(MA_COL_0_IDX_TYPE4_STAT_GC).width = 1900
        ws.col(MA_COL_0_IDX_TYPE4_STAT_GP).width = 1900
        ws.set_panes_frozen(True)
        ws.set_horz_split_pos(3)
        ws.set_remove_splits(True)

    def __export_family_xls(self, family_code, directory):
        """ export mutations for one family to the given directory """

        self.info("exporting family: " + family_code)
        file_name = 'family' + family_code + '_' + self.__report_code + '.xls'
        output_file = os.path.join(directory, file_name)

        wb = xlwt.Workbook()

        yellow_st = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
        family = self.__families[family_code]
        for patient_code in family.patient_codes:
            self.__add_csv_sheet(wb,
                                 family_code,
                                 patient_code,
                                 [patient_code],
                                 yellow_st,
                                 )
        self.__add_csv_sheet(wb,
                             family_code,
                             'In common',
                             family.patient_codes,
                             yellow_st,
                             )
        wb.save(output_file)

    def export_family_xls(self, family_code, directory):
        """ export mutations for one family to the given directory """
        return self.__export_family_xls(family_code, directory)

    def __get_xls_records(self, patient_codes):
        """ prepare data for one data sheet """
        xls_records = []
        sa_key_fmt = "{vcf_mutation_key}|{ref}|{obs}"
        for vcf_mutation_key in self.__db_manager.vcf_db.common_mutations(patient_codes):
            vcf_mutation = self.__vcf_mutations[vcf_mutation_key]
            genotype_field = vcf_mutation.genotype_fields[patient_codes[0]]
            gt = genotype_field.raw_gt.split('/')
            annovar_mutations = genotype_field.annovar_mutations
            annovar_idx = 0
            sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
                                                ref=annovar_mutations[annovar_idx]['ref'],
                                                obs=annovar_mutations[annovar_idx]['alt'])
            if gt[0] != '0':
#                sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
#                                                    ref=annovar_mutations[annovar_idx]['ref'],
#                                                    obs=annovar_mutations[annovar_idx]['alt'])
                annovar_idx += 1
                if sa_mutation_key in self.__sa_mutations:
                    mutation = self.__sa_mutations[sa_mutation_key]
                    if mutation.func != "exonic":
                        continue
                    mutation.zygosity = genotype_field.zygosity
                    idx = int(gt[0])-1
                    mutation.stat_type1_ac = vcf_mutation.stats_type1_ac[idx]
                    mutation.stat_type1_pc = vcf_mutation.stats_type1_pc[idx]
                    mutation.stat_type1_pp = vcf_mutation.stats_type1_pp[idx]
                    mutation.stat_type1_gc = vcf_mutation.stats_type1_gc
                    mutation.stat_type1_gp = vcf_mutation.stats_type1_gp
                    mutation.stat_type2_ac = vcf_mutation.stats_type2_ac[idx]
                    mutation.stat_type2_pc = vcf_mutation.stats_type2_pc[idx]
                    mutation.stat_type2_pp = vcf_mutation.stats_type2_pp[idx]
                    mutation.stat_type2_gc = vcf_mutation.stats_type2_gc
                    mutation.stat_type2_gp = vcf_mutation.stats_type2_gp
                    mutation.stat_type3_ac = vcf_mutation.stats_type3_ac[idx]
                    mutation.stat_type3_pc = vcf_mutation.stats_type3_pc[idx]
                    mutation.stat_type3_pp = vcf_mutation.stats_type3_pp[idx]
                    mutation.stat_type3_gc = vcf_mutation.stats_type3_gc
                    mutation.stat_type3_gp = vcf_mutation.stats_type3_gp
                    mutation.stat_type4_ac = vcf_mutation.stats_type4_ac[idx]
                    mutation.stat_type4_pc = vcf_mutation.stats_type4_pc[idx]
                    mutation.stat_type4_pp = vcf_mutation.stats_type4_pp[idx]
                    mutation.stat_type4_gc = vcf_mutation.stats_type4_gc
                    mutation.stat_type4_gp = vcf_mutation.stats_type4_gp
                    xls_records.append(mutation)
                else:
                    self.warn('patient code: "' + str(patient_codes) + '"\tkey: "' + sa_mutation_key + '" not found')

            if (gt[1] != '0') and (gt[0] != gt[1]):
#                sa_mutation_key = sa_key_fmt.format(vcf_mutation_key=vcf_mutation_key,
#                                                    ref=annovar_mutations[annovar_idx]['ref'],
#                                                    obs=annovar_mutations[annovar_idx]['alt'])
                if sa_mutation_key in self.__sa_mutations:
                    mutation = self.__sa_mutations[sa_mutation_key]
                    if mutation.func != "exonic":
                        continue
                    mutation.zygosity = genotype_field.zygosity
                    idx = int(gt[1])-1
                    mutation.stat_type1_ac = vcf_mutation.stats_type1_ac[idx]
                    mutation.stat_type1_pc = vcf_mutation.stats_type1_pc[idx]
                    mutation.stat_type1_pp = vcf_mutation.stats_type1_pp[idx]
                    mutation.stat_type1_gc = vcf_mutation.stats_type1_gc
                    mutation.stat_type1_gp = vcf_mutation.stats_type1_gp
                    mutation.stat_type2_ac = vcf_mutation.stats_type2_ac[idx]
                    mutation.stat_type2_pc = vcf_mutation.stats_type2_pc[idx]
                    mutation.stat_type2_pp = vcf_mutation.stats_type2_pp[idx]
                    mutation.stat_type2_gc = vcf_mutation.stats_type2_gc
                    mutation.stat_type2_gp = vcf_mutation.stats_type2_gp
                    mutation.stat_type3_ac = vcf_mutation.stats_type3_ac[idx]
                    mutation.stat_type3_pc = vcf_mutation.stats_type3_pc[idx]
                    mutation.stat_type3_pp = vcf_mutation.stats_type3_pp[idx]
                    mutation.stat_type3_gc = vcf_mutation.stats_type3_gc
                    mutation.stat_type3_gp = vcf_mutation.stats_type3_gp
                    mutation.stat_type4_ac = vcf_mutation.stats_type4_ac[idx]
                    mutation.stat_type4_pc = vcf_mutation.stats_type4_pc[idx]
                    mutation.stat_type4_pp = vcf_mutation.stats_type4_pp[idx]
                    mutation.stat_type4_gc = vcf_mutation.stats_type4_gc
                    mutation.stat_type4_gp = vcf_mutation.stats_type4_gp
                    xls_records.append(mutation)
                else:
                    self.info('patient code: "' + str(patient_codes) + '"\tkey: "' + sa_mutation_key + '" not found')
        return sorted(xls_records, key=lambda record: record.maf, reverse=True)

    def get_xls_records(self, patient_codes):
        return self.__get_xls_records(patient_codes)

    def __annotate_patient_group(self):
        """ to identify patient group in patient record """
        vcf_patients = self.__vcf_patients
        families = self.__families
        for family_code in families:
            family = families[family_code]
            for patient_code in family.patient_codes:
                if family.type2 == TYPE2_RECTAL:
                    vcf_patients[patient_code].type2 = TYPE2_RECTAL
                else:
                    vcf_patients[patient_code].type2 = TYPE2_NON_RECTAL
                if family.type3 == TYPE3_COLON:
                    vcf_patients[patient_code].type3 = TYPE3_COLON
                else:
                    vcf_patients[patient_code].type3 = TYPE3_NON_COLON
                if family.type4 == TYPE4_CAFAM:
                    vcf_patients[patient_code].type4 = TYPE4_CAFAM
                else:
                    vcf_patients[patient_code].type4 = TYPE4_NON_CAFAM

    def __annotate_group_stat(self):
        """ calculate group stat for each mutation record """

        group_members_count = self.__group_members_count
        vcf_mutations = self.__vcf_mutations
        vcf_patients = self.__vcf_patients
        all_patient_codes = filter(lambda x: vcf_patients[x].type2 is not None, vcf_patients)
        rectal_patient_codes = filter(lambda x: vcf_patients[x].type2 == TYPE2_RECTAL, vcf_patients)
        colon_patient_codes = filter(lambda x: vcf_patients[x].type3 == TYPE3_COLON, vcf_patients)
        cafam_patient_codes = filter(lambda x: vcf_patients[x].type4 == TYPE4_CAFAM, vcf_patients)
        for mutation_key in vcf_mutations:
            mutation = vcf_mutations[mutation_key]
            #re-calculate stat for all members
            all_genotypes = map(lambda x: mutation.genotype_fields[x],
                                all_patient_codes)
            stat = mutation.calculate_stat(all_genotypes)
            mutation.stats_type1_ac = stat['allele_count']
            mutation.stats_type1_pc = stat['patient_count']
            mutation.stats_type1_pp = []
            for pc in stat['patient_count']:
                if stat['genotype_count'] == 0:
                    mutation.stats_type1_pp.append('-')
                else:
                    mutation.stats_type1_pp.append(float("{:.2f}".format(float(pc)/stat['genotype_count'])))
            mutation.stats_type1_gc = stat['genotype_count']
            mutation.stats_type1_gp = float("{:.2f}".format(float(stat['genotype_count'])/group_members_count[TYPE1_ALL]))
            #calculate stat for RECTAL group
            rectal_genotypes = map(lambda x: mutation.genotype_fields[x],
                                   rectal_patient_codes)
            stat = mutation.calculate_stat(rectal_genotypes)
            mutation.stats_type2_ac = stat['allele_count']
            mutation.stats_type2_pc = stat['patient_count']
            mutation.stats_type2_pp = []
            for pc in stat['patient_count']:
                if stat['genotype_count'] == 0:
                    mutation.stats_type2_pp.append('-')
                else:
                    mutation.stats_type2_pp.append(float("{:.2f}".format(float(pc)/stat['genotype_count'])))
            mutation.stats_type2_gc = stat['genotype_count']
            mutation.stats_type2_gp = float("{:.2f}".format(float(stat['genotype_count'])/group_members_count[TYPE2_RECTAL]))
            #calculate stat for COLON group
            colon_genotypes = map(lambda x: mutation.genotype_fields[x],
                                  colon_patient_codes)
            stat = mutation.calculate_stat(colon_genotypes)
            mutation.stats_type3_ac = stat['allele_count']
            mutation.stats_type3_pc = stat['patient_count']
            mutation.stats_type3_pp = []
            for pc in stat['patient_count']:
                if stat['genotype_count'] == 0:
                    mutation.stats_type3_pp.append('-')
                else:
                    mutation.stats_type3_pp.append(float("{:.2f}".format(float(pc)/stat['genotype_count'])))
            mutation.stats_type3_gc = stat['genotype_count']
            mutation.stats_type3_gp = float("{:.2f}".format(float(stat['genotype_count'])/group_members_count[TYPE3_COLON]))
            #calculate stat for CAFAM group
            cafam_genotypes = map(lambda x: mutation.genotype_fields[x],
                                  cafam_patient_codes)
            stat = mutation.calculate_stat(cafam_genotypes)
            mutation.stats_type4_ac = stat['allele_count']
            mutation.stats_type4_pc = stat['patient_count']
            mutation.stats_type4_pp = []
            for pc in stat['patient_count']:
                if stat['genotype_count'] == 0:
                    mutation.stats_type4_pp.append('-')
                else:
                    mutation.stats_type4_pp.append(float("{:.2f}".format(float(pc)/stat['genotype_count'])))
            mutation.stats_type4_gc = stat['genotype_count']
            mutation.stats_type4_gp = float("{:.2f}".format(float(stat['genotype_count'])/group_members_count[TYPE4_CAFAM]))

    @property
    def vcf_mutations(self):
        return self.__vcf_mutations

    @property
    def db_manager(self):
        return self.__db_manager

    @db_manager.setter
    def db_manager(self, value):
        db_man = value
        self.__db_manager = value
        self.info("connecting db manager")
        if not self.__db_manager.valid_patient_codes:
            self.throw("Invalid patient codes either in Vcf database or Family data. Please check")
        self.__group_members_count = db_man.family_db.group_members_count
        self.__sa_mutations = db_man.summarize_annovar_db.mutations
        self.__vcf_patients = db_man.vcf_db.patients
        self.__vcf_mutations = db_man.vcf_db.mutations
        self.__families = self.__db_manager.family_db.families
        self.info("annotating patient group")
        self.__annotate_patient_group()
        self.info("annotating group stat")
        self.__annotate_group_stat()
