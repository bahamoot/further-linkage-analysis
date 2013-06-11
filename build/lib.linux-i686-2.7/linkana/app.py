import os
import sys
import linkana.settings as lka_const
from linkana.analysis.anal import Analyzer


def list_POTEC_gene_from_one_member(output_file=None):
    if output_file is not None:
        sys.stdout = open(output_file, 'w')

    out_fmt = '{gene}\t{chrom}\t{pos}\t{key}'
    analyzer = Analyzer()
    data_root = os.path.join(lka_const.PROJECT_ROOT,
                             'data')
    analyzer.load_one_member_data(data_root)
    snp_mgr = analyzer.db_mgr.snp_mgr
    for key in snp_mgr.keys():
        if snp_mgr[key].info.gene == 'POTEC':
            if snp_mgr[key].info.exonic_func != 'synonymous SNV':
                print out_fmt.format(gene=snp_mgr[key].info.gene,
                                     chrom=snp_mgr[key].info.chrom,
                                     pos=snp_mgr[key].info.start_pos,
                                     key=snp_mgr[key].pkey,
                                     )
    sys.stdout = sys.__stdout__
