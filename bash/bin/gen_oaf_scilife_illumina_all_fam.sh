#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_gen_oaf=$script_dir/script_gen_oaf.sh

$script_gen_oaf $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ $CMM_HBVDB_SCILIFE_ILLUMINA_ALL_FAM $CMM_OAF_SCILIFE_ILLUMINA_ALL_FAM
