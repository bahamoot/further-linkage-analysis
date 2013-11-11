#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_sa=$script_dir/script_build_sa.sh
working_dir=$script_dir/tmp

#---------- arguments --------------
out_prefix=$6

out_file=$working_dir/$out_prefix".tab.csv"
#---------- arguments --------------

#---------- vcf2avdb --------------
tmp_avdb=$working_dir/$out_prefix"_tmp_avdb"
avdb_out=$working_dir/$out_prefix".avdb"

$script_build_sa "" "" "" $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ $working_dir "scilife" $CMM_SCILIFE_ILLUMINA_SA_DB

#if [ -z $chr ]
#then
#    cut_region="zcat $tabix_file | grep -v \"^#\""
#else
#    cut_region="tabix $tabix_file $chr:$begin_pos-$end_pos"
#fi
#create_tmp_avdb="$cut_region | cut -f1-10 | awk -F'\t' '{printf \"%s\t%s\t%s\t%s\t%s\t%s|%s\t%s\t%s\t%s\t%s\n\", \$1, \$2, \$3, \$4, \$5, \$6, \$2, \$7, \$8, \$9, \$10}' > $tmp_avdb"
#echo "execute $create_tmp_avdb" 1>&2
#eval $create_tmp_avdb
#
#$convert2annovar_script -format vcf4old $tmp_avdb --allallele > $avdb_out
##---------- vcf2avdb --------------
#
##---------- summarize --------------
#summarize_annovar_script=$annovar_dir/summarize_annovar.pl
#human_db_dir=$annovar_dir/humandb/
#summarize_out=$working_dir/$out_prefix
#
#$summarize_annovar_script -out $summarize_out -buildver hg19 -verdbsnp 137 -ver1000g 1000g2012apr -veresp 6500 -remove -alltranscript $avdb_out $human_db_dir
##---------- summarize --------------
#
##---------- comma2tab --------------
#csv_file=$summarize_out".genome_summary.csv"
#perl -pe 'while (s/(,"[^"]+),/\1<COMMA>/g) {1}; s/"//g; s/,/\t/g; s/<COMMA>/,/g' < $csv_file > $out_file
##---------- comma2tab --------------


