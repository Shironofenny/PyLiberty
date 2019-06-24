import shlex

from .Statement import Statement

class ComplexAttribute(Statement):

    def __init__(self, i_name = ''):
        '''
        '''
        Statement.__init__(self, i_name)
        self.value = ''

    def __str__(self):
        return 'Complex Attribute: ' + self.name

    def parse(self, libFile, curChar, endChar, curLine, verbose=False):

        # Sanity check
        if curChar >= endChar:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endChar, -1

        # Complex attribute only occupies one line
        self.startingPoint = curChar

        tString = libFile[curChar:]
        indexParenthesisLeft = tString.find('(')
        indexParenthesisRight = tString.find(')')
        indexFirstSemicolon = tString.find(';')
        indexFirstNewLine = tString.find('\n')

        if indexParenthesisLeft == -1 or indexParenthesisRight == -1 or indexFirstSemicolon == -1 or indexParenthesisLeft > indexFirstNewLine or indexParenthesisRight > indexFirstNewLine:
            if verbose:
                print("[ERROR]: Not a valid complex attribute on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
        else:
            self.name = tString[:indexParenthesisLeft].strip(' ')
            tShlexObject = shlex.shlex(tString[indexParenthesisLeft + 1:indexParenthesisRight])
            tShlexObject.whitespace += ','
            self.value = list(tShlexObject)
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