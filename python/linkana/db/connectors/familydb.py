from linkana.template import LinkAnaBase

FAMILY_DB_0_IDX_FAMILY_CODE = 0
FAMILY_DB_0_IDX_TYPE1 = 1
FAMILY_DB_0_IDX_TYPE2 = 2
FAMILY_DB_0_IDX_TYPE3 = 3
FAMILY_DB_0_IDX_TYPE4 = 4
FAMILY_DB_0_IDX_PATIENT_CODES = 5


class FamilyDBContentRecord(LinkAnaBase):
    """ to automatically parse Family data """

    def __init__(self, rec):
        if isinstance(rec, list):
            self.__rec = rec
        else:
            self.__rec = rec.split('\t')

    def get_raw_repr(self):
        return {'Family code': self.family_code,
                'Type2': self.type2,
                'Type3': self.type3,
                'Type4': self.type4,
                'Patients code': self.patient_codes,
                }

    @property
    def family_code(self):
        return self.__rec[FAMILY_DB_0_IDX_FAMILY_CODE]

    @property
    def type2(self):
        return self.__rec[FAMILY_DB_0_IDX_TYPE2]

    @property
    def type3(self):
        return self.__rec[FAMILY_DB_0_IDX_TYPE3]

    @property
    def type4(self):
        return self.__rec[FAMILY_DB_0_IDX_TYPE4]

    @property
    def patient_codes(self):
        return self.__rec[FAMILY_DB_0_IDX_PATIENT_CODES:len(self.__rec)+1]


class FamilyDB(LinkAnaBase):
    """ to connect to a file descript families and their members """

    def __init__(self):
        self.__family_db_file = None

    def get_raw_repr(self):
        return str({'database file': self.__family_db_file,
                    })

    def __open_db(self, family_db_file):
        self.__family_db_file = family_db_file

    def open_db(self, family_db_file):
        return self.__open_db(family_db_file)

    @property
    def header(self):
        return None

    @property
    def records(self):
        db_file = open(self.__family_db_file)
        for line in db_file:
            yield FamilyDBContentRecord(line.strip())
