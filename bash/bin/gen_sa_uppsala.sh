#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_sa=$script_dir/script_build_sa.sh
working_dir=$script_dir/tmp

$script_build_sa "" "" "" $CMM_UPPSALA_ALL_PATIENTS_BWA_GATK_GZ $CMM_OAF_UPPSALA_ALL_FAM $working_dir "uppsala" $CMM_UPPSALA_SA_DB
