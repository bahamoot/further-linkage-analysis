import os
import sys
import subprocess
import linkana.settings as lka_const

REF_DB_PREFIX = "/home/jessada/development/scilifelab/tools/annovar/humandb/hg19_snp137"

def check_output(cmd):
    p = subprocess.check_output(cmd, shell=True)
    if p == 1:
        raise Exception("Error found during execute command '%s' with error code %d" % (cmd, error))
    return p

def exec_sh(cmd):
    p = subprocess.call(cmd, shell=True)
    if p == 1:
        raise Exception("Error found during execute command '%s' with error code %d" % (cmd, p))
    return p

def summarize_annovar(chrom, begin_pos, end_pos, tabix_file, working_dir, out_prefix):
    cmd = []
    cmd.append(lka_const.WRAPPED_SUMMARIZE_ANNOVAR)
    cmd.append(chrom)
    cmd.append(begin_pos)
    cmd.append(end_pos)
    cmd.append(tabix_file)
    cmd.append(working_dir)
    cmd.append(out_prefix)
    return exec_sh(' '.join(cmd))

def get_pos(marker, ref_db_file):
    cmd = 'grep -P "' + marker + '\t" ' + ref_db_file
    record = check_output(cmd)
    return record.split('\t')[2]

def get_region(begin_marker, end_marker, ref_db_file):
    begin_pos = get_pos(begin_marker, ref_db_file)
    end_pos = get_pos(end_marker, ref_db_file)
    return begin_pos, end_pos

def get_region_chrom(chrom, begin_marker, end_marker, ref_db_prefix):
    return get_region(begin_marker, end_marker, ref_db_prefix+"_chr"+chrom+".txt")

def get_raw_vcf_gz_header(vcf_gz_file):
    cmd = 'zcat ' + vcf_gz_file + ' | grep "^#C"'
    return check_output(cmd)

