import os
import sys
from linkana.settings import REF_DB_FILE_PREFIX
from linkana.settings import BWA_VCF_TABIX_FILE
from linkana.settings import MOSAIK_VCF_TABIX_FILE
from linkana.settings import GLOBAL_WORKING_DIR
from linkana.settings import SA_OUT_DIR
from linkana.settings import CHR6_BEGIN_MARKER
from linkana.settings import CHR6_END_MARKER
from linkana.settings import CHR18_BEGIN_MARKER
from linkana.settings import CHR18_END_MARKER
from linkana.settings import CHR19_BEGIN_MARKER
from linkana.settings import CHR19_END_MARKER
from linkana.settings import FAMILY_FILE
from linkana.settings import XLS_OUT_DIR
from linkana.misc.script import get_region_chrom
from linkana.misc.script import summarize_annovar
from linkana.presentation.xls import MutationAnnotator
from linkana.db.manager import DBManager

def export_xls_chr6_bwa():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr6_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr6_bwa')
    export_xls('6',
               CHR6_BEGIN_MARKER,
               CHR6_END_MARKER,
               sa_tab_csv_file,
               BWA_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               )

def export_xls_chr18_bwa():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr18_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr18_bwa')
    export_xls('18',
               CHR18_BEGIN_MARKER,
               CHR18_END_MARKER,
               sa_tab_csv_file,
               BWA_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               )

def export_xls_chr19_bwa():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr19_bwa.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr19_bwa')
    export_xls('19',
               CHR19_BEGIN_MARKER,
               CHR19_END_MARKER,
               sa_tab_csv_file,
               BWA_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               )

def export_xls_chr6_mosaik():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr6_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr6_mosaik')
    export_xls('6',
               CHR6_BEGIN_MARKER,
               CHR6_END_MARKER,
               sa_tab_csv_file,
               MOSAIK_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               report_code='chr6_daniel',
               )

def export_xls_chr18_mosaik():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr18_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr18_mosaik')
    export_xls('18',
               CHR18_BEGIN_MARKER,
               CHR18_END_MARKER,
               sa_tab_csv_file,
               MOSAIK_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               report_code='chr18_daniel',
               )

def export_xls_chr19_mosaik():
    sa_tab_csv_file = os.path.join(SA_OUT_DIR, 'chr19_mosaik.tab.csv')
    xls_out_dir = os.path.join(XLS_OUT_DIR, 'chr19_mosaik')
    export_xls('19',
               CHR19_BEGIN_MARKER,
               CHR19_END_MARKER,
               sa_tab_csv_file,
               MOSAIK_VCF_TABIX_FILE,
               FAMILY_FILE,
               xls_out_dir,
               report_code='chr19_daniel',
               )

def export_xls(chrom,
               begin_marker,
               end_marker,
               sa_tab_csv_file,
               vcf_tabix_file,
               family_file,
               output_dir,
               report_code=None,
               ):
    (begin_pos, end_pos) = get_region_chrom(chrom,
                                            begin_marker,
                                            end_marker,
                                            REF_DB_FILE_PREFIX,
                                            )
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if report_code is None:
        report_code = 'chr' + str(chrom)
    ma = MutationAnnotator(report_code)
    db_man = DBManager()
    db_man.connect_summarize_annovar_db(sa_tab_csv_file)
    db_man.connect_vcf_db(vcf_tabix_file, chrom, begin_pos, end_pos)
    db_man.connect_family_db(family_file)
    ma.db_manager = db_man
    ma.export_xls(output_dir)

def generate_summarize_annovar_db_chr6_bwa():
    generate_summarize_annovar_db('6',
                                  CHR6_BEGIN_MARKER,
                                  CHR6_END_MARKER,
                                  BWA_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr6_bwa',
                                  )

def generate_summarize_annovar_db_chr18_bwa():
    generate_summarize_annovar_db('18',
                                  CHR18_BEGIN_MARKER,
                                  CHR18_END_MARKER,
                                  BWA_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr18_bwa',
                                  )

def generate_summarize_annovar_db_chr19_bwa():
    generate_summarize_annovar_db('19',
                                  CHR19_BEGIN_MARKER,
                                  CHR19_END_MARKER,
                                  BWA_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr19_bwa',
                                  )

def generate_summarize_annovar_db_chr6_mosaik():
    generate_summarize_annovar_db('6',
                                  CHR6_BEGIN_MARKER,
                                  CHR6_END_MARKER,
                                  MOSAIK_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr6_mosaik',
                                  )

def generate_summarize_annovar_db_chr18_mosaik():
    generate_summarize_annovar_db('18',
                                  CHR18_BEGIN_MARKER,
                                  CHR18_END_MARKER,
                                  MOSAIK_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr18_mosaik',
                                  )

def generate_summarize_annovar_db_chr19_mosaik():
    generate_summarize_annovar_db('19',
                                  CHR19_BEGIN_MARKER,
                                  CHR19_END_MARKER,
                                  MOSAIK_VCF_TABIX_FILE,
                                  GLOBAL_WORKING_DIR,
                                  'chr19_mosaik',
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

