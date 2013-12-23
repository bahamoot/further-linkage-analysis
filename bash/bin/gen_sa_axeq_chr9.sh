#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_gen_sa=$script_dir/script_gen_sa.sh
working_dir=$script_dir/tmp

$script_gen_sa "" "" "" $CMM_AXEQ_CHR9_ALL_PATIENTS_GZ $CMM_OAF_AXEQ_CHR9_ALL_FAM $working_dir "axeq_chr9" $CMM_AXEQ_CHR9_SA_DB
