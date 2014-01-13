#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls=$script_dir/csvs2xls.py
sort_n_awk_csv=$script_dir/sort_n_awk_csv.sh

project_name="chr9_axeq"
sub_project_name=$1
chrom=$2
min_pos=$3
max_pos=$4
family_code=$5

patient_count=0
declare -a args=("$@")
for (( i=5; i<$((${#args[@]})); i++ ))
do
    patient_count=$((patient_count+1))
    patient_code[$patient_count]="${args[$i]}"
done

working_dir=$script_dir/tmp
sa_db_file=$CMM_AXEQ_CHR9_SA_DB
vcf_gz_file=$CMM_AXEQ_CHR9_ALL_PATIENTS_GZ
vcf_header_file=$CMM_AXEQ_CHR9_ALL_PATIENTS_HEADER
tmp_sa_filtered=$working_dir/tmp_sa_filtered_for_"$project_name"_fam"$family_code"
tmp_common_mutations_csv=$working_dir/"$project_name"_"$sub_project_name"_fam"$family_code"_common_mutations_tmp.tab.csv

project_out_dir=$script_dir/../out/"$project_name"
sub_project_out_dir=$project_out_dir/"$sub_project_name"
out_dir=$sub_project_out_dir/"fam_"$family_code
out_common_mutations_csv=$out_dir/"$sub_project_name"_fam"$family_code"_common_mutations.tab.csv
out_file=$out_dir/"$sub_project_name"_fam"$family_code".xls

echo "##" 1>&2
echo "##" 1>&2
echo "##" 1>&2
echo "## (for sanna and vinay) building an xls file for project $project_name" 1>&2
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

echo "##" 1>&2
echo "## family & members" 1>&2
echo "## family code:            $family_code" 1>&2
for (( i=1; i<=$((${#patient_code[@]})); i++ ))
do
    patient_col[$i]=`get_vcf_col $vcf_header_file ${patient_code[$i]}`
    echo "## patient code$i:          ${patient_code[$i]}" 1>&2
    echo "## column:                 ${patient_col[$i]}" 1>&2
done

#---------- display sub project configuration --------------

echo "##" 1>&2
echo "## sub project configuration" 1>&2
echo "## sub project name:       $sub_project_name" 1>&2
echo "## chromosome:             $chrom" 1>&2
echo "## min position:           $min_pos" 1>&2
echo "## max position:           $max_pos" 1>&2

#---------- check if output directory exist --------------
if [ ! -d "$project_out_dir" ]; then
    mkdir $project_out_dir
fi
if [ ! -d "$sub_project_out_dir" ]; then
    mkdir $sub_project_out_dir
fi
if [ ! -d "$out_dir" ]; then
    mkdir $out_dir
fi
#---------- check if output directory exist --------------

function join_sa_vcf_n_filter {
    vcf_keys_file=$1
    filtered_sa_file=$2
    tmp_dir=$3

    tmp_join_sa_vcf=$tmp_dir/tmp_join_sa_vcf

    echo "" 1>&2
    join_sa_vcf_clause="join -t $'\t' -1 1 -2 1 -o 2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.20,2.21,2.22,2.23,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.31,2.32,2.33,2.34"
    join_sa_vcf_cmd="$join_sa_vcf_clause <( sort -t\$'\t' -k1,1 $vcf_keys_file ) <( awk -F '\t' '{ printf \"%s\t%s\n\", \$28, \$0 }' $filtered_sa_file | sort -t\$'\t' -k1,1 | grep -v \"Func\") | sort -t\$'\t' -n -k28 > $tmp_join_sa_vcf"
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
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d|%s|%s\t%s\t%s\t%s\n\", \$1, \$2, \$4, \$5, \$$col1, \$$col2, \$$col3 }' > $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d|%s|%s\t%s\t%s\t%s\n\", \$1, \$2, \$4, \$5, \$$col1, \$$col2, \$$col3 }' >> $tmp_vcf_keys"
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
    get_vcf_records_clause="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if (\$$col != \".\" && \$$col !~ \"\\./\\.\" && \$$col !~ \"0/0\") print \$0 }'"
    get_vcf_records_clause="tabix $gz_file $chrom":"$min_pos"-"$max_pos | grep -v \"^#\" | awk -F'\t' '{ if (\$$col != \".\" && \$$col !~ \"\\./\\.\" && \$$col !~ \"0/0\") print \$0 }'"
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d|%s|%s\t%s\n\", \$1, \$2, \$4, \$5, \$$col }' > $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d|%s|%s\t%s\n\", \$1, \$2, \$4, \$5, \$$col }' >> $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
}

#---------- filter annotation from summarize annovar --------------
sed -n 1p $sa_db_file > $tmp_sa_filtered
filter_sa="cat $sa_db_file   > $tmp_sa_filtered"
#filter_sa="grep \"^exon\" $sa_db_file | grep -vP \"\tsyn\" | awk -F'\t' '{ if (\$3 != \"unknown\" && \$3 != \"\") print \$0}'  >> $tmp_sa_filtered"
echo "" 1>&2
echo "## ************************** filter annotation from summarize annovar *******************************" 1>&2
echo "## no filter" 1>&2
echo "## executing $filter_sa" 1>&2
eval $filter_sa
#---------- filter annotation from summarize annovar --------------

#---------- generate csv files --------------
# individuals
for (( i=1; i<=$((${#patient_code[@]})); i++ ))
do
    tmp_individual_mutations_csv[$i]=$working_dir/"$project_name"_"$sub_project_name"_fam"$family_code"_"${patient_code[$i]}"_tmp.tab.csv
    out_individual_mutations_csv[$i]=$out_dir/"$sub_project_name"_fam"$family_code"_"${patient_code[$i]}".tab.csv

    echo "" 1>&2
    echo "## gerating csv for individual mutation of patient ${patient_code[$i]}" 1>&2
    sed -n 1p $sa_db_file > ${tmp_individual_mutations_csv[$i]}
    build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir ${patient_col[$i]} >> ${tmp_individual_mutations_csv[$i]}

    cmd="$sort_n_awk_csv ${tmp_individual_mutations_csv[$i]}  > ${out_individual_mutations_csv[$i]}"
    eval $cmd
done

# common
if [ $# -ge 7 ]; then
    build_common_mutations_csv_cmd="build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir "
    for (( i=1; i<=$((${#patient_code[@]})); i++ ))
    do
        build_common_mutations_csv_cmd+=" ${patient_col[$i]} "
    done

    echo "" 1>&2
    echo "## gerating csv for common mutation" 1>&2
    sed -n 1p $sa_db_file > $tmp_common_mutations_csv
    build_common_mutations_csv_cmd+=" >> $tmp_common_mutations_csv"
    eval $build_common_mutations_csv_cmd

    cmd="$sort_n_awk_csv $tmp_common_mutations_csv > $out_common_mutations_csv"
    eval $cmd
fi
#---------- generate csv files --------------

#---------- generate output xls file --------------
if [ $# -eq 6 ]; then
    python_cmd="python $csvs2xls ${out_individual_mutations_csv[1]} ${patient_code[1]} $out_file"
    echo "" 1>&2
    echo "executing $python_cmd" 1>&2
    eval $python_cmd
else
    python_cmd="python $csvs2xls "
    for (( i=1; i<=$((${#patient_code[@]})); i++ ))
    do
        python_cmd+=" ${out_individual_mutations_csv[$i]} ${patient_code[$i]} "
    done
    python_cmd+=" $out_common_mutations_csv $out_file"
    echo "" 1>&2
    echo "executing $python_cmd" 1>&2
    eval $python_cmd
fi
#---------- generate output xls file --------------

