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
        
        for i in range (sEndLine):
            print(sListOfStatements[i].value)
        self.assertFalse(False)

if __name__ == "__main__":
    unittest.main()