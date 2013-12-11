#!/bin/bash


echo "## plainly generate oaf using all patients found in vcf files produced by Mans from Scilife-Illumina project" 1>&2
cmd="$HBVDB_BVD_ADD <( zcat $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ ) --database $CMM_HBVDB_SCILIFE_ILLUMINA_ALL_FAM"
echo "## executing $cmd" 1>&2
eval $cmd

cmd="$HBVDB_BVD_GET --database $CMM_HBVDB_SCILIFE_ILLUMINA_ALL_FAM > $CMM_OAF_SCILIFE_ILLUMINA_ALL_FAM"
echo "## executing $cmd" 1>&2
eval $cmd

