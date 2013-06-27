import os
import sys
from linkana.settings import REF_DB_FILE_PREFIX
from linkana.settings import BWA_VCF_TABIX_FILE
from linkana.settings import GLOBAL_WORKING_DIR
from linkana.settings import SA_OUT_DIR
from linkana.settings import CHR18_BEGIN_MARKER
from linkana.settings import CHR18_END_MARKER
from linkana.misc.script import get_region_chrom
from linkana.misc.script import summarize_annovar

def generate_summarize_annovar_db_chr18_bwa():
    generate_summarize_annovar_db('18',
                                  CHR18_BEGIN_MARKER,
                                  CHR18_END_MARKER,
                                  BWA_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr18_bwa',
                                  )


def generate_summarize_annovar_db(chrom,
                                  begin_marker,
                                  end_marker,
                                  tabix_vcf_file,
                                  working_dir,
                                  out_prefix):
    (begin_pos, end_pos) = get_region_chrom(chrom,
                                            begin_marker,
                                            end_marker,
                                            REF_DB_FILE_PREFIX,
                                            )
    summarize_annovar(chrom,
                      begin_pos,
                      end_pos,
                      tabix_vcf_file,
                      working_dir,
                      out_prefix)

