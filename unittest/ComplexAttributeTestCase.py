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
            sEndOfFile = len(sContent)
            sListOfStatements = []
            tCurLine = 0
            tCurChar = 0
            tEndChar = 0
            while(tCurChar < sEndOfFile):
                tNextStatement, tEndChar = Utils.classify(sContent, tCurChar)
                sListOfStatements.append(tNextStatement)
                tCurChar, tCurLine = sListOfStatements[-1].parse(sContent, tCurChar, tEndChar, tCurLine, verbose=True)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndOfFile, tCurLine)

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        sWriteFile = ''
        indentationLevel = 0
        for i in range(7):
            print(sListOfStatements[i].name)
            print(sListOfStatements[i].value)
            print(sListOfStatements[i].comment)
            sWriteFile, indentationLevel = sListOfStatements[i].write(sWriteFile, indentationLevel)
        with open('ut_caswrite.lib', 'w') as sOutputFile:
            sOutputFile.write(sWriteFile)
        
if __name__ == "__main__":
    unittest.main()