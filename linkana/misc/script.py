import os
import sys
import subprocess
import linkana.settings as lka_const

def exec_sh(cmd):
    p = subprocess.Popen(cmd, shell=True)
    error = p.wait()
    if error:
        raise Exception("Error found during execute command '%s' with error code %d" % (cmd, error))

def summarize_annovar(chrom, begin_marker, end_marker, tabix_file, working_dir, out_prefix):
    cmd = []
    cmd.append(lka_const.WRAPPED_SUMMARIZE_ANNOVAR)
    cmd.append(chrom)
    cmd.append(begin_marker)
    cmd.append(end_marker)
    cmd.append(tabix_file)
    cmd.append(working_dir)
    cmd.append(out_prefix)
    return exec_sh(' '.join(cmd))

#def list_POTEC_gene_from_one_member(output_file=None):
#    if output_file is not None:
#        sys.stdout = open(output_file, 'w')
#
#    out_fmt = '{gene}\t{chrom}\t{pos}\t{key}'
#    analyzer = Analyzer()
#    data_root = os.path.join(lka_const.PROJECT_ROOT,
#                             'data')
#    analyzer.load_one_member_data(data_root)
#    snp_mgr = analyzer.db_mgr.snp_mgr
#    for key in snp_mgr.keys():
#        if snp_mgr[key].info.gene == 'POTEC':
#            if snp_mgr[key].info.exonic_func != 'synonymous SNV':
#                print out_fmt.format(gene=snp_mgr[key].info.gene,
#                                     chrom=snp_mgr[key].info.chrom,
#                                     pos=snp_mgr[key].info.start_pos,
#                                     key=snp_mgr[key].pkey,
#                                     )
#    sys.stdout = sys.__stdout__
