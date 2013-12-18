#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

working_dir=$script_dir/tmp
tmp_oaf=$working_dir/tmp_oaf

out_oaf=$CMM_OAF_UPPSALA_REALIGNED_ALL_50FAM

echo "## plainly add all patients found in vcf files produced from uppsala" 1>&2
cmd="$HBVDB_BVD_ADD <( zcat $CMM_UPPSALA_50FAM_ALL_PATIENTS_GZ ) --database $CMM_HBVDB_UPPSALA_REALIGNED_ALL_50FAM"
echo "## executing $cmd" 1>&2
eval $cmd

cmd="$HBVDB_BVD_GET --database $CMM_HBVDB_UPPSALA_REALIGNED_ALL_50FAM > $tmp_oaf"
echo "## executing $cmd" 1>&2
eval $cmd

echo "##" 1>&2
oaf_key_cmd="grep -P \"^[0-9]\" $tmp_oaf | awk -F'\t' '{ printf \"%02d|%012d|%s|%s\t%s\n\", \$1, \$2, \$4, \$5, \$6}' | sort -k1 > $out_oaf"
echo "## executing $oaf_key_cmd" 1>&2
eval $oaf_key_cmd
oaf_key_cmd="grep -vP \"^[0-9]\" $tmp_oaf | awk -F'\t' '{ printf \"%s|%012d|%s|%s\t%s\n\", \$1, \$2, \$4, \$5, \$6}' | sort -k1 >> $out_oaf"
echo "## executing $oaf_key_cmd" 1>&2
eval $oaf_key_cmd
