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
                    self.path = ''
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
    
    def write(self, filename, verbose = False):
        if os.path.isfile(filename):
            if verbose:
                print("[WARNING]: File " + filename + " exists. Its content will be overwritten!")
        
        if not isinstance(filename, str):
            if verbose:
                print("[ERROR]: Input argument \"filename\" must be a valid string!")
        with open(filename, 'w') as libFile:
            sLibString = ''
            if len(self.headComment) > 0:
                for tIterator in range(len(self.headComment)):
                    sLibString = self.headComment[tIterator].write(sLibString, 0, verbose)
            sLibString = GroupStatement.write(self, sLibString, 0, verbose)
            if len(self.headComment) > 0:
                for tIterator in range(len(self.headComment)):
                    sLibString = self.headComment[tIterator].write(sLibString, 0, verbose)
            # Remove the initial new line
            if sLibString[0] == '\n':
                sLibString = sLibString[1:]
            libFile.write(sLibString)