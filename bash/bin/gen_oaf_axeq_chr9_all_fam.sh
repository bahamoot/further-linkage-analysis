#!/bin/bash


echo "## plainly generate oaf using all patients found in chr9 vcf files produced by axeq" 1>&2
cmd="$HBVDB_BVD_ADD <( zcat $CMM_AXEQ_CHR9_ALL_PATIENTS_GZ ) --database $CMM_HBVDB_AXEQ_CHR9_ALL_FAM"
echo "## executing $cmd" 1>&2
eval $cmd

cmd="$HBVDB_BVD_GET --database $CMM_HBVDB_AXEQ_CHR9_ALL_FAM > $CMM_OAF_AXEQ_CHR9_ALL_FAM"
echo "## executing $cmd" 1>&2
eval $cmd

