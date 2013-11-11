#!/bin/bash


cmd="$HBVDB_BVD_ADD <( zcat $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ ) --database $CMM_LINKAGE_OAF_SCILIFE_ILLUMINA_ALL_FAM"
echo "plainly add all patients found in vcf files produced by Mans from Scilife-Illumina project"
echo "executing $cmd" 1>&2
eval $cmd

