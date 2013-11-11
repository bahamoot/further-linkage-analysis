#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_sa=$script_dir/script_build_sa.sh
working_dir=$script_dir/tmp

#---------- arguments --------------
out_prefix=$6

out_file=$working_dir/$out_prefix".tab.csv"
#---------- arguments --------------

#---------- vcf2avdb --------------
tmp_avdb=$working_dir/$out_prefix"_tmp_avdb"
avdb_out=$working_dir/$out_prefix".avdb"

$script_build_sa "" "" "" $CMM_SCILIFE_ILLUMINA_ALL_PATIENTS_MANS_GZ $working_dir "scilife" $CMM_SCILIFE_ILLUMINA_SA_DB
