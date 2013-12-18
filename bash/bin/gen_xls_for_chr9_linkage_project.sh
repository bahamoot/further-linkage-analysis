#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

script_build_xls=$script_dir/script_build_xls_for_chr9_linkage_family.sh
working_dir=$script_dir/tmp

AD_min_pos="101300000"
AD_max_pos="103100000"
AR_min_pos="92900000"
AR_max_pos="101400000"


$script_build_xls "9" $AD_min_pos $AD_max_pos "8AD" "Co35" "Co37"
$script_build_xls "9" $AD_min_pos $AD_max_pos "13AD" "Co95"
$script_build_xls "9" $AD_min_pos $AD_max_pos "296AD" "Co793" "Co876"
$script_build_xls "9" $AD_min_pos $AD_max_pos "350AD" "1104-03D"
$script_build_xls "9" $AD_min_pos $AD_max_pos "740AD" "Co1373" "602-05o" "Co1383"
$script_build_xls "9" $AD_min_pos $AD_max_pos "918AD" "134-06" "354-06"
$script_build_xls "9" $AR_min_pos $AR_max_pos "8AR" "Co35" "Co37"
$script_build_xls "9" $AR_min_pos $AR_max_pos "275AR" "Co1262" "Co618"
$script_build_xls "9" $AR_min_pos $AR_max_pos "478AR" "Co1274" "Co1207"
$script_build_xls "9" $AR_min_pos $AR_max_pos "740AR" "Co1373" "602-05o" "Co1383"
