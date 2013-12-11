import unittest
import os
from linkana.template import SafeTester
from linkana.template import RiskyTester
import linkana.settings as lka_settings


class SafeConnectorsTester(SafeTester):
    """ General template for safe "Connectors" modules testing """

    def __init__(self, test_name):
        SafeTester.__init__(self, test_name)

    def set_dir(self):
        self.working_dir = os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),
                                                                  'tmp'),
                                                     self.test_class),
                                        self.test_function)
        self.data_dir = os.path.join(os.path.join(os.path.dirname(__file__),
                                                  'data'),
                                     self.test_class)


class RiskyConnectorsTester(RiskyTester):
    """ General template for risky "Connectors" modules testing """

    def __init__(self, test_name):
        RiskyTester.__init__(self, test_name)

    def set_dir(self):
        self.working_dir = linkana_settings.linkana_WORKING_DIR
        self.data_dir = os.path.join(os.path.join(os.path.dirname(__file__),
                                                  'big_data'),
                                     self.test_class)
