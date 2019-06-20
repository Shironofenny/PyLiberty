from Statement import Statement

class SimpleAttribute(Statement):

    def __init__(self, i_name = ''):
        ''' Initialize everything that belongs to this class
        '''

        # The name in the parenthsis
        Statement.__init__(self, i_name)
        self.value = ' '
        pass

    def __str__(self):
        # This class is supposed to be a semi-abstract class
        return 'Simple Attribute: ' + self.name

    def parse(self, libFile, curLine, endLine, verbose = False):
        
        # Sanity check
        if curLine >= endLine:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endLine
        
        # Simple attributes occupies only one line
        self.startingLine = curLine
        self.endingLine = curLine
        
        tString = libFile[curLine]
        tOffsetColon = tString.find(':')
        tOffsetSemicolon = tString.find(';')

        if tOffsetColon == -1 or tOffsetSemicolon == -1:
            if verbose:
                print("[ERROR]: Not a valid simple attribute on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
        else:
            self.name = tString[:tOffsetColon].strip(' ')
            self.value = tString[tOffsetColon + 1 : tOffsetSemicolon].strip(' ')
        return curLine + 1
