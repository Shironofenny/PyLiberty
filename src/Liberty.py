import os
from . import Utils

from .GroupStatement import GroupStatement
from .SimpleAttribute import SimpleAttribute
from .ComplexAttribute import ComplexAttribute
from .Comment import Comment

class Liberty(GroupStatement):

    def __init__(self, i_filename = None):
        '''
        '''

        self.headComment = []
        self.tailComment = []
        if i_filename == None:
            GroupStatement.__init__(self)
        else:
            GroupStatement.__init__(self, i_filename)
            if os.path.isfile(i_filename):
                self.read(i_filename)

    def read(self, i_filename, verbose = False):
        if not os.path.isfile(i_filename):
            if verbose:
                print("[ERROR]: File " + i_filename + " doesn't exist!")
            return

        with open(i_filename, 'r') as libertyFile:
            sLibertyString = Utils.readLibertyFile(libertyFile)
            curLine = 0
            curChar = 0
            endChar = len(sLibertyString)
            curChar, curLine = Utils.moveToNextStatement(sLibertyString, curChar, endChar, curLine)
            sIsPostLibrary = False
            while curChar < endChar:
                tNextStatement, _ = Utils.classify(sLibertyString, curChar)
                if isinstance(tNextStatement, Comment) and not sIsPostLibrary:
                    self.headComment.append(tNextStatement)
                    curChar, curLine = tNextStatement.parse(sLibertyString, curChar, endChar, curLine, verbose)
                elif isinstance(tNextStatement, GroupStatement):
                    curChar, curLine = self.parse(sLibertyString, curChar, endChar, curLine, verbose)
                    sIsPostLibrary = True
                elif isinstance(tNextStatement, Comment) and sIsPostLibrary:
                    self.tailComment.append(tNextStatement)
                    curChar, curLine = tNextStatement.parse(sLibertyString, curChar, endChar, curLine, verbose)
                else:
                    if verbose:
                        print("[ERROR]: Extra statements found before library definition!")
                        return
                curChar, curLine = Utils.moveToNextStatement(sLibertyString, curChar, endChar, curLine)

    def getLibraryName(self):
        return self.value