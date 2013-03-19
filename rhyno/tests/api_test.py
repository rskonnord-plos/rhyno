from __future__ import absolute_import

import unittest

from ..api import Rhyno

API_HOST = 'https://webprod.plosjournals.org/api'
SHELL_HOST = 'iad-webprod-devstack01.int.plos.org'
TEST_PACKAGE_FILENAME = 'pone.0057000.zip'

class TestRhinoAPI(unittest.TestCase):
    def setUp(self):     
        self.r = Rhyno(API_HOST)
    
    def test_ingestible_get(self):
        ret = self.r.ingestible(verbose=True)
        print("INGESTIBLE DOIS: %s" % ret)
        
    def test_ingestible_post(self):
        
        
if __name__ == '__main__':
    unittest.main()
