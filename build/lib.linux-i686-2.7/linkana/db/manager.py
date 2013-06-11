import linkana.settings as lka_const
from linkana.template import LinkAnaBase



#from linkana.db.mutation import SNPRecord
class SNPRecord(object):
    """ to automatically parse SNP data"""

    def __init__(self, rec):
        self.__rec = rec

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'gene': self.gene,
                    'exonic function': self.exonic_func,
                    'maf': self.maf,
                    'marker': self.marker,
                    'chrom': self.chrom,
                    'start_pos': self.start_pos,
                    'end_pos': self.end_pos,
                    'ref': self.ref,
                    'alt': self.alt,
                    })

    @property
    def gene(self):
        return self.__rec[lka_const.SNP_0_IDX_GENE_NAME]

    @property
    def exonic_func(self):
        return self.__rec[lka_const.SNP_0_IDX_EXONIC_FUNC]

    @property
    def maf(self):
        return self.__rec[lka_const.SNP_0_IDX_MAF]

    @property
    def marker(self):
        return self.__rec[lka_const.SNP_0_IDX_MARKER]

    @property
    def chrom(self):
        return self.__rec[lka_const.SNP_0_IDX_CHROM]

    @property
    def start_pos(self):
        return self.__rec[lka_const.SNP_0_IDX_START_POS]

    @property
    def end_pos(self):
        return self.__rec[lka_const.SNP_0_IDX_END_POS]

    @property
    def ref(self):
        return self.__rec[lka_const.SNP_0_IDX_REF]

    @property
    def alt(self):
        return self.__rec[lka_const.SNP_0_IDX_ALT]


class SNPItem(object):

    def __init__(self, snp_record):
        self.info = snp_record
        self.count = 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'info': self.info,
                    'chrom': self.info.chrom,
                    'count': self.count,
                    'pkey': self.pkey,
                    })

    @property
    def pkey(self):
        pkey_fmt = "{chrom:0>2}|{pos:0>12}"
        return pkey_fmt.format(chrom=self.info.chrom,
                               pos=self.info.start_pos,
                               )


class SNPManager(dict, LinkAnaBase):

    def __init__(self, *args, **kwargs ):
#        myparam = kwargs.pop('myparam', '')
        dict.__init__(self, *args, **kwargs )
        LinkAnaBase.__init__(self)

    def add_snp(self, snp_record):
        snp_item = SNPItem(snp_record)
        if snp_item.pkey not in self.keys():
            self[snp_item.pkey] = snp_item
        else:
            self[snp_item.pkey].count += 1

    def get_items_by_gene(self, gene):
        for snp_key in self.keys():
            if self[snp_key].info.gene == gene:
                yield self[snp_key]


class MemberItem(object):

    def __init__(self, chrom, fam_code, member_code):
        self.chrom = chrom
        self.fam_code = fam_code
        self.member_code = member_code
        self.snps = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'chrom': self.chrom,
                    'family code': self.fam_code,
                    'member code': self.member_code,
                    'snps': self.snps,
                    'pkey': self.pkey,
                    })

    @property
    def pkey(self):
        pkey_fmt = "{chrom}|{fam_code}|{member_code}"
        return pkey_fmt.format(chrom=self.chrom,
                               fam_code=self.fam_code,
                               member_code=self.member_code,
                               )

    def add_snp_key(self, snp_key):
        self.snps.append(snp_key)


class MemberManager(dict, LinkAnaBase):

    def __init__(self, *args, **kwargs ):
        dict.__init__(self, *args, **kwargs )
        LinkAnaBase.__init__(self)

    def add_member(self, member_item):
        self[member_item.pkey] = member_item


class FamilyItem(object):

    def __init__(self, chrom, fam_code):
        self.chrom = chrom
        self.fam_code = fam_code
        self.member_keys = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str({'chrom': self.chrom,
                    'fam_code': self.fam_code,
                    'member_codes': self.member_codes,
                    'pkey': self.pkey,
                    })

    @property
    def pkey(self):
        pkey_fmt = "{chrom}|{fam_code}"
        return pkey_fmt.format(chrom=self.chrom,
                               fam_code=self.fam_code,
                               )

#    def member_key(self, member_code):
#        return"{family_key}|{member_code}".format(family_key=self.pkey,
#                                                  member_code=member_code)
#
    def add_member_key(self, member_key):
        self.member_keys.append(member_key)


class DBManager(LinkAnaBase):

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.snp_mgr = SNPManager()

    def add_mutation(self, snp_record):
        self.snp_mgr.add_snp(snp_record)

#    def get_snps_by_gene(self, gene):
#        return self.snp_mgr.get_snps_by_gene(gene)
#    def __read_csv(self, csv_file):
#        print csv_file
#        csv_records = csv.reader(open(csv_file, 'rb'), delimiter='\t')
#        for csv_record in csv_records:
#            if (isFloat(csv_record[col_maf]) and (float(csv_record[col_maf])<=0.1)) or (csv_record[col_maf]=='') :
#               if (csv_record[col_exonic_func] != 'synonymous SNV'):
#                   self.__add_mutation(csv_record)
#
#    def load(self, data_dir):
#        os.chdir(data_dir)
#        for csv_file in glob.glob("*.csv"):
#            self.__read_csv(csv_file)


