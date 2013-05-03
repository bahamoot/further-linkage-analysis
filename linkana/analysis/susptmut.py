


import sys
import csv
import xlwt
import os
import glob

data_dir    = sys.argv[1]
output_file = sys.argv[2]

col_gene_name   = 1
col_exonic_func = 2
col_maf         = 7
col_marker      = 8
col_chrom       = 21
col_start_pos   = 22
col_end_pos     = 23
col_ref         = 24
col_alt         = 25

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

class SNP(object):

    def __init__(self):
        self.gene_name = None
        self.maf       = None
        self.marker    = None
        self.chrom     = None
        self.start_pos = None
        self.end_pos   = None
        self.ref       = None
        self.alt       = None

    def __repr__(self):
        return str({'gene': self.gene_name,
                    'maf': self.maf,
                    'marker': self.marker,
                    'chrom': self.chrom,
                    'start_pos': self.start_pos,
                    'end_pos': self.end_pos,
                    'ref': self.ref,
                    'alt': self.alt,
                    })

class SuspectMutations(object):

    def __init__(self):
        pass

    def __add_mutation(self, mutation_record):
        snp = SNP()
        snp.gene_name = mutation_record[col_gene_name]
        snp.maf       = mutation_record[col_maf]
        snp.marker    = mutation_record[col_marker]
        snp.chrom     = mutation_record[col_chrom]
        snp.start_pos = mutation_record[col_start_pos]
        snp.end_pos   = mutation_record[col_end_pos]
        snp.ref       = mutation_record[col_ref]
        snp.alt       = mutation_record[col_alt]
        print snp

    def __read_csv(self, csv_file):
        print csv_file
        csv_records = csv.reader(open(csv_file, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            if (isFloat(csv_record[col_maf]) and (float(csv_record[col_maf])<=0.1)) or (csv_record[col_maf]=='') :
               if (csv_record[col_exonic_func] != 'synonymous SNV'):
                   self.__add_mutation(csv_record)

    def load(self, data_dir):
        os.chdir(data_dir)
        for csv_file in glob.glob("*.csv"):
            self.__read_csv(csv_file)

def sample_merge(wb):
    ws = wb.add_sheet('sample_merge')
    fnt = xlwt.Font()
    fnt.name = 'Arial'
    fnt.colour_index = 4
    fnt.bold = True

    borders = xlwt.Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    style = xlwt.XFStyle()
    style.font = fnt
    style.borders = borders

    ws.write_merge(3, 3, 1, 5, 'test1', style)
    ws.write_merge(4, 10, 1, 5, 'test2', style)
    ws.col(1).width = 0x0d00
    return ws

def sample_alignment(wb):
    worksheet = wb.add_sheet('alignment')
    alignment = xlwt.Alignment() # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    worksheet.write(0, 0, 'Cell Contents', style)
    return worksheet

def sample_borders(wb):
    worksheet = wb.add_sheet('borders')
    borders = xlwt.Borders() # Create Borders
    borders.left = xlwt.Borders.DASHED # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    borders.right = xlwt.Borders.DASHED
    borders.top = xlwt.Borders.DASHED
    borders.bottom = xlwt.Borders.DASHED
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40
    style = xlwt.XFStyle() # Create Style
    style.borders = borders # Add Borders to Style
    worksheet.write(0, 0, 'Cell Contents', style)
    return worksheet

def create_header(wb, sty):
    ws = wb.add_sheet('summarize')
    ws.write_merge(0, 0, 1, 2, 'Families', sty)
    ws.write_merge(1, 2, 1, 1, 'Code', sty)
    ws.write_merge(1, 2, 2, 2, 'Members', sty)
    return ws

def generate_header_style():
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.DOUBLE
    borders.right = xlwt.Borders.DOUBLE
    borders.top = xlwt.Borders.DOUBLE
    borders.bottom = xlwt.Borders.DOUBLE

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    header_style = xlwt.XFStyle()
    header_style.borders = borders
    header_style.alignment = alignment
    return header_style

suspect_mutations = SuspectMutations()
suspect_mutations.load(data_dir)

header_style = generate_header_style()

wb = xlwt.Workbook()
create_header(wb, header_style)
sample_borders(wb)
sample_merge(wb)
sample_alignment(wb)
wb.save(output_file)


#member1_csv  = sys.argv[1]
#member1_code = sys.argv[2]
#
#if len(sys.argv) == 4:
#    output_file  = sys.argv[3]
#else:
#    member2_csv  = sys.argv[3]
#    member2_code = sys.argv[4]
#    if len(sys.argv) == 7:
#        incommon_csv = sys.argv[5]
#        output_file  = sys.argv[6]
#    else:
#        member3_csv  = sys.argv[5]
#        member3_code = sys.argv[6]
#        incommon_csv = sys.argv[7]
#        output_file  = sys.argv[8]
#
#def isFloat(string):
#    try:
#        float(string)
#        return True
#    except ValueError:
#        return False
#
#def explain_annotation(csv_record):
#    col_ljb_phylop_pred         = 11
#    col_ljb_sift_pred           = 13
#    col_ljb_polyphen2_pred      = 15
#    col_ljb_lrt_pred            = 17
#    col_ljb_mutationtaster_pred = 19
#
#    phylop_explanation         = {'C': 'conserved', 'N': 'not conserved'}
#    sift_explanation           = {'T': 'tolerated', 'D': 'deleterious'}
#    polyphen2_explanation      = {'D': 'probably damaging', 'P': 'possibly damaging', 'B': 'benign'}
#    lrt_explanation            = {'D': 'tolerated', 'N': 'neutral'}
#    mutationtaster_explanation = {'A': 'disease causing automatic', 'D': 'disease causing', 'N': 'polymorphism', 'P': 'polymorphism automatic'}
#
#    if csv_record[col_ljb_phylop_pred] in phylop_explanation:
#        csv_record[col_ljb_phylop_pred]         = phylop_explanation[csv_record[col_ljb_phylop_pred]]
#    if csv_record[col_ljb_sift_pred] in sift_explanation:
#        csv_record[col_ljb_sift_pred]           = sift_explanation[csv_record[col_ljb_sift_pred]]
#    if csv_record[col_ljb_polyphen2_pred] in polyphen2_explanation:
#        csv_record[col_ljb_polyphen2_pred]      = polyphen2_explanation[csv_record[col_ljb_polyphen2_pred]]
#    if csv_record[col_ljb_lrt_pred] in lrt_explanation:
#        csv_record[col_ljb_lrt_pred]            = lrt_explanation[csv_record[col_ljb_lrt_pred]]
#    if csv_record[col_ljb_mutationtaster_pred] in mutationtaster_explanation:
#        csv_record[col_ljb_mutationtaster_pred] = mutationtaster_explanation[csv_record[col_ljb_mutationtaster_pred]]
#    return csv_record
#
#def add_csv_sheet(wb, sheet_name, csv_file, st):
#    ws = wb.add_sheet(sheet_name)
#    with open(csv_file, 'rb') as csvfile:
#        csv_records = list(csv.reader(csvfile, delimiter='\t'))
#        for row in xrange(len(csv_records)):
#            csv_record = csv_records[row]
#            csv_record = explain_annotation(csv_record)
#            for col in xrange(len(csv_record)):
#                if (isFloat(csv_record[7]) and (float(csv_record[7])<=0.1)) or (csv_record[7]=='') :
#                    if (csv_record[2] != 'synonymous SNV'):
#                        ws.write(row, col, csv_record[col], st)
#                    else:
#                        ws.write(row, col, csv_record[col])
#                else:
#                    ws.write(row, col, csv_record[col])
#    ws.set_panes_frozen(True)
#    ws.set_horz_split_pos(1)
#    ws.set_remove_splits(True)
#
#wb = xlwt.Workbook()
#yellow_st = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
#
#add_csv_sheet(wb, member1_code, member1_csv, yellow_st)
#if len(sys.argv) > 4:
#    add_csv_sheet(wb, member2_code, member2_csv, yellow_st)
#    if len(sys.argv) == 9:
#        add_csv_sheet(wb, member3_code, member3_csv, yellow_st)
#    add_csv_sheet(wb, "In common", incommon_csv, yellow_st)
#
#wb.save(output_file)

