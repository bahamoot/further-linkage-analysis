#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_gen_oaf=$script_dir/script_gen_oaf.sh

$script_gen_oaf $CMM_AXEQ_CHR9_ALL_PATIENTS_GZ $CMM_HBVDB_AXEQ_CHR9_ALL_FAM $CMM_OAF_AXEQ_CHR9_ALL_FAM

