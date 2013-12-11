import os
from linkana.db.connectors.test.template import SafeConnectorsTester
from linkana.db.connectors.familydb import FamilyDB


class TestFamilyDB(SafeConnectorsTester):

    def __init__(self, test_name):
        SafeConnectorsTester.__init__(self, test_name)

    def setUp(self):
        self.test_class = 'FamilyDB'

    def __create_db_instance(self):
        db = FamilyDB()
        return db

    def test_records_count(self):
        """ to check if all records are read """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        db.open_db(test_file)
        self.assertEqual(len(list(db.records)),
                         7,
                         'Incorrect number of records retrieved by FamilyDB')

    def test_records(self):
        """ to see if FamilyDB can correctly retrieve family informaiton """

        self.init_test(self.current_func_name)
        db = self.__create_db_instance()
        test_file = os.path.join(self.data_dir,
                                 self.current_func_name + '.txt')
        db.open_db(test_file)
        records = db.records
        test_record = records.next()
        self.assertEqual(test_record.family_code,
                         '8',
                         'Incorrect family code')
        self.assertEqual(test_record.type2,
                         'RECTAL',
                         'Incorrect family type2')
        self.assertEqual(test_record.type3,
                         '',
                         'Incorrect family type3')
        self.assertEqual(test_record.type4,
                         'CAFAM',
                         'Incorrect family type4')
        patient_codes = test_record.patient_codes
        self.assertEqual(len(patient_codes),
                         2,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[0],
                         'Co35',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[1],
                         'Co37',
                         'Incorrect patient code')
        records.next()
        test_record = records.next()
        self.assertEqual(test_record.family_code,
                         '348',
                         'Incorrect family code')
        self.assertEqual(test_record.type2,
                         '',
                         'Incorrect family type2')
        self.assertEqual(test_record.type3,
                         'COLON',
                         'Incorrect family type3')
        self.assertEqual(test_record.type4,
                         '',
                         'Incorrect family type4')
        patient_codes = test_record.patient_codes
        self.assertEqual(len(patient_codes),
                         2,
                         'Incorrect number of patient codes being read')
        self.assertEqual(patient_codes[0],
                         'Co846',
                         'Incorrect patient code')
        self.assertEqual(patient_codes[1],
                         'Co857',
                         'Incorrect patient code')

