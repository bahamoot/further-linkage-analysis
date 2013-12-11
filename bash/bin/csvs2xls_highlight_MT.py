import sys
import csv
import xlwt

output_file = sys.argv[1]

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

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def add_csv_sheet(wb, sheet_name, csv_file, st):
    ws = wb.add_sheet(sheet_name)
    with open(csv_file, 'rb') as csvfile:
        csv_records = list(csv.reader(csvfile, delimiter='\t'))
        csv_row = 0
        for xls_row in xrange(len(csv_records)):
            csv_record = csv_records[xls_row]
            for col in xrange(len(csv_record)):
                if ((csv_record[col] == '1/1') or (csv_record[col] == '0/1')):
#                    ws.write(csv_row, col, csv_record[col])
                    ws.write(csv_row, col, csv_record[col], st["ice blue"])
                else:
                    ws.write(csv_row, col, csv_record[col])
            csv_row += 1
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)
    ws.set_remove_splits(True)


wb = xlwt.Workbook()
st = {}
st["ocean blue"] = xlwt.easyxf('pattern: pattern solid, fore_colour ocean_blue;')
st["light blue"] = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;')
st["ice blue"] = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')

for i in xrange(2, len(sys.argv), 2):
    sheet_name = sys.argv[i+1]
    input_csv  = sys.argv[i]
    add_csv_sheet(wb, sheet_name, input_csv, st)


wb.save(output_file)

