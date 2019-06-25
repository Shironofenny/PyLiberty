from .Statement import Statement

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

    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        
        # Sanity check
        if curChar >= endChar:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endChar, -1
        
        self.startingPoint = curChar

        tString = libFile[curChar:]
        indexFirstColon = tString.find(':')
        indexFirstSemicolon = tString.find(';')
        indexFirstNewLine = tString.find('\n')
        
        # Assuming there is always a new line at the end of the file, if the file is read through Utils.readLibertyFile(fileObject)
        if indexFirstColon == -1 or indexFirstSemicolon == -1 or indexFirstColon > indexFirstNewLine or indexFirstSemicolon > indexFirstNewLine:
            if verbose:
                print("[ERROR]: Not a valid simple attribute on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
        else:
            self.name = tString[:indexFirstColon].strip(' ')
            self.value = tString[indexFirstColon + 1 : indexFirstSemicolon].strip(' ')
            tResidualString = tString[indexFirstSemicolon + 1 : indexFirstNewLine]
            if tResidualString.strip() != '':
                # Indicates there are following comments
                # And the comment may not end at the same line
                indexCommentStart = tString.find('/*')
                indexCommentEnd = tString.find('*/')
                if indexCommentStart == -1 or indexCommentEnd == -1:
                    if verbose:
                        print('[WARNING]: Not a valid comment after simple attribute on line ' + str(curLine + 1) + '.')
                else:
                    self.comment = tString[indexCommentStart:indexCommentEnd+2]
                    indexFirstNewLine = indexCommentEnd + tString[indexCommentEnd:].find('\n')
        curChar = curChar + indexFirstNewLine + 1
        # Advances line number by one
        curLine = curLine + 1

        return curChar, curLine