import unittest
import os
import sys

# Import the base class for testing
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
from Comment import Comment

import Utils

class GroupStatementTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_gs_parsing(self):
        sFilename = "ut_minlib.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = Utils.readLibertyFile(tLibFile)
            sEndChar = len(sContent)
            sListOfStatements = [None] * 2
            tCurLine = 0
            tCurChar = 0
            tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndChar, tCurLine)
            i = 0
            while(tCurChar < sEndChar):
                sListOfStatements[i] = Utils.classify(sContent[tCurChar:])
                tCurChar, tCurLine = sListOfStatements[i].parse(sContent, tCurChar, sEndChar, tCurLine)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndChar, tCurLine)
                i = i+1

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        print(sListOfStatements[0].value)
        print(sListOfStatements[1].index)
        print(sListOfStatements[1].content)
        
if __name__ == "__main__":
    unittest.main()