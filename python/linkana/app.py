import os
import sys
from linkana.settings import REF_DB_FILE_PREFIX
from linkana.settings import UPPSALA_BWA_VCF_TABIX_FILE
from linkana.settings import UPPSALA_MOSAIK_VCF_TABIX_FILE
from linkana.settings import AXEQ_VCF_TABIX_FILE
from linkana.settings import SCILIFE_VCF_TABIX_FILE
from linkana.settings import GLOBAL_WORKING_DIR
from linkana.settings import SA_DB_DIR
from linkana.settings import CHR6_BEGIN_MARKER
from linkana.settings import CHR6_END_MARKER
from linkana.settings import CHR18_BEGIN_MARKER
from linkana.settings import CHR18_END_MARKER
from linkana.settings import CHR19_BEGIN_MARKER
from linkana.settings import CHR19_END_MARKER
from linkana.settings import UPPSALA_FAMILY_FILE
from linkana.settings import AXEQ_FAMILY_FILE
from linkana.settings import SCILIFE_FAMILY_FILE
from linkana.settings import XLS_OUT_DIR
from linkana.misc.script import get_region_chrom
from linkana.misc.script import summarize_annovar
from linkana.presentation.xls import MutationAnnotator
from linkana.db.manager import DBManager

def export_xls_chr6_uppsala_bwa():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr6_uppsala_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr6_uppsala_bwa')
    export_xls(sa_tab_csv_file,
               UPPSALA_BWA_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               chrom='6',
               begin_marker=CHR6_BEGIN_MARKER,
               end_marker=CHR6_END_MARKER,
               )

def export_xls_chr18_uppsala_bwa():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr18_uppsala_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr18_uppsala_bwa')
    export_xls(sa_tab_csv_file,
               UPPSALA_BWA_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               chrom='18',
               begin_marker=CHR18_BEGIN_MARKER,
               end_marker=CHR18_END_MARKER,
               )

def export_xls_chr19_uppsala_bwa():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr19_uppsala_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr19_uppsala_bwa')
    export_xls(sa_tab_csv_file,
               UPPSALA_BWA_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               chrom='19',
               begin_marker=CHR19_BEGIN_MARKER,
               end_marker=CHR19_END_MARKER,
               )

def export_xls_chr6_uppsala_mosaik():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr6_uppsala_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr6_uppsala_mosaik')
    export_xls(sa_tab_csv_file,
               UPPSALA_MOSAIK_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               report_code='chr6_daniel',
               chrom='6',
               begin_marker=CHR6_BEGIN_MARKER,
               end_marker=CHR6_END_MARKER,
               )

def export_xls_chr18_uppsala_mosaik():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr18_uppsala_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr18_uppsala_mosaik')
    export_xls(sa_tab_csv_file,
               UPPSALA_MOSAIK_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               report_code='chr18_daniel',
               chrom='18',
               begin_marker=CHR18_BEGIN_MARKER,
               end_marker=CHR18_END_MARKER,
               )

def export_xls_chr19_uppsala_mosaik():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr19_uppsala_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr19_uppsala_mosaik')
    export_xls(sa_tab_csv_file,
               UPPSALA_MOSAIK_VCF_TABIX_FILE,
               UPPSALA_FAMILY_FILE,
               xls_out_dir,
               report_code='chr19_daniel',
               chrom='19',
               begin_marker=CHR19_BEGIN_MARKER,
               end_marker=CHR19_END_MARKER,
               )

def export_xls_chr9_axeq():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'chr9_axeq.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr9_axeq')
    export_xls_pos(sa_tab_csv_file,
                   AXEQ_VCF_TABIX_FILE,
                   AXEQ_FAMILY_FILE,
                   xls_out_dir,
                   report_code='chr9_axeq',
                   chrom='9',
                   begin_pos='1',
                   end_pos='106000000',
                   )

