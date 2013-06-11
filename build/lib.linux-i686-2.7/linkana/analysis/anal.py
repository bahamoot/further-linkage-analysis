import glob
import os
import re
import csv
import linkana.settings as lka_const
from linkana.template import LinkAnaBase
from linkana.db.manager import DBManager
from linkana.db.manager import SNPRecord


FAMILY_DIR_PATTERN = r"""family(?P<fam_code>[\d]*)_chr(?P<chrom>[\d]*)"""
MEMBER_FILE_PATTERN = r"""(?P<member_code>[\w-]*).*.csv"""
class Analyzer(LinkAnaBase):

    def __init__(self):
        LinkAnaBase.__init__(self)
        self.db_mgr = DBManager()

    def parse_dir_path(self, dir_path):
        if os.path.isdir(dir_path):
            m = re.match(FAMILY_DIR_PATTERN, os.path.basename(dir_path))
            return {'dir_path' : dir_path,
                    'fam_code' : m.group('fam_code'),
                    'chrom' : m.group('chrom'),
                    }
        else:
            return None

    def get_dirs_list(self, data_root):
        dirs_list = []
        os.chdir(data_root)
        for dir_name in glob.glob('*'):
            dir_info = self.parse_dir_path(os.path.join(data_root,
                                                        dir_name)
                                           )
            if dir_info is not None:
                dirs_list.append(dir_info)
        return dirs_list

    def parse_file_name(self, file_name):
        if re.match(r""".*common.*""", file_name) is not None:
            return None
        elif re.match(r""".*.xls""", file_name) is not None:
            return None
        else:
            m = re.match(MEMBER_FILE_PATTERN, file_name)
            return {'file_name' : file_name,
                    'member_code' : m.group('member_code'),
                    }

    def get_files_list(self, family_dir):
        files_list = []
        os.chdir(family_dir)
        for file_name in glob.glob('*'):
            file_info = self.parse_file_name(file_name)
            if file_info is not None:
                file_info['file_path'] = os.path.join(family_dir,
                                                      file_info['file_name'])
                files_list.append(file_info)
        return files_list

    def load_csv2db(self, csv_file):
        csv_records = csv.reader(open(csv_file, 'rb'), delimiter='\t')
        for csv_record in csv_records:
            snp_record = SNPRecord(csv_record)
            if snp_record.gene != 'Gene':
                self.db_mgr.add_mutation(snp_record)

    def load_one_member_data(self, data_root):
        dirs_list = self.get_dirs_list(data_root)
        for dir_info in dirs_list:
            files_list = self.get_files_list(dir_info['dir_path'])
            self.load_csv2db(files_list[0]['file_path'])
