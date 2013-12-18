#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_sa=$script_dir/script_build_sa.sh
working_dir=$script_dir/tmp

$script_build_sa "" "" "" $CMM_UPPSALA_50FAM_ALL_PATIENTS_GZ $CMM_OAF_UPPSALA_REALIGNED_ALL_50FAM $working_dir "uppsala_realigned_50fam" $CMM_UPPSALA_REALIGNED_50FAM_SA_DB
