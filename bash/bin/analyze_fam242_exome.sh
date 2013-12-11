#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

csvs2xls_highlight_MT=$script_dir/csvs2xls_highlight_MT.py

project_name="fam242_exome"
patient_code[1]=Co441
patient_code[2]=Co771
patient_code[3]=Co666

working_dir=$script_dir/tmp
sa_db_file=$CMM_SCILIFE_ILLUMINA_MANS_SA_DB

oaf_file=$CMM_OAF_SCILIFE_ILLUMINA_ALL_FAM

other_families_sub_project_name[1]="scilife_illumina_families"
vcf_gz_file[1]=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ
vcf_header_file[1]=$CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_HEADER
other_families_sub_project_name[2]="uppsala_50fam"
vcf_gz_file[2]=$CMM_UPPSALA_50FAM_ALL_PATIENTS_GZ
vcf_header_file[2]=$CMM_UPPSALA_50FAM_ALL_PATIENTS_HEADER

out_dir=$script_dir/../out/"$project_name"
out_oaf_csv=$out_dir/"$project_name"_analyze_oaf.csv
out_file=$out_dir/"$project_name"_analyze.xls

echo "## analyze result from $project_name" 1>&2
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

gene_name[1]="WDR63"
gene_name[2]="EPB41L4B"
gene_name[3]="RHOXF2,RHOXF2B"

gene_name[4]="WDR63"
gene_name[5]="SYDE2"
gene_name[6]="FLG"
gene_name[7]="TBCE"
gene_name[8]="MTR"
gene_name[9]="KIF26B"
gene_name[10]="OR2G2"
gene_name[11]="GPR113"
gene_name[12]="C2orf71"
gene_name[13]="NEB"
gene_name[14]="NEB"
gene_name[15]="NEB"
gene_name[16]="KCNJ3"
gene_name[17]="MARCH7"
gene_name[18]="ABCB11"
gene_name[19]="ARIH2"
gene_name[20]="DNAJC13"
gene_name[21]="DZIP1L"
gene_name[22]="CLSTN2"
gene_name[23]="PCOLCE2"
gene_name[24]="IGSF10"
gene_name[25]="SUCNR1"
gene_name[26]="BOD1L1"
gene_name[27]="GPR125"
gene_name[28]="SEL1L3"
gene_name[29]="FAM50B"
gene_name[30]="MGAM"
gene_name[31]="ARHGEF5"
gene_name[32]="MLL3"
gene_name[33]="OR13C8"
gene_name[34]="ACTL7B"
gene_name[35]="SVEP1"
gene_name[36]="C9orf43"
gene_name[37]="TNC"
gene_name[38]="PAPPA"
gene_name[39]="CEL"
gene_name[40]="DNLZ"
gene_name[41]="DNLZ"
gene_name[42]="SEC16A"
gene_name[43]="NOTCH1"
gene_name[44]="AKR1C2"
gene_name[45]="ANKRD16"
gene_name[46]="OR10A4"
gene_name[47]="FAM86C1"
gene_name[48]="AMOTL1"
gene_name[49]="SNX19"
gene_name[50]="TAS2R7"
gene_name[51]="ACACB"
gene_name[52]="MVK"
gene_name[53]="CSPG4"
gene_name[54]="TPSAB1"
gene_name[55]="ERCC4"
gene_name[56]="MYH11"
gene_name[57]="HS3ST2"
gene_name[58]="MYO19"
gene_name[59]="PIGW"
gene_name[60]="MRM1"
gene_name[61]="KRTAP4-2"
gene_name[62]="SCN4A"
gene_name[63]="ABCA9"
gene_name[64]="EPB41L3"
gene_name[65]="LMAN1"
gene_name[66]="PIGN"
gene_name[67]="RTTN"
gene_name[68]="RTTN"
gene_name[69]="ZNF407"
gene_name[70]="ZFR2"
gene_name[71]="ZNF181"
gene_name[72]="TPTE"
gene_name[73]="TBC1D10A"
gene_name[74]="SF3A1"
gene_name[75]="GAL3ST1"
gene_name[76]="TRIOBP"
gene_name[77]="TRIOBP"
gene_name[78]="TRIOBP"
gene_name[79]="PKDREJ"
gene_name[80]="COL4A5"
gene_name[81]="RHOXF2,RHOXF2B"
gene_name[82]="BCORL1"
gene_name[83]="IGSF1"
gene_name[84]="FAM122C"

chrom[1]="1"
chrom[2]="9"
chrom[3]="X"

