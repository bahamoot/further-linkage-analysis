import sys
import csv
import xlwt

member1_csv  = sys.argv[1]
member1_code = sys.argv[2]

if len(sys.argv) == 4:
    output_file  = sys.argv[3]
else:
    member2_csv  = sys.argv[3]
    member2_code = sys.argv[4]
    if len(sys.argv) == 7:
        incommon_csv = sys.argv[5]
        output_file  = sys.argv[6]
    else:
        member3_csv  = sys.argv[5]
        member3_code = sys.argv[6]
        incommon_csv = sys.argv[7]
        output_file  = sys.argv[8]

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def explain_annotation(csv_record):
    col_ljb_phylop_pred         = 11
    col_ljb_sift_pred           = 13
    col_ljb_polyphen2_pred      = 15
    col_ljb_lrt_pred            = 17
    col_ljb_mutationtaster_pred = 19

    phylop_explanation         = {'C': 'conserved', 'N': 'not conserved'}
    sift_explanation           = {'T': 'tolerated', 'D': 'deleterious'}
    polyphen2_explanation      = {'D': 'probably damaging', 'P': 'possibly damaging', 'B': 'benign'}
    lrt_explanation            = {'D': 'tolerated', 'N': 'neutral'}
    mutationtaster_explanation = {'A': 'disease causing automatic', 'D': 'disease causing', 'N': 'polymorphism', 'P': 'polymorphism automatic'}

    if csv_record[col_ljb_phylop_pred] in phylop_explanation:
        csv_record[col_ljb_phylop_pred]         = phylop_explanation[csv_record[col_ljb_phylop_pred]]
    if csv_record[col_ljb_sift_pred] in sift_explanation:
        csv_record[col_ljb_sift_pred]           = sift_explanation[csv_record[col_ljb_sift_pred]]
    if csv_record[col_ljb_polyphen2_pred] in polyphen2_explanation:
        csv_record[col_ljb_polyphen2_pred]      = polyphen2_explanation[csv_record[col_ljb_polyphen2_pred]]
    if csv_record[col_ljb_lrt_pred] in lrt_explanation:
        csv_record[col_ljb_lrt_pred]            = lrt_explanation[csv_record[col_ljb_lrt_pred]]
    if csv_record[col_ljb_mutationtaster_pred] in mutationtaster_explanation:
        csv_record[col_ljb_mutationtaster_pred] = mutationtaster_explanation[csv_record[col_ljb_mutationtaster_pred]]
    return csv_record

def split_last_extra_info(csv_record, sheet_name):
#    tmp_len   = len(csv_record)
#    if sheet_name != "In common":
#        if csv_record[tmp_len-1] == 'Otherinfo':
#            csv_record.append('QUAL')
#            csv_record.append('FILTER')
#        else:
#            tmp_split = csv_record[tmp_len-1].split('|')
#            csv_record[tmp_len-1] = tmp_split[0]
#            csv_record.append(tmp_split[1])
#            csv_record.append(tmp_split[2])
#    else:
#        csv_record[tmp_len-3] = csv_record[tmp_len-3].split('|')[0]
#        csv_record[tmp_len-2] = csv_record[tmp_len-2].split('|')[0]
#        csv_record[tmp_len-1] = csv_record[tmp_len-1].split('|')[0]
    return csv_record


def add_csv_sheet(wb, sheet_name, csv_file, st):
    ws = wb.add_sheet(sheet_name)
    with open(csv_file, 'rb') as csvfile:
        csv_records = list(csv.reader(csvfile, delimiter='\t'))
        for row in xrange(len(csv_records)):
            csv_record = csv_records[row]
            csv_record = split_last_extra_info(explain_annotation(csv_record), sheet_name)
            for col in xrange(len(csv_record)):
                if (isFloat(csv_record[7]) and (float(csv_record[7])<=0.1)) or (csv_record[7]=='') :
                    if (csv_record[2] != 'synonymous SNV'):
                        ws.write(row, col, csv_record[col], st)
                    else:
                        ws.write(row, col, csv_record[col])
                else:
                    ws.write(row, col, csv_record[col])
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)
    ws.set_remove_splits(True)

wb = xlwt.Workbook()
yellow_st = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')

add_csv_sheet(wb, member1_code, member1_csv, yellow_st)
if len(sys.argv) > 4:
    add_csv_sheet(wb, member2_code, member2_csv, yellow_st)
    if len(sys.argv) == 9:
        add_csv_sheet(wb, member3_code, member3_csv, yellow_st)
    add_csv_sheet(wb, "In common", incommon_csv, yellow_st)

wb.save(output_file)

