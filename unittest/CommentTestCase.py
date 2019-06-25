import unittest
import os
import sys

# Import the base class for testing
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

from src import Comment
from src import InternalHelperUtilities as Utils

class CommentTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_comment_parsing(self):
        sFilename = "ut_comment.lib"
        if os.path.isdir('unittest'):
            sFilename = "unittest/" + sFilename
        with open(sFilename, 'r') as tLibFile:
            sContent = Utils.readLibertyFile(tLibFile)
            sEndOfFile = len(sContent)
            sListOfStatements = [None] * 3
            tCurLine = 0
            tCurChar = 0
            tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndOfFile, tCurLine)
            i = 0
            tEndChar = sEndOfFile
            while(tCurChar < sEndOfFile):
                sListOfStatements[i], tEndChar = Utils.classify(sContent, tCurChar)
                tCurChar, tCurLine = sListOfStatements[i].parse(sContent, tCurChar, tEndChar, tCurLine, verbose=True)
                tCurChar, tCurLine = Utils.moveToNextStatement(sContent, tCurChar, sEndOfFile, tCurLine)
                i = i+1

        sSortedListOfStatements = sListOfStatements.copy()
        sSortedListOfStatements.sort()

        self.assertEqual(sSortedListOfStatements, sListOfStatements)
        for i in range(3):
            print(sListOfStatements[i].name)
            print(sListOfStatements[i].value)
            print(sListOfStatements[i].comment)
        
if __name__ == "__main__":
    unittest.main()