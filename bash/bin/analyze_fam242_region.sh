#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls_highlight_MT=$script_dir/csvs2xls_highlight_MT.py

project_name="fam242_region"
patient_code[1]=Co441
patient_code[2]=Co771
patient_code[3]=Co666

working_dir=$script_dir/tmp
sa_db_file=$CMM_SCILIFE_ILLUMINA_MANS_SA_DB

other_families_sub_project_name[1]="scilife_illumina_families"
vcf_gz_file[1]=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ
vcf_header_file[1]=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_HEADER
other_families_sub_project_name[2]="uppsala_50fam"
vcf_gz_file[2]=$CMM_UPPSALA_50FAM_ALL_PATIENTS_GZ
vcf_header_file[2]=$CMM_UPPSALA_50FAM_ALL_PATIENTS_HEADER

out_dir=$script_dir/../out/"$project_name"
out_file=$out_dir/"$project_name"_analyze.xls

echo "## analyze result from family 242 region" 1>&2
echo "## parameters" 1>&2
echo "## summarize_annovar_file: $sa_db_file" 1>&2
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

#---------- debug other families --------------
function cut_gt {
    rec=$1
    field=$2
    cut_cmd="echo \"$rec\" | cut -f$field -d\" \" | cut -f1 -d\":\""
    eval $cut_cmd
}

function lookup_mt_in_other_families {
    vcf_gz_file=$1
    vcf_header_file=$2

    for (( i=1; i<=$((${#patient_code[@]})); i++ ))
    do
        patient_col[$i]=`get_vcf_col $vcf_header_file ${patient_code[$i]}`
        echo "## patient code$i:          ${patient_code[$i]}" 1>&2
        echo "## column:                 ${patient_col[$i]}" 1>&2
    done
    tmp_csv="$working_dir/tmp.csv"

    printf_str=""
    patient_param=""
    for (( i=1; i<=$((${#patient_code[@]})); i++ ))
    do
        printf_str+="\t%s"
        patient_param+=", \$${patient_col[$i]}"
    done

    n_col=`awk -F '\t' '{print NF}' $vcf_header_file`

    parsed_header="gene\tchrom\tposition"
    case_header=""
    non_case_header=""
    for (( j=1; j<=$n_col; j++ ))
    do
        if [ $j -ne 1 ] && [ $j -ne 2 ] && [ $j -ne 3 ] && [ $j -ne 6 ] && [ $j -ne 7 ] && [ $j -ne 8 ] && [ $j -ne 9 ]; then
            case=0
            for (( k=1; k<=$((${#patient_code[@]})); k++ ))
            do
                if [ -n "${patient_col[$k]}" ]; then
                    if [ $j -eq ${patient_col[$k]} ]; then
                        case=$j
                    fi
                fi
            done
            if [ $case -ne 0 ]; then
                cut_cmd="cut -f$case $vcf_header_file"
                case_header+="\t"`eval $cut_cmd`
            elif [ $j -gt 9 ]; then
                cut_cmd="cut -f$j $vcf_header_file"
                non_case_header+="\t"`eval $cut_cmd`
            else
                cut_cmd="cut -f$j $vcf_header_file"
                parsed_header+="\t"`eval $cut_cmd`
            fi
        fi
    done
    parsed_header+="$case_header"
    parsed_header+="$non_case_header"
    echo -e "$parsed_header" > $tmp_csv

    for (( i=1; i<=$((${#gene_pos[@]})); i++ ))
    do
        dbg_cmd="tabix $vcf_gz_file $chrom":"${gene_pos[$i]}"-"${gene_pos[$i]}"
        rec=`eval $dbg_cmd`
        parsed_rec="${gene_name[$i]}"
        case_gts=""
        non_case_gts=""
        for (( j=1; j<=$n_col; j++ ))
        do
            if [ $j -ne 3 ] && [ $j -ne 6 ] && [ $j -ne 7 ] && [ $j -ne 8 ] && [ $j -ne 9 ]; then
                case=0
                for (( k=1; k<=$((${#patient_code[@]})); k++ ))
                do
                    if [ -n "${patient_col[$k]}" ]; then
                        if [ $j -eq ${patient_col[$k]} ]; then
                            case=$j
                        fi
                    fi
                done
                if [ $case -ne 0 ]; then
                    case_gts+="\t"`cut_gt "$rec" "$case"`
                elif [ $j -gt 9 ]; then
                    non_case_gts+="\t"`cut_gt "$rec" "$j"`
                else
                    parsed_rec+="\t"`cut_gt "$rec" "$j"`
                fi
            fi
        done
        parsed_rec+="$case_gts"
        parsed_rec+="$non_case_gts"
        echo -e "$parsed_rec" >> $tmp_csv
    done

    cat $tmp_csv
}

csv2xls_cmd="python $csvs2xls_highlight_MT $out_file"

for (( n=1; n<=$((${#other_families_sub_project_name[@]})); n++ ))
do
    csv_file=$out_dir/"$project_name"_analyze_other_${other_families_sub_project_name[$n]}.csv
    echo "" 1>&2
    echo "## sub project name:       ${other_families_sub_project_name[$n]}" 1>&2
    echo "## vcf file:               ${vcf_gz_file[$n]}" 1>&2
    echo "## header file:            ${vcf_header_file[$n]}" 1>&2
    lookup_mt_in_other_families ${vcf_gz_file[$n]} ${vcf_header_file[$n]} $scilife_illumina_mans_vcf_header_file > $csv_file

    csv2xls_cmd+=" $csv_file ${other_families_sub_project_name[$n]}"
done

#---------- debug other families --------------

echo "executing $csv2xls_cmd" 1>&2
eval $csv2xls_cmd
