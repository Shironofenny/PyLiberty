from Statement import Statement

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
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endChar, -1

        tString = libFile[curChar:]
        indexCommentStart = tString.find('/*')
        if indexCommentStart != 0:
            if verbose:
                print("[ERROR]: Not a valid comment on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
            return endChar, -1
        
        self.name = 'comment'
        indexCommentEnd = tString.find('*/')
        self.value = tString[:indexCommentEnd + 2]
        tNrNewLines = self.value.count('\n')
        curLine = curLine + tNrNewLines
        curChar = curChar + indexCommentEnd + 2
        return curChar, curLine