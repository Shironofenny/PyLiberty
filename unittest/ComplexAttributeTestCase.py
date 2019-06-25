import unittest
import os
import sys

# Import the base class for testing
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from src import ComplexAttribute
from src import InternalHelperUtilities as Utils

class ComplexAttributeTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_ca_parsing(self):
        sFilename = "ut_cas.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = Utils.readLibertyFile(tLibFile)
            sEndChar = len(sContent)
            sListOfStatements = [None] * 6
            tCurLine = 0
            tCurChar = 0
            while(tCurChar < sEndChar):
                sListOfStatements[tCurLine] = ComplexAttribute()
                tCurChar, tCurLine = sListOfStatements[tCurLine].parse(sContent, tCurChar, sEndChar, tCurLine)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndChar, tCurLine)

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        for i in range(6):
            print(sListOfStatements[i].name)
            print(sListOfStatements[i].value)
            print(sListOfStatements[i].comment)
        
if __name__ == "__main__":
    unittest.main()