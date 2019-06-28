import shlex

from .Statement import Statement
from . import Utils

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

        tString = libFile[curChar:endChar]
        indexParenthesisLeft = tString.find('(')
        indexParenthesisRight = tString.find(')')
        indexFirstSemicolon = tString.find(';')
        indexFirstNewLine = tString.find('\n')
        
        # Check if it is a multi-line statement
        while indexFirstNewLine != -1:
            indexPrevFirstNewLine = indexFirstNewLine - 1
            while tString[indexPrevFirstNewLine] == ' ' or tString[indexPrevFirstNewLine] == '\t':
                indexPrevFirstNewLine = indexPrevFirstNewLine - 1
            if tString[indexPrevFirstNewLine] == '\\':
                tString = tString[:indexPrevFirstNewLine] + ' ' * (indexFirstNewLine - indexPrevFirstNewLine + 1) + tString[indexFirstNewLine + 1:]
                indexFirstNewLine = tString.find('\n')
                curLine = curLine + 1
            else:
                break

        if indexParenthesisLeft == -1 or indexParenthesisRight == -1 or indexFirstSemicolon == -1:
            if verbose:
                print("[ERROR]: Not a valid complex attribute on line " + str(curLine + 1) + ".")
            self.name = 'invalid_name'
            self.value = 'invalid_value'
        else:
            self.name = tString[:indexParenthesisLeft].strip()
            tShlexObject = shlex.shlex(tString[indexParenthesisLeft + 1:indexParenthesisRight])
            tShlexObject.whitespace += ','
            tShlexObject.wordchars += '.'
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
        curChar = endChar
        # Advances line number by one
        curLine = curLine + 1

        return curChar, curLine

    def write(self, libFile, indentationLevel, verbose = False):
        listLength = len(self.value)
        if listLength == 0:
            if verbose:
                print("[Warning]: Complex attribute " + self.name + " has no value!")
                return libFile, indentationLevel
        else:
            libFile = libFile + '\n' + Utils.indent(indentationLevel, verbose)
            libFile = libFile + self.name + ' ('
            if listLength > 1 and len(self.value[0]) * listLength > 50:
                for tIterator in range(listLength):
                    if tIterator != 0:
                        libFile = libFile + ', '
                    libFile = libFile + '\\\n' + Utils.indent(indentationLevel + 1, verbose)
                    libFile = libFile + self.value[tIterator]
                libFile = libFile + '\\\n' + Utils.indent(indentationLevel, verbose) + ');'
            else:
                for tIterator in range(listLength):
                    libFile = libFile + self.value[tIterator]
                    if tIterator != listLength - 1:
                        libFile = libFile + ', '
                libFile = libFile + ');'
            if self.comment != None:
                libFile = libFile + ' ' + self.comment
        return libFile, indentationLevel