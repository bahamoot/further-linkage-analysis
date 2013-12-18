#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_sa=$script_dir/script_build_sa.sh
working_dir=$script_dir/tmp

$script_build_sa "" "" "" $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_UPPSALA_GZ $CMM_OAF_SCILIFE_ILLUMINA_ALL_FAM $working_dir "scilife_illumina_uppsala" $CMM_SCILIFE_ILLUMINA_UPPSALA_SA_DB
