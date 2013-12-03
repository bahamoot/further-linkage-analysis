#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls=$script_dir/csvs2xls.py
sort_n_awk_csv=$script_dir/sort_n_awk_csv.sh

project_name="fam242_region"
patient_code[1]=Co441
patient_code[2]=Co771
patient_code[3]=Co666

working_dir=$script_dir/tmp
sa_db_file=$CMM_SCILIFE_ILLUMINA_MANS_SA_DB
vcf_gz_file=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ
vcf_header_file=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_HEADER
#tmp_sa_filtered=$working_dir/tmp_sa_filtered_for_"$project_name"
#tmp_common_mutations_csv=$working_dir/"$project_name"_common_mutations_tmp.tab.csv
#tmp_individual_mutations_csv1=$working_dir/"$project_name"_"$patient_code1"_tmp.tab.csv
#tmp_individual_mutations_csv2=$working_dir/"$project_name"_"$patient_code2"_tmp.tab.csv
#tmp_individual_mutations_csv3=$working_dir/"$project_name"_"$patient_code3"_tmp.tab.csv

out_dir=$script_dir/../out/"$project_name"
#out_common_mutations_csv=$out_dir/"$project_name"_common_mutations.tab.csv
#out_individual_mutations_csv1=$out_dir/"$project_name"_"$patient_code1".tab.csv
#out_individual_mutations_csv2=$out_dir/"$project_name"_"$patient_code2".tab.csv
#out_individual_mutations_csv3=$out_dir/"$project_name"_"$patient_code3".tab.csv
out_file=$out_dir/"$project_name"_analyze.csv

echo "## analyze result from family 242 region" 1>&2
echo "## parameters" 1>&2
echo "## summarize_annovar_file: $sa_db_file" 1>&2
echo "## vcf gz file:            $vcf_gz_file" 1>&2
echo "## vcf header file:        $vcf_header_file" 1>&2
echo "## working dir:            $working_dir" 1>&2
echo "## out file:               $out_file" 1>&2

#---------- get vcf columns from patient codes --------------
function get_vcf_col {
    grep "^#C" $1 | grep -i $2 | awk -va="$2" 'BEGIN{}
    END{}
    {
        for(i=1;i<=NF;i++){
            IGNORECASE = 1
            if ( tolower($i) == tolower(a))
                {print i }
        }
    }'
}

#---------- get vcf columns from patient codes --------------

echo "## family & members" 1>&2
echo "## family code:            $project_name" 1>&2

