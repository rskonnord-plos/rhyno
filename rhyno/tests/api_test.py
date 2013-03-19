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

    def test_ingest_zip(self):
        with self.assertRaises(Rhyno.ArticleAlreadyExists):
            self.r.ingest_zip(TEST_PACKAGE_FILENAME, verbose=True)
            
        self.r.ingest_zip(TEST_PACKAGE_FILENAME, force_reingest=True, verbose=True)
        

        
        
if __name__ == '__main__':
    unittest.main()
