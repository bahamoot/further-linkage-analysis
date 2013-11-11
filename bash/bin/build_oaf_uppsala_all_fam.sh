#!/bin/bash


cmd="$HBVDB_BVD_ADD <( zcat $CMM_UPPSALA_ALL_PATIENTS_BWA_GATK_GZ ) --database $CMM_LINKAGE_OAF_UPPSALA_ALL_FAM"
echo "plainly add all patients found in vcf files produced from uppsala"
echo "executing $cmd" 1>&2
eval $cmd