for (( i=1; i<=$((${#patient_code[@]})); i++ ))
do
    patient_col[$i]=`get_vcf_col $vcf_header_file ${patient_code[$i]}`
    echo "## patient code$i:          ${patient_code[$i]}" 1>&2
    echo "## column:                 ${patient_col[$i]}" 1>&2
done
#echo "## chrom:                  $chrom" 1>&2
#echo "## min position:           $min_pos" 1>&2
#echo "## max position:           $max_pos" 1>&2


#---------- debug mutations --------------
chrom=3
gene_name[1]="DNAJC13"
gene_name[2]="DZIP1L"
gene_name[3]="CLSTN2"
gene_name[4]="PCOLCE2"
gene_name[5]="IGSF10"
gene_name[6]="SUCNR1"
gene_name[7]="MUC13"
gene_name[8]="ALG1L2"
gene_name[9]="YEATS2"
gene_name[10]="MAGEF1"
gene_pos[1]="132226100"
gene_pos[2]="137786409"
gene_pos[3]="140178381"
gene_pos[4]="142542415"
gene_pos[5]="151171329"
gene_pos[6]="151598890"
gene_pos[7]="124646705"
gene_pos[8]="129814934"
gene_pos[9]="184429133"
gene_pos[10]="183493743"

printf_str=""
patient_param=""
for (( i=1; i<=$((${#patient_code[@]})); i++ ))
do
    printf_str+="\t%s"
    patient_param+=", \$${patient_col[$i]}"
done

n_col=`awk -F '\t' '{print NF}' $vcf_header_file`

parsed_header="gene\tchrom\tposition"
for (( j=1; j<=$n_col; j++ ))
do
    if [ $j -ne 1 ] && [ $j -ne 2 ] && [ $j -ne 3 ] && [ $j -ne 6 ] && [ $j -ne 7 ] && [ $j -ne 8 ] && [ $j -ne 9 ]; then
        echo_cmd="cut -f$j $vcf_header_file"
        gt=`eval $echo_cmd`
        parsed_header+="\t$gt"
    fi
done
echo -e "$parsed_header" > $out_file

for (( i=1; i<=$((${#gene_pos[@]})); i++ ))
do
    dbg_cmd="tabix $vcf_gz_file $chrom":"${gene_pos[$i]}"-"${gene_pos[$i]}"
#    dbg_cmd="tabix $vcf_gz_file $chrom":"${gene_pos[$i]}"-"${gene_pos[$i]} | awk -F'\t' '{ printf \"${gene_name[$i]}\t%s\t%s$printf_str\n\", \$1, \$2$patient_param }'"
#    echo "executing $dbg_cmd" 1>&2
#    eval $dbg_cmd
    rec=`eval $dbg_cmd`
    parsed_rec="${gene_name[$i]}"
#    echo_cmd="echo \"$rec\" | cut -f1,2,4,5 -d\" \""
#    parsed_rec+=`eval $echo_cmd`
    for (( j=1; j<=$n_col; j++ ))
    do
        if [ $j -ne 3 ] && [ $j -ne 6 ] && [ $j -ne 7 ] && [ $j -ne 8 ] && [ $j -ne 9 ]; then
            echo_cmd="echo \"$rec\" | cut -f$j -d\" \" | cut -f1 -d\":\""
    #        echo_cmd="$dbg_cmd | cut -f$j"
    #        echo "executing $echo_cmd" 1>&2
    #        gt[$j]=`eval $echo_cmd`
            gt=`eval $echo_cmd`
            parsed_rec+="\t$gt"
        fi
    done
    echo -e "$parsed_rec" >> $out_file
done


##---------- filter annotation from summarize annovar --------------
#sed -n 1p $sa_db_file > $tmp_sa_filtered
#filter_sa="grep \"^exon\" $sa_db_file | grep -vP \"\tsyn\" | awk -F'\t' '{ if (\$3 != \"unknown\" && \$3 != \"\") print \$0}'  >> $tmp_sa_filtered"
#echo "" 1>&2
#echo "## ************************** filter annotation from summarize annovar *******************************" 1>&2
#echo "## filter only exon -> remove synonymous SNV -> remove all \"unknown\" and \"\" in ExonicFunc" 1>&2
#echo "## executing $filter_sa" 1>&2
#eval $filter_sa
##---------- filter annotation from summarize annovar --------------
#
#function join_sa_vcf_n_filter {
#    vcf_keys_file=$1
#    filtered_sa_file=$2
#    tmp_dir=$3
#
#    tmp_join_sa_vcf=$tmp_dir/tmp_join_sa_vcf
#
#    echo "" 1>&2
#    join_sa_vcf_clause="join -t $'\t' -1 1 -2 1 -o 2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.20,2.21,2.22,2.23,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.31,2.32,2.33,2.34"
#    join_sa_vcf_cmd="$join_sa_vcf_clause <( sort -t\$'\t' -k1 $vcf_keys_file ) <( awk -F '\t' '{ printf \"%s\t%s\n\", \$32, \$0 }' $filtered_sa_file | sort -t\$'\t' -k1 | grep -v \"Func\") | sort -t\$'\t' -n -k32 > $tmp_join_sa_vcf"
#    echo "## executing $join_sa_vcf_cmd" 1>&2
#    eval $join_sa_vcf_cmd
#
#    cat $tmp_join_sa_vcf
#}
#
#function build_common_mutations_csv {
#    gz_file=$1
#    sa_file=$2
#    tmp_dir=$3
#    col1=$4
#    col2=$5
#    col3=$6
#
#    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_"$project_name"
#
#    echo "## ************************** Build commmon mutations *******************************" 1>&2
#    echo "## generate vcf keys for all mutations that there are mutations in any members of family 242" 1>&2
#    get_vcf_records_clause="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if ((\$$col1 != \"./.\" && \$$col1 !~ \"0/0\") && (\$$col2 != \"./.\" && \$$col2 !~ \"0/0\") && (\$$col3 != \"./.\" && \$$col3 !~ \"0/0\")) print \$0 }'"
#    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d\t%s\t%s\t%s\n\", \$1, \$2, \$$col1, \$$col2, \$$col3 }' > $tmp_vcf_keys"
#    echo "## executing $generate_vcf_keys_cmd" 1>&2
#    eval $generate_vcf_keys_cmd
#    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d\t%s\t%s\t%s\n\", \$1, \$2, \$$col1, \$$col2, \$$col3 }' >> $tmp_vcf_keys"
#    echo "## executing $generate_vcf_keys_cmd" 1>&2
#    eval $generate_vcf_keys_cmd
#
#    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
#}
#
#function build_individual_mutations_csv {
#    gz_file=$1
#    sa_file=$2
#    tmp_dir=$3
#    col=$4
#
#    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_"$project_name"_"$col"
#
#    echo "## ************************** Build individual mutations (col $col)*******************************" 1>&2
#    echo "## generate vcf keys for individual mutations" 1>&2
#    get_vcf_records_clause="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if (\$$col != \"./.\" && \$$col !~ \"0/0\") print \$0 }'"
#    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d\t%s\n\", \$1, \$2, \$$col }' > $tmp_vcf_keys"
#    echo "## executing $generate_vcf_keys_cmd" 1>&2
#    eval $generate_vcf_keys_cmd
#    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d\t%s\n\", \$1, \$2, \$$col }' >> $tmp_vcf_keys"
#    echo "## executing $generate_vcf_keys_cmd" 1>&2
#    eval $generate_vcf_keys_cmd
#
#    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
#}
#
#echo "" 1>&2
#echo "## gerating csv for common mutation of family 242" 1>&2
#sed -n 1p $sa_db_file > $tmp_common_mutations_csv
#build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 $col2 $col3 >> $tmp_common_mutations_csv
#echo "" 1>&2
#echo "## gerating csv for individual mutation of patient $patient_code1" 1>&2
#sed -n 1p $sa_db_file > $tmp_individual_mutations_csv1
#build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 >> $tmp_individual_mutations_csv1
#echo "" 1>&2
#echo "## gerating csv for individual mutation of patient $patient_code2" 1>&2
#sed -n 1p $sa_db_file > $tmp_individual_mutations_csv2
#build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col2 >> $tmp_individual_mutations_csv2
#echo "" 1>&2
#echo "## gerating csv for individual mutation of patient $patient_code3" 1>&2
#sed -n 1p $sa_db_file > $tmp_individual_mutations_csv3
#build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col3 >> $tmp_individual_mutations_csv3
#echo "" 1>&2
#
#region_filter="awk -F'\t' '{if ((\$8 == \"3\" && \$9 > 118600000 && \$9 < 185000000) || (\$1 == \"Func\")) print \$0}'"
#
#cmd="$sort_n_awk_csv $tmp_common_mutations_csv | $region_filter > $out_common_mutations_csv"
#eval $cmd
#cmd="$sort_n_awk_csv $tmp_individual_mutations_csv1 | $region_filter > $out_individual_mutations_csv1"
#eval $cmd
#cmd="$sort_n_awk_csv $tmp_individual_mutations_csv2 | $region_filter > $out_individual_mutations_csv2"
#eval $cmd
#cmd="$sort_n_awk_csv $tmp_individual_mutations_csv3 | $region_filter > $out_individual_mutations_csv3"
#eval $cmd
#
#python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_individual_mutations_csv2 $patient_code2 $out_individual_mutations_csv3 $patient_code3 $out_common_mutations_csv $out_file
