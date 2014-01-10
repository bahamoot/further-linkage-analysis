#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_gen_xls=$script_dir/script_gen_xls_for_sanna_n_vinay.sh
working_dir=$script_dir/tmp

#---------- recessive model colon cancer --------------
chrom="6"
min_pos="37763732" #rs1738240 = 38763732
max_pos="45479949" #rs941983  = 44479949
sub_project_name="colon_recessive_chr$chrom"

$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "110" "1526-02D" "Co1301"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "301" "Co837" "Co840" "Co1053"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "650" "398-05o" "729-05o"

#---------- recessive model rectal cancer --------------
chrom="18"
min_pos="9928706"  #rs906283  = 10928706
max_pos="21607819" #rs1010800 = 20607819
sub_project_name="rectal_recessive_chr$chrom"

$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "8" "Co35" "Co37"
#$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "258" "" ""
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "918" "134-06" "354-06"
$script_gen_xls $sub_project_name $chrom $min_pos $max_pos "1213" "Co1666"

