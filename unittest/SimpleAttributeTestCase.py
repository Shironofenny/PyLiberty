import unittest
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from src import SimpleAttribute
from src import InternalHelperUtilities as Utils

class SimpleAttributeTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_sa_parsing(self):
        sFilename = "ut_sas.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = Utils.readLibertyFile(tLibFile)
            sEndChar = len(sContent)
            sListOfStatements = [None] * 9
            tCurLine = 0
            tCurChar = 0
            while(tCurChar < sEndChar):
                sListOfStatements[tCurLine] = SimpleAttribute()
                tCurChar, tCurLine = sListOfStatements[tCurLine].parse(sContent, tCurChar, sEndChar, tCurLine)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndChar, tCurLine)

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        
        self.assertEqual(sListOfStatements[0].name, 'comment')
        self.assertEqual(sListOfStatements[0].value, '" "')
        self.assertEqual(sListOfStatements[1].name, 'date')
        self.assertEqual(sListOfStatements[1].value, '"$Date: Jun 18"')
        self.assertEqual(sListOfStatements[1].comment, '/* With a regular line comment */')
        self.assertEqual(sListOfStatements[2].name, 'version')
        self.assertEqual(sListOfStatements[2].value, '"1.0"')
        self.assertEqual(sListOfStatements[2].comment, '/* With a strange line comment \n\n*/')
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