from .Statement import Statement
from . import Utils

class Comment(Statement):

    def __init__(self, i_name = ''):
        ''' Initialize everything that belongs to this class
        '''

        # The name in the parenthsis
        Statement.__init__(self, i_name)
        self.value = ' '
        pass

    def __str__(self):
        # This class is supposed to be a semi-abstract class
        return 'Comments of ' + str(self.endingLine - self.startingLine) + ' lines long.'
    
    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        
        # Sanity check
        if curChar >= endChar:
            print("[ERROR]: Starting beyond the end of the statement. Something must has gone wrong!")
            return endChar, -1

        tString = libFile[curChar:]
        indexCommentStart = tString.find('/*')
        if indexCommentStart != 0:
            if verbose:
                print("[ERROR]: Not a valid comment on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
            return endChar, -1
        
        self.startingPoint = curChar
        # "static_comment_string" is used as "comment" sometimes is a valid simple attribute for certain cases
        self.name = 'static_comment_string'
        indexCommentEnd = tString.find('*/')
        if indexCommentEnd != endChar - curChar - 2:
            if verbose:
                print("[WARNING]: Comment line extends beyond the end of the statement")
        self.value = tString[:indexCommentEnd + 2]
        tNrNewLines = self.value.count('\n')
        curLine = curLine + tNrNewLines
        curChar = curChar + indexCommentEnd + 2
        return curChar, curLine
    
    def write(self, libFile, indentationLevel, verbose = False):
        libFile = libFile + '\n' + Utils.indent(indentationLevel)
        libFile = libFile + self.value
        return libFile