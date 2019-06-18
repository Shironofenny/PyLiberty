import unittest
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from SimpleAttribute import SimpleAttribute

class SimpleAttributeTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_sa_parsing(self):
        sFilename = "ut_sas.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = tLibFile.readlines()
            sEndLine = len(sContent)
            sListOfStatements = [None] * sEndLine
            tCurLine = 0
            while(tCurLine < sEndLine):
                sListOfStatements[tCurLine] = SimpleAttribute()
                tCurLine = sListOfStatements[tCurLine].parse(sContent, tCurLine, sEndLine)
        
        self.assertEqual(sListOfStatements[0].name, 'comment')
        self.assertEqual(sListOfStatements[0].value, '" "')
        self.assertEqual(sListOfStatements[1].name, 'date')
        self.assertEqual(sListOfStatements[1].value, '"$Date: Jun 18"')
        self.assertEqual(sListOfStatements[2].name, 'version')
        self.assertEqual(sListOfStatements[2].value, '"1.0"')
        self.assertEqual(sListOfStatements[3].name, 'value')
        self.assertEqual(sListOfStatements[3].value, '1')
        self.assertEqual(sListOfStatements[4].name, 'invalid_name')
        self.assertEqual(sListOfStatements[4].value, 'invalid_value')
        self.assertEqual(sListOfStatements[5].name, 'invalid_name')
        self.assertEqual(sListOfStatements[5].value, 'invalid_value')
        self.assertEqual(sListOfStatements[6].name, 'invalid_name')
        self.assertEqual(sListOfStatements[6].value, 'invalid_value')
        self.assertEqual(sListOfStatements[7].name, 'invalid_name')
        self.assertEqual(sListOfStatements[7].value, 'invalid_value')
        self.assertEqual(sListOfStatements[8].name, 'index')
        self.assertEqual(sListOfStatements[8].value, '5')

if __name__ == "__main__":
    unittest.main()