chrom[4]="1"
chrom[5]="1"
chrom[6]="1"
chrom[7]="1"
chrom[8]="1"
chrom[9]="1"
chrom[10]="1"
chrom[11]="2"
chrom[12]="2"
chrom[13]="2"
chrom[14]="2"
chrom[15]="2"
chrom[16]="2"
chrom[17]="2"
chrom[18]="2"
chrom[19]="3"
chrom[20]="3"
chrom[21]="3"
chrom[22]="3"
chrom[23]="3"
chrom[24]="3"
chrom[25]="3"
chrom[26]="4"
chrom[27]="4"
chrom[28]="4"
chrom[29]="6"
chrom[30]="7"
chrom[31]="7"
chrom[32]="7"
chrom[33]="9"
chrom[34]="9"
chrom[35]="9"
chrom[36]="9"
chrom[37]="9"
chrom[38]="9"
chrom[39]="9"
chrom[40]="9"
chrom[41]="9"
chrom[42]="9"
chrom[43]="9"
chrom[44]="10"
chrom[45]="10"
chrom[46]="11"
chrom[47]="11"
chrom[48]="11"
chrom[49]="11"
chrom[50]="12"
chrom[51]="12"
chrom[52]="12"
chrom[53]="15"
chrom[54]="16"
chrom[55]="16"
chrom[56]="16"
chrom[57]="16"
chrom[58]="17"
chrom[59]="17"
chrom[60]="17"
chrom[61]="17"
chrom[62]="17"
chrom[63]="17"
chrom[64]="18"
chrom[65]="18"
chrom[66]="18"
chrom[67]="18"
chrom[68]="18"
chrom[69]="18"
chrom[70]="19"
chrom[71]="19"
chrom[72]="21"
chrom[73]="22"
chrom[74]="22"
chrom[75]="22"
chrom[76]="22"
chrom[77]="22"
chrom[78]="22"
chrom[79]="22"
chrom[80]="X"
chrom[81]="X"
chrom[82]="X"
chrom[83]="X"
chrom[84]="X"

gene_pos[1]="85598679"
gene_pos[2]="111947836"
gene_pos[3]="119293216"

gene_pos[4]="85589842"
gene_pos[5]="85655916"
gene_pos[6]="152282684"
gene_pos[7]="235577776"
gene_pos[8]="236990141"
gene_pos[9]="245851609"
gene_pos[10]="247752109"
gene_pos[11]="26534041"
gene_pos[12]="29295186"
gene_pos[13]="152515585"
gene_pos[14]="152520258"
gene_pos[15]="152536299"
gene_pos[16]="155555406"
gene_pos[17]="160604936"
gene_pos[18]="169870004"
gene_pos[19]="48965078"
gene_pos[20]="132226100"
gene_pos[21]="137786409"
gene_pos[22]="140178381"
gene_pos[23]="142542415"
gene_pos[24]="151171329"
gene_pos[25]="151598890"
gene_pos[26]="13590380"
gene_pos[27]="22440018"
gene_pos[28]="25849449"
gene_pos[29]="3850338"
gene_pos[30]="141765172"
gene_pos[31]="144061117"
gene_pos[32]="151877127"
gene_pos[33]="107331452"
gene_pos[34]="111618209"
gene_pos[35]="113192279"
gene_pos[36]="116185655"
gene_pos[37]="117826096"
gene_pos[38]="119028233"
gene_pos[39]="135946690"
gene_pos[40]="139256468"
gene_pos[41]="139256541"
gene_pos[42]="139369066"
gene_pos[43]="139401233"
gene_pos[44]="5043821"
gene_pos[45]="5931230"
gene_pos[46]="6898495"
gene_pos[47]="71507157"
gene_pos[48]="94602414"
gene_pos[49]="130784886"
gene_pos[50]="10954583"
gene_pos[51]="109617728"
gene_pos[52]="110013879"
gene_pos[53]="75982072"
gene_pos[54]="1291548"
gene_pos[55]="14029033"
gene_pos[56]="15818842"
gene_pos[57]="22826046"
gene_pos[58]="34871721"
gene_pos[59]="34893326"
gene_pos[60]="34958598"
gene_pos[61]="39334241"
gene_pos[62]="62028920"
gene_pos[63]="67017930"
gene_pos[64]="5397383"
gene_pos[65]="57026436"
gene_pos[66]="59713173"
gene_pos[67]="67721492"
gene_pos[68]="67836115"
gene_pos[69]="72343156"
gene_pos[70]="3834863"
gene_pos[71]="35232677"
gene_pos[72]="10906915"
gene_pos[73]="30688659"
gene_pos[74]="30733787"
gene_pos[75]="30951208"
gene_pos[76]="38111897"
gene_pos[77]="38120542"
gene_pos[78]="38121013"
gene_pos[79]="46653273"
gene_pos[80]="107844666"
gene_pos[81]="119297530"
gene_pos[82]="129149906"
gene_pos[83]="130409697"
gene_pos[84]="133963268"

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
        dbg_cmd="tabix $vcf_gz_file ${chrom[$i]}":"${gene_pos[$i]}"-"${gene_pos[$i]}"
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

#---------- debug oaf --------------
echo -e "chrom\tstart pos\tend pos\tref\tobs\toaf" > $out_oaf_csv
for (( i=1; i<=$((${#gene_pos[@]})); i++ ))
do
    oaf_cmd="grep -P \"\t${gene_pos[$i]}\t\" $oaf_file >> $out_oaf_csv"
    eval $oaf_cmd
done
#---------- debug oaf --------------

csv2xls_cmd+=" $out_oaf_csv \"oaf\""
echo "executing $csv2xls_cmd" 1>&2
eval $csv2xls_cmd
