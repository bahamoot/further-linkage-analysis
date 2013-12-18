#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls=$script_dir/csvs2xls.py
sort_n_awk_csv=$script_dir/sort_n_awk_csv.sh

project_name="fam242_expectation_pass"
patient_code1=Co441
patient_code2=Co771
patient_code3=Co666

working_dir=$script_dir/tmp
sa_db_file=$CMM_SCILIFE_ILLUMINA_MANS_SA_DB
vcf_gz_file=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ
vcf_header_file=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_HEADER
tmp_sa_filtered=$working_dir/tmp_sa_filtered_for_"$project_name"
tmp_common_mutations_csv=$working_dir/"$project_name"_common_mutations_tmp.tab.csv
tmp_individual_mutations_csv1=$working_dir/"$project_name"_"$patient_code1"_tmp.tab.csv
tmp_individual_mutations_csv2=$working_dir/"$project_name"_"$patient_code2"_tmp.tab.csv
tmp_individual_mutations_csv3=$working_dir/"$project_name"_"$patient_code3"_tmp.tab.csv

out_dir=$script_dir/../out/"$project_name"
out_common_mutations_csv=$out_dir/"$project_name"_common_mutations.tab.csv
out_individual_mutations_csv1=$out_dir/"$project_name"_"$patient_code1".tab.csv
out_individual_mutations_csv2=$out_dir/"$project_name"_"$patient_code2".tab.csv
out_individual_mutations_csv3=$out_dir/"$project_name"_"$patient_code3".tab.csv
out_file=$out_dir/"$project_name".xls

echo "## building the xls file for $project_name" 1>&2
echo "## parameters" 1>&2
echo "## summarize_annovar_file: $sa_db_file" 1>&2
echo "## vcf gz file:            $vcf_gz_file" 1>&2
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
#col1=14
#col2=21
#col3=42
#---------- get vcf columns from patient codes --------------


#---------- filter annotation from summarize annovar --------------
cp $sa_db_file $tmp_sa_filtered

#sed -n 1p $sa_db_file > $tmp_sa_filtered
#filter_sa="grep \"^exon\" $sa_db_file | grep -vP \"\tsyn\" | awk -F'\t' '{ if (\$3 != \"unknown\" && \$3 != \"\") print \$0}'  >> $tmp_sa_filtered"
#echo "" 1>&2
#echo "## ************************** filter annotation from summarize annovar *******************************" 1>&2
#echo "## filter only exon -> remove synonymous SNV -> remove all \"unknown\" and \"\" in ExonicFunc" 1>&2
#echo "## executing $filter_sa" 1>&2
#eval $filter_sa
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
    col2=$5
    col3=$6

    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_"$project_name"

    echo "## ************************** Build commmon mutations *******************************" 1>&2
    echo "## generate vcf keys for all mutations that there are mutations in any members of family 242" 1>&2
    get_vcf_records_clause="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if ((\$$col1 !~ \"\\./\\.\" && \$$col1 !~ \"0/0\") && (\$$col2 !~ \"\\./\\.\" && \$$col2 !~ \"0/0\") && (\$$col3 !~ \"\\./\\.\" && \$$col3 !~ \"0/0\") && (\$7 == \"PASS\")) print \$0 }'"
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
    get_vcf_records_clause="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if (\$$col !~ \"\\./\\.\" && \$$col !~ \"0/0\" && \$7 == \"PASS\") print \$0 }'"
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -P \"^[0-9]\" | awk -F'\t' '{ printf \"%02d|%012d\t%s\n\", \$1, \$2, \$$col }' > $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd
    generate_vcf_keys_cmd="$get_vcf_records_clause | grep -vP \"^[0-9]\" | awk -F'\t' '{ printf \"%s|%012d\t%s\n\", \$1, \$2, \$$col }' >> $tmp_vcf_keys"
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $tmp_dir
}

echo "" 1>&2
echo "## generating csv for common mutation of family 242" 1>&2
sed -n 1p $sa_db_file > $tmp_common_mutations_csv
build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 $col2 $col3 >> $tmp_common_mutations_csv
echo "" 1>&2
echo "## generating csv for individual mutation of patient $patient_code1" 1>&2
sed -n 1p $sa_db_file > $tmp_individual_mutations_csv1
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 >> $tmp_individual_mutations_csv1
echo "" 1>&2
echo "## generating csv for individual mutation of patient $patient_code2" 1>&2
sed -n 1p $sa_db_file > $tmp_individual_mutations_csv2
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col2 >> $tmp_individual_mutations_csv2
echo "" 1>&2
echo "## generating csv for individual mutation of patient $patient_code3" 1>&2
sed -n 1p $sa_db_file > $tmp_individual_mutations_csv3
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col3 >> $tmp_individual_mutations_csv3
echo "" 1>&2

function count_expectation {
    tmp_csv=$1
    out_csv=$2

    echo -e "Func\tCount" > $out_csv
    cut -f1 $tmp_csv | sort | uniq -c | grep -v Func | awk '{ printf "%s\t%s\n", substr($0,9,60), substr($0,1,7)}' >> $out_csv
    total_func_count=`grep -v Func $tmp_csv | wc -l`
    echo "" >> $out_csv
    echo -e "Total\t$total_func_count" >> $out_csv
    echo "" >> $out_csv
    echo "" >> $out_csv
    echo "" >> $out_csv
    echo -e "ExonicFunc\tCount" >> $out_csv
    cut -f3 $tmp_csv | grep -v "^$" | sort | uniq -c | grep -v Func | awk '{ printf "%s\t%s\n", substr($0,9,60), substr($0,1,7)}' >> $out_csv
    total_exonic_func_count=`cut -f3 $tmp_csv | grep -v "^$" | grep -v Func | wc -l`
    echo "" >> $out_csv
    echo -e "Total\t$total_exonic_func_count" >> $out_csv
}

count_expectation $tmp_individual_mutations_csv1 $out_individual_mutations_csv1
count_expectation $tmp_individual_mutations_csv2 $out_individual_mutations_csv2
count_expectation $tmp_individual_mutations_csv3 $out_individual_mutations_csv3
count_expectation $tmp_common_mutations_csv $out_common_mutations_csv



python $csvs2xls $out_individual_mutations_csv1 $patient_code1 $out_individual_mutations_csv2 $patient_code2 $out_individual_mutations_csv3 $patient_code3 $out_common_mutations_csv $out_file