def export_xls_scilife():
    sa_tab_csv_file = os.path.join(SA_DB_DIR, 'scilife.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'scilife')
    export_xls_pos(sa_tab_csv_file,
                   SCILIFE_VCF_TABIX_FILE,
                   SCILIFE_FAMILY_FILE,
                   xls_out_dir,
                   report_code='scilife_exome',
    #               chrom='1',
                   patient_codes=["Co441", "Co666", "Co771"],
                   )

def export_xls(sa_tab_csv_file,
               vcf_tabix_file,
               family_file,
               output_dir,
               report_code=None,
               chrom="",
               begin_marker="",
               end_marker="",
               ):
    (begin_pos, end_pos) = get_region_chrom(chrom,
                                            begin_marker,
                                            end_marker,
                                            REF_DB_FILE_PREFIX,
                                            )
    export_xls_pos(sa_tab_csv_file,
                   vcf_tabix_file,
                   family_file,
                   output_dir,
                   report_code=None,
                   chrom=chrom,
                   begin_pos=begin_pos,
                   end_pos=end_pos,
                   )

def export_xls_pos(sa_tab_csv_file,
                   vcf_tabix_file,
                   family_file,
                   output_dir,
                   report_code=None,
                   chrom="",
                   begin_pos="",
                   end_pos="",
                   patient_codes=None,
                   ):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if report_code is None:
        report_code = 'chr' + str(chrom)
    ma = MutationAnnotator(report_code)
    db_man = DBManager()
    db_man.connect_summarize_annovar_db(sa_tab_csv_file)
    db_man.connect_vcf_db(vcf_tabix_file, chrom, begin_pos, end_pos, patient_codes=patient_codes)
    db_man.connect_family_db(family_file)
    ma.db_manager = db_man
    ma.export_xls(output_dir)

def generate_summarize_annovar_db_chr6_uppsala_bwa():
    generate_summarize_annovar_db(UPPSALA_BWA_VCF_TABIX_FILE,
                                  'chr6_uppsala_bwa',
                                  '6',
                                  CHR6_BEGIN_MARKER,
                                  CHR6_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr18_uppsala_bwa():
    generate_summarize_annovar_db(UPPSALA_BWA_VCF_TABIX_FILE,
                                  'chr18_uppsala_bwa',
                                  '18',
                                  CHR18_BEGIN_MARKER,
                                  CHR18_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr19_uppsala_bwa():
    generate_summarize_annovar_db(UPPSALA_BWA_VCF_TABIX_FILE,
                                  'chr19_uppsala_bwa',
                                  '19',
                                  CHR19_BEGIN_MARKER,
                                  CHR19_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr6_uppsala_mosaik():
    generate_summarize_annovar_db(UPPSALA_MOSAIK_VCF_TABIX_FILE,
                                  'chr6_uppsala_mosaik',
                                  '6',
                                  CHR6_BEGIN_MARKER,
                                  CHR6_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr18_uppsala_mosaik():
    generate_summarize_annovar_db(UPPSALA_MOSAIK_VCF_TABIX_FILE,
                                  'chr18_uppsala_mosaik',
                                  '18',
                                  CHR18_BEGIN_MARKER,
                                  CHR18_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr19_uppsala_mosaik():
    generate_summarize_annovar_db(UPPSALA_MOSAIK_VCF_TABIX_FILE,
                                  'chr19_uppsala_mosaik',
                                  '19',
                                  CHR19_BEGIN_MARKER,
                                  CHR19_END_MARKER,
                                  )

def generate_summarize_annovar_db_chr9_axeq():
    summarize_annovar(AXEQ_VCF_TABIX_FILE,
                      GLOBAL_WORKING_DIR,
                      'chr9_axeq',
                      '9',
                      '1',
                      '106000000',
                      )

def generate_summarize_annovar_db_scilife():
    summarize_annovar(SCILIFE_VCF_TABIX_FILE,
                      GLOBAL_WORKING_DIR,
                      'scilife',
                      )

#def generate_summarize_annovar_db_pos(chrom,
#                                      begin_pos,
#                                      end_pos,
#                                      tabix_vcf_file,
#                                      working_dir,
#                                      out_prefix):
#    summarize_annovar(chrom,
#                      begin_pos,
#                      end_pos,
#                      tabix_vcf_file,
#                      working_dir,
#                      out_prefix)

def generate_summarize_annovar_db(tabix_vcf_file,
                                  out_prefix,
                                  chrom,
                                  begin_marker,
                                  end_marker,
                                  ):
    if chrom != "":
        (begin_pos, end_pos) = get_region_chrom(chrom,
                                                begin_marker,
                                                end_marker,
                                                REF_DB_FILE_PREFIX,
                                                )
    summarize_annovar(tabix_vcf_file,
                      GLOBAL_WORKING_DIR,
                      out_prefix,
                      chrom,
                      begin_pos,
                      end_pos,
                      )

