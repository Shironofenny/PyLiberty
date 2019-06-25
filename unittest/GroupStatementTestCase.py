import unittest
import os
import sys

# Import the base class for testing
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from src import Comment
from src import InternalHelperUtilities as Utils

class GroupStatementTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_gs_parsing(self):
        sFilename = "ut_minlib.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = Utils.readLibertyFile(tLibFile)
            sEndOfFile = len(sContent)
            sListOfStatements = [None] * 2
            tCurLine = 0
            tCurChar = 0
            tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndChar, tCurLine)
            i = 0
            while(tCurChar < sEndOfFile):
                sListOfStatements[i], tEndChar = Utils.classify(sContent, tCurChar)
                tCurChar, tCurLine = sListOfStatements[i].parse(sContent, tCurChar, tEndChar, tCurLine)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndOfFile, tCurLine)
                i = i+1

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        print(sListOfStatements[0].value)
        print(sListOfStatements[1].index)
        print(sListOfStatements[1].content)
        
if __name__ == "__main__":
    unittest.main()