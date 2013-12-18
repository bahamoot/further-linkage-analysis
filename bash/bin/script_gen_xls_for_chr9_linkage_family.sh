#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls=$script_dir/csvs2xls.py
sort_n_awk_csv=$script_dir/sort_n_awk_csv.sh

project_name="chr9_linkage"
chrom=$1
min_pos=$2
max_pos=$3
family_code=$4
patient_code1=$5
patient_code2=$6
patient_code3=$7

working_dir=$script_dir/tmp
sa_db_file=$CMM_UPPSALA_SA_DB
vcf_gz_file=$CMM_UPPSALA_ALL_PATIENTS_BWA_GATK_GZ
vcf_header_file=$CMM_UPPSALA_ALL_PATIENTS_BWA_GATK_HEADER
tmp_sa_filtered=$working_dir/tmp_sa_filtered_for_"$project_name"_fam"$family_code"
tmp_common_mutations_csv=$working_dir/"$project_name"_fam"$family_code"_common_mutations_tmp.tab.csv
tmp_individual_mutations_csv1=$working_dir/"$project_name"_fam"$family_code"_"$patient_code1"_tmp.tab.csv
tmp_individual_mutations_csv2=$working_dir/"$project_name"_fam"$family_code"_"$patient_code2"_tmp.tab.csv
tmp_individual_mutations_csv3=$working_dir/"$project_name"_fam"$family_code"_"$patient_code3"_tmp.tab.csv

out_dir=$script_dir/../out/"$project_name"/fam_"$family_code"
out_common_mutations_csv=$out_dir/"$project_name"_fam"$family_code"_common_mutations.tab.csv
out_individual_mutations_csv1=$out_dir/"$project_name"_fam"$family_code"_"$patient_code1".tab.csv
out_individual_mutations_csv2=$out_dir/"$project_name"_fam"$family_code"_"$patient_code2".tab.csv
out_individual_mutations_csv3=$out_dir/"$project_name"_fam"$family_code"_"$patient_code3".tab.csv
out_file=$out_dir/"$project_name"_fam"$family_code".xls

echo "## building the xls file chr9 linkage family $family_code" 1>&2
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

col1=`get_vcf_col $vcf_header_file $patient_code1`
col2=`get_vcf_col $vcf_header_file $patient_code2`
col3=`get_vcf_col $vcf_header_file $patient_code3`

#---------- get vcf columns from patient codes --------------

echo "## family & members" 1>&2
echo "## family code:            $family_code" 1>&2
echo "## patient code1:          $patient_code1" 1>&2
echo "## column:                 $col1" 1>&2
echo "## patient code2:          $patient_code2" 1>&2
echo "## column:                 $col2" 1>&2
echo "## patient code3:          $patient_code3" 1>&2
echo "## column:                 $col3" 1>&2
echo "## chrom:                  $chrom" 1>&2
echo "## min position:           $min_pos" 1>&2
echo "## max position:           $max_pos" 1>&2

#---------- check if output directory exist --------------
if [ ! -d "$out_dir" ]; then
    mkdir $out_dir
fi
#---------- check if output directory exist --------------

#---------- filter annotation from summarize annovar --------------
sed -n 1p $sa_db_file > $tmp_sa_filtered
filter_sa="grep \"^exon\" $sa_db_file | grep -vP \"\tsyn\" | awk -F'\t' '{ if (\$3 != \"unknown\" && \$3 != \"\") print \$0}'  >> $tmp_sa_filtered"
echo "" 1>&2
echo "## ************************** filter annotation from summarize annovar *******************************" 1>&2
echo "## filter only exon -> remove synonymous SNV -> remove all \"unknown\" and \"\" in ExonicFunc" 1>&2
echo "## executing $filter_sa" 1>&2
eval $filter_sa
#---------- filter annotation from summarize annovar --------------

function join_sa_vcf_n_filter {
    vcf_keys_file=$1
    filtered_sa_file=$2
    tmp_dir=$3

    tmp_join_sa_vcf=$tmp_dir/tmp_join_sa_vcf

    echo "" 1>&2
    join_sa_vcf_clause="join -t $'\t' -1 1 -2 1 -o 2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.20,2.21,2.22,2.23,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.31,2.32,2.33,2.34"
    join_sa_vcf_cmd="$join_sa_vcf_clause <( sort -t\$'\t' -k1 $vcf_keys_file ) <( awk -F '\t' '{ printf \"%s\t%s\n\", \$32, \$0 }' $filtered_sa_file | sort -t\$'\t' -k1 | grep -v \"Func\") | sort -t\$'\t' -n -k32 > $tmp_join_sa_vcf"
    echo "## executing $join_sa_vcf_cmd" 1>&2
    eval $join_sa_vcf_cmd

    cat $tmp_join_sa_vcf
}

function build_common_mutations_csv {
    gz_file=$1
    sa_file=$2
    tmp_dir=$3
    col1=$4
    col2=$4
    col3=$4

    if [ $# -gt 4 ]; then
        col2=$5
    fi
    if [ $# -gt 5 ]; then
        col3=$6
    fi

    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_"$project_name"

    echo "## ************************** Build commmon mutations *******************************" 1>&2
    echo "## generate vcf keys for all mutations that there are mutations in any members of family $family_code" 1>&2
    get_vcf_records_clause="tabix $gz_file $chrom":"$min_pos"-"$max_pos | grep -v \"^#\" | awk -F'\t' '{ if ((\$$col1 != \".\" && \$$col1 != \"./.\" && \$$col1 !~ \"0/0\") && (\$$col2 != \".\" && \$$col2 != \"./.\" && \$$col2 !~ \"0/0\") && (\$$col3 != \".\" && \$$col3 != \"./.\" && \$$col3 !~ \"0/0\")) print \$0 }'"
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d\t%s\t%s\t%s\n\", \$1, \$2, \$$col1, \$$col2, \$$col3 }' > $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d\t%s\t%s\t%s\n\", \$1, \$2, \$$col1, \$$col2, \$$col3 }' >> $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
}

function build_individual_mutations_csv {
    gz_file=$1
    sa_file=$2
    tmp_dir=$3
    col=$4

    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_"$project_name"_"$col"

    echo "## ************************** Build individual mutations (col $col)*******************************" 1>&2
    echo "## generate vcf keys for individual mutations" 1>&2
    get_vcf_records_clause="tabix $gz_file $chrom":"$min_pos"-"$max_pos | grep -v \"^#\" | awk -F'\t' '{ if (\$$col != \".\" && \$$col != \"./.\" && \$$col !~ \"0/0\") print \$0 }'"
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d\t%s\n\", \$1, \$2, \$$col }' > $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d\t%s\n\", \$1, \$2, \$$col }' >> $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
}

echo "" 1>&2
echo "## gerating csv for individual mutation of patient $patient_code1" 1>&2
sed -n 1p $sa_db_file > $tmp_individual_mutations_csv1
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 >> $tmp_individual_mutations_csv1

cmd="$sort_n_awk_csv $tmp_individual_mutations_csv1  > $out_individual_mutations_csv1"
eval $cmd

if [ $# -eq 5 ]; then
    python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_file
else
    echo "" 1>&2
    echo "## gerating csv for individual mutation of patient $patient_code2" 1>&2
    sed -n 1p $sa_db_file > $tmp_individual_mutations_csv2
    build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col2 >> $tmp_individual_mutations_csv2

    cmd="$sort_n_awk_csv $tmp_individual_mutations_csv2  > $out_individual_mutations_csv2"
    eval $cmd

    if [ $# -eq 6 ]; then
        echo "" 1>&2
        echo "## gerating csv for common mutation of family $family_code" 1>&2
        sed -n 1p $sa_db_file > $tmp_common_mutations_csv
        build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 $col2 >> $tmp_common_mutations_csv
        echo "" 1>&2

        cmd="$sort_n_awk_csv $tmp_common_mutations_csv > $out_common_mutations_csv"
        eval $cmd

        python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_individual_mutations_csv2 $patient_code2 $out_common_mutations_csv $out_file
    else
        if [ $# -eq 7 ]; then
            echo "" 1>&2
            echo "## gerating csv for individual mutation of patient $patient_code3" 1>&2
            sed -n 1p $sa_db_file > $tmp_individual_mutations_csv3
            build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col3 >> $tmp_individual_mutations_csv3

            cmd="$sort_n_awk_csv $tmp_individual_mutations_csv3  > $out_individual_mutations_csv3"
            eval $cmd

            echo "" 1>&2
            echo "## gerating csv for common mutation of family $family_code" 1>&2
            sed -n 1p $sa_db_file > $tmp_common_mutations_csv
            build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 $col2 $col3 >> $tmp_common_mutations_csv
            echo "" 1>&2
            cmd="$sort_n_awk_csv $tmp_common_mutations_csv > $out_common_mutations_csv"
            eval $cmd

            python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_individual_mutations_csv2 $patient_code2 $out_individual_mutations_csv3 $patient_code3 $out_common_mutations_csv $out_file
        fi
    fi
fi
#
#python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_individual_mutations_csv2 $patient_code2 $out_common_mutations_csv $out_file
