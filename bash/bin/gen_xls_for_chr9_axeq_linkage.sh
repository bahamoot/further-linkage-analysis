#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_gen_xls=$script_dir/script_gen_xls_for_chr9_axeq_linkage.sh
working_dir=$script_dir/tmp

#---------- recessive model colon cancer --------------
chrom="9"
min_pos="98478118"
max_pos="98504905"
sub_project_name="p05"

$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "161" "Co809"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "275" "Co618"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "869" "Co1685"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "1025" "Co1529"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "1085" "Co1518"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "1252" "Co1719"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "208" "Co1094"
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "301" "Co837" "Co840" "Co1053"
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "650" "398-05o" "729-05o"

##---------- recessive model rectal cancer --------------
#chrom="18"
#min_pos="9928706"  #rs906283  = 10928706
#max_pos="21607819" #rs1010800 = 20607819
#sub_project_name="rectal_recessive_chr$chrom"
#
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "8" "Co35" "Co37"
##$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "258" "" ""
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "918" "134-06" "354-06"
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "1213" "Co1666"

