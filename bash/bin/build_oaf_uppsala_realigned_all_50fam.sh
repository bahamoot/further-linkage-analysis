#!/bin/bash


echo "## plainly add all patients found in vcf files produced from uppsala" 1>&2
cmd="$HBVDB_BVD_ADD <( zcat $CMM_UPPSALA_50FAM_ALL_PATIENTS_GZ ) --database $CMM_HBVDB_UPPSALA_REALIGNED_ALL_50FAM"
echo "## executing $cmd" 1>&2
eval $cmd

cmd="$HBVDB_BVD_GET --database $CMM_HBVDB_UPPSALA_REALIGNED_ALL_50FAM > $CMM_OAF_UPPSALA_REALIGNED_ALL_50FAM"
echo "## executing $cmd" 1>&2
eval $cmd

