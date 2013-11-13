#!/bin/bash

#---------- arguments --------------
chr=$1
begin_pos=$2
end_pos=$3
tabix_file=$4
oaf_file=$5
working_dir=$6
out_prefix=$7
out_file=$8

#---------- arguments --------------

echo "## building summarize annovar database" 1>&2
echo "## parameters" 1>&2
echo "## chromosome:  $chr" 1>&2
echo "## begin pos:   $begin_pos" 1>&2
echo "## end pos:     $end_pos" 1>&2
echo "## tabix_file:  $tabix_file" 1>&2
echo "## oaf_file:    $oaf_file" 1>&2
echo "## working_dir: $working_dir" 1>&2
echo "## out_prefix:  $out_prefix" 1>&2
echo "## out_file:    $out_file" 1>&2


#---------- vcf2avdb --------------
tmp_avdb=$working_dir/$out_prefix"_tmp_avdb"
avdb_out=$working_dir/$out_prefix".avdb"
avdb_key=$working_dir/$out_prefix".key.avdb"
avdb_oaf=$working_dir/$out_prefix".oaf.avdb"


if [ -z $chr ]
then
    cut_region="zcat $tabix_file | grep -v \"^#\""
else
    cut_region="tabix $tabix_file $chr:$begin_pos-$end_pos"
fi
create_tmp_avdb="$cut_region | cut -f1-10 | awk -F'\t' '{printf \"%s\t%s\t%s\t%s\t%s\t%s|%s\t%s\t%s\t%s\t%s\n\", \$1, \$2, \$3, \$4, \$5, \$6, \$2, \$7, \$8, \$9, \$10}' > $tmp_avdb"
echo "## execute $create_tmp_avdb" 1>&2
eval $create_tmp_avdb

convert2annovar="$CONVERT2ANNOVAR -format vcf4old $tmp_avdb --allallele > $avdb_out"
echo "## execute $convert2annovar" 1>&2
eval $convert2annovar
#---------- vcf2avdb --------------


#---------- add oaf to avdb --------------
add_key_to_avdb="awk -F'|' '{ printf \"%s\t%s\n\", \$1, \$2 }' $avdb_out | awk -F'\t' '{ printf \"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s|%012d\n\", \$1, \$2, \$3, \$4, \$5, \$6, \$7, \$9, \$10, \$11, \$1, \$8 }' > $avdb_key"
echo "## execute $add_key_to_avdb" 1>&2
eval $add_key_to_avdb


join_cmd="join -t $'\t' -a 1 -a 2 -1 11 -2 1 -e NULL -o 1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,2.2 <( grep -v \"^X\" $avdb_key | grep -v \"^Y\" | grep -v \"^M\" ) <(awk -F'\t' '{ printf \"%s|%012d\t%s\n\", \$1, \$2, \$6}' $oaf_file | grep -v \"^X\" | grep -v \"^Y\" | grep -v \"^M\") > $avdb_oaf"
echo "## execute $join_cmd" 1>&2
eval $join_cmd
join_cmd="join -t $'\t' -a 1 -a 2 -1 11 -2 1 -e NULL -o 1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,2.2 <( awk -F'\t' '{ if (\$1 == \"X\" || \$1 == \"Y\" || \$1 == \"MT\") print \$0 }' $avdb_key | sort -k11) <(awk -F'\t' '{ printf \"%s|%012d\t%s\n\", \$1, \$2, \$6}' $oaf_file | awk -F'\t' '{ if (\$1 ~ /X/ || \$1 ~ /Y/ || \$1 ~ /MT/) print \$0 }' | sort -k1) >> $avdb_oaf"
echo "## execute $join_cmd" 1>&2
eval $join_cmd
#---------- add oaf to avdb --------------


#---------- summarize --------------
summarize_out=$working_dir/$out_prefix
summarize_annovar="$SUMMARIZE_ANNOVAR -out $summarize_out -buildver hg19 -verdbsnp 137 -ver1000g 1000g2012apr -veresp 6500 -remove -alltranscript $avdb_oaf $ANNOVAR_HUMAN_DB_DIR"
echo "## execute $summarize_annovar" 1>&2
eval $summarize_annovar
#---------- summarize --------------


#---------- comma2tab --------------
csv_file=$summarize_out".genome_summary.csv"
comma2tab="perl -pe 'while (s/(,\"[^\"]+),/\1<COMMA>/g) {1}; s/\"//g; s/,/\t/g; s/<COMMA>/,/g' < $csv_file > $out_file"
echo "## execute $comma2tab" 1>&2
eval $comma2tab
#---------- comma2tab --------------