#import sys
#import csv
#import xlwt
#import os
#import glob
#
#data_dir    = sys.argv[1]
#output_file = sys.argv[2]
#
#col_gene_name   = 1
#col_exonic_func = 2
#col_maf         = 7
#col_marker      = 8
#col_chrom       = 21
#col_start_pos   = 22
#col_end_pos     = 23
#col_ref         = 24
#col_alt         = 25
#
#def isFloat(string):
#    try:
#        float(string)
#        return True
#    except ValueError:
#        return False
#
#class SuspectMutations(object):
#
#    def __init__(self):
#        pass
#
#    def __add_mutation(self, mutation_record):
#        snp = SNP()
#        snp.gene_name = mutation_record[col_gene_name]
#        snp.maf       = mutation_record[col_maf]
#        snp.marker    = mutation_record[col_marker]
#        snp.chrom     = mutation_record[col_chrom]
#        snp.start_pos = mutation_record[col_start_pos]
#        snp.end_pos   = mutation_record[col_end_pos]
#        snp.ref       = mutation_record[col_ref]
#        snp.alt       = mutation_record[col_alt]
#        print snp
#
#    def __read_csv(self, csv_file):
#        print csv_file
#        csv_records = csv.reader(open(csv_file, 'rb'), delimiter='\t')
#        for csv_record in csv_records:
#            if (isFloat(csv_record[col_maf]) and (float(csv_record[col_maf])<=0.1)) or (csv_record[col_maf]=='') :
#               if (csv_record[col_exonic_func] != 'synonymous SNV'):
#                   self.__add_mutation(csv_record)
#
#    def load(self, data_dir):
#        os.chdir(data_dir)
#        for csv_file in glob.glob("*.csv"):
#            self.__read_csv(csv_file)
#
#def sample_merge(wb):
#    ws = wb.add_sheet('sample_merge')
#    fnt = xlwt.Font()
#    fnt.name = 'Arial'
#    fnt.colour_index = 4
#    fnt.bold = True
#
#    borders = xlwt.Borders()
#    borders.left = 6
#    borders.right = 6
#    borders.top = 6
#    borders.bottom = 6
#
#    style = xlwt.XFStyle()
#    style.font = fnt
#    style.borders = borders
#
#    ws.write_merge(3, 3, 1, 5, 'test1', style)
#    ws.write_merge(4, 10, 1, 5, 'test2', style)
#    ws.col(1).width = 0x0d00
#    return ws
#
#def sample_alignment(wb):
#    worksheet = wb.add_sheet('alignment')
#    alignment = xlwt.Alignment() # Create Alignment
#    alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
#    alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
#    style = xlwt.XFStyle() # Create Style
#    style.alignment = alignment # Add Alignment to Style
#    worksheet.write(0, 0, 'Cell Contents', style)
#    return worksheet
#
#def sample_borders(wb):
#    worksheet = wb.add_sheet('borders')
#    borders = xlwt.Borders() # Create Borders
#    borders.left = xlwt.Borders.DASHED # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
#    borders.right = xlwt.Borders.DASHED
#    borders.top = xlwt.Borders.DASHED
#    borders.bottom = xlwt.Borders.DASHED
#    borders.left_colour = 0x40
#    borders.right_colour = 0x40
#    borders.top_colour = 0x40
#    borders.bottom_colour = 0x40
#    style = xlwt.XFStyle() # Create Style
#    style.borders = borders # Add Borders to Style
#    worksheet.write(0, 0, 'Cell Contents', style)
#    return worksheet
#
#def create_header(wb, sty):
#    ws = wb.add_sheet('summarize')
#    ws.write_merge(0, 0, 1, 2, 'Families', sty)
#    ws.write_merge(1, 2, 1, 1, 'Code', sty)
#    ws.write_merge(1, 2, 2, 2, 'Members', sty)
#    return ws
#
#def generate_header_style():
#    borders = xlwt.Borders()
#    borders.left = xlwt.Borders.DOUBLE
#    borders.right = xlwt.Borders.DOUBLE
#    borders.top = xlwt.Borders.DOUBLE
#    borders.bottom = xlwt.Borders.DOUBLE
#
#    alignment = xlwt.Alignment()
#    alignment.horz = xlwt.Alignment.HORZ_CENTER
#    alignment.vert = xlwt.Alignment.VERT_CENTER
#
#    header_style = xlwt.XFStyle()
#    header_style.borders = borders
#    header_style.alignment = alignment
#    return header_style
#
#suspect_mutations = SuspectMutations()
#suspect_mutations.load(data_dir)
#
#header_style = generate_header_style()
#
#wb = xlwt.Workbook()
#create_header(wb, header_style)
#sample_borders(wb)
#sample_merge(wb)
#sample_alignment(wb)
#wb.save(output_file)


