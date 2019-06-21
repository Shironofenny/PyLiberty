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
    
    def parse(self, libFile, curLine, endLine, verbose = False):
        
        # Sanity check
        if curLine >= endLine:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endLine

        tString = libFile[curLine]
        indexCommentStart = tString.find('/*')
        if indexCommentStart == -1:
            if verbose:
                print("[ERROR]: Not a valid comment on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
            return curLine + 1
        
        self.name = 'comment'
        self.value = []

        self.value.append(tString)
        indexCommentEnd = tString.find('*/')
        while indexCommentEnd == -1:
            curLine = curLine + 1
            tString = libFile[curLine]
            indexCommentEnd = tString.find('*/')
            self.value.append(tString)
        return curLine + 1