#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

working_dir=$script_dir/tmp
sa_db_file=$CMM_SCILIFE_ILLUMINA_SA_DB
vcf_gz_file=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ
tmp_sa_filtered=$working_dir/tmp_sa_filtered_for_fam24_exome

patient_code1=Co441
patient_code2=Co771
patient_code3=Co666

out_dir=$script_dir/../out/fam242_exome
out_common_mutations_csv=$out_dir/fam242_common_mutations.tab.csv
out_individual_mutations_csv1=$out_dir/fam242_"$patient_code1".tab.csv
out_individual_mutations_csv2=$out_dir/fam242_"$patient_code2".tab.csv
out_individual_mutations_csv3=$out_dir/fam242_"$patient_code3".tab.csv

maf_filter=0.1
oaf_filter=0.1

echo "## building summarize annovar database" 1>&2
echo "## parameters" 1>&2
echo "## summarize_annovar_file:  $sa_db_file" 1>&2
echo "## vcf gz file:    $vcf_gz_file" 1>&2
echo "## working_dir: $working_dir" 1>&2
echo "## out_file:    $out_file" 1>&2

#---------- get vcf columns from patient codes --------------
function get_vcf_col {
    zcat $1 | grep "^#C" | grep -i $2 | awk -va="$2" 'BEGIN{}
    END{}
    {
        for(i=1;i<=NF;i++){
            IGNORECASE = 1
            if ( tolower($i) == tolower(a))
                {print i }
        }
    }'
}

col1=`get_vcf_col $vcf_gz_file $patient_code1`
col2=`get_vcf_col $vcf_gz_file $patient_code2`
col3=`get_vcf_col $vcf_gz_file $patient_code3`
#col1=14
#col2=21
#col3=42
#---------- get vcf columns from patient codes --------------


#---------- filter annotation from summarize annovar --------------
filter_sa="grep \"^exon\" $sa_db_file | grep -vP \"\tsyn\" | awk -F'\t' '{ if (\$3 != \"unknown\" && \$3 != \"\") print \$0}' | awk -F'\t' '{ if (\$8 == \"\" || \$8 < $maf_filter) print \$0}' > $tmp_sa_filtered"
echo "## filter only exon -> remove synonymous SNV -> remove all \"unknown\" and \"\" in ExonicFunc -> remove those with MAF 1000g2012apr_ALL >= 0.1" 1>&2
echo "## executing $filter_sa" 1>&2
eval $filter_sa
#---------- filter annotation from summarize annovar --------------

function join_sa_vcf_n_filter {
    vcf_keys_file=$1
    filtered_sa_file=$2
    tmp_dir=$3

    tmp_join_sa_vcf=$tmp_dir/tmp_join_sa_vcf

    join_sa_vcf_cmd="join -t $'\t' -1 1 -2 1 -o 2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.20,2.21,2.22,2.23,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.31,2.32,2.33,2.34 <( awk -F'\t' '{ if (\$1 !~ /X/ && \$1 !~ /Y/ && \$1 !~ /MT/) print \$0 }' $vcf_keys_file | sort -k1) <( awk -F '\t' '{ printf \"%s\t%s\n\", \$32, \$0 }' $filtered_sa_file | awk -F'\t' '{ if (\$1 !~ /X/ && \$1 !~ /Y/ && \$1 !~ /MT/) print \$0 }' | sort -k1) | awk -F'\t' '{ if (\$33 < $oaf_filter ) print \$0 }' | sort -n -k32 -t\$'\t' > $tmp_join_sa_vcf"
    echo "## executing $join_sa_vcf_cmd" 1>&2
    eval $join_sa_vcf_cmd
    join_sa_vcf_cmd="join -t $'\t' -1 1 -2 1 -o 2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,2.10,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.20,2.21,2.22,2.23,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.31,2.32,2.33,2.34 <( awk -F'\t' '{ if (\$1 ~ /X/ || \$1 ~ /Y/ || \$1 ~ /MT/) print \$0 }' $vcf_keys_file | sort -k1) <( awk -F '\t' '{ printf \"%s\t%s\n\", \$32, \$0 }' $filtered_sa_file | awk -F'\t' '{ if (\$1 ~ /X/ || \$1 ~ /Y/ || \$1 ~ /MT/) print \$0 }' | sort -k1) | awk -F'\t' '{ if (\$33 < $oaf_filter ) print \$0 }' | sort -n -k32 -t\$'\t' >> $tmp_join_sa_vcf"
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

    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_fam24_exome

    generate_vcf_keys_cmd="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if ((\$$col1 != \"./.\" && \$$col1 !~ \"0/0\") && (\$$col2 != \"./.\" && \$$col2 !~ \"0/0\") && (\$$col3 != \"./.\" && \$$col3 !~ \"0/0\")) printf \"%s|%012d\t%s\t%s\t%s\n\", \$1, \$2, \$$col1, \$$col2, \$$col3 }' > $tmp_vcf_keys"
    echo "## generate vcf keys for all mutations that there are mutations in any members of family 242" 1>&2
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $out_csv_file $tmp_dir
}

function build_individual_mutations_csv {
    gz_file=$1
    sa_file=$2
    tmp_dir=$3
    col=$4

    tmp_vcf_keys=$tmp_dir/tmp_vcf_keys_for_fam24_exome

    generate_vcf_keys_cmd="zcat $gz_file | grep -v \"^#\" | awk -F'\t' '{ if (\$$col != \"./.\" && \$$col !~ \"0/0\") printf \"%s|%012d\t%s\n\", \$1, \$2, \$$col }' > $tmp_vcf_keys"
    echo "## generate vcf keys for individual mutations" 1>&2
    echo "## executing $generate_vcf_keys_cmd" 1>&2
    eval $generate_vcf_keys_cmd

    join_sa_vcf_n_filter $tmp_vcf_keys $sa_file $out_csv_file $tmp_dir
}

echo "## gerating csv for common mutation of family 242" 1>&2
sed -n 1p $sa_db_file > $out_common_mutations_csv
build_common_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 $col2 $col3 >> $out_common_mutations_csv
echo "## gerating csv for common mutation of patient $patient_code1" 1>&2
sed -n 1p $sa_db_file > $out_individual_mutations_csv1
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col1 >> $out_individual_mutations_csv1
echo "## gerating csv for common mutation of patient $patient_code2" 1>&2
sed -n 1p $sa_db_file > $out_individual_mutations_csv2
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col2 >> $out_individual_mutations_csv2
echo "## gerating csv for common mutation of patient $patient_code3" 1>&2
sed -n 1p $sa_db_file > $out_individual_mutations_csv3
build_individual_mutations_csv $vcf_gz_file $tmp_sa_filtered $working_dir $col3 >> $out_individual_mutations_csv3
