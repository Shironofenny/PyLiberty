from .Statement import Statement
from .Comment import Comment
from .SimpleAttribute import SimpleAttribute
from .ComplexAttribute import ComplexAttribute
from .GroupStatement import GroupStatement

def indent(level, verbose = False):
    if not isinstance(level, int):
        if verbose:
            print("[WARNING]: Incorrect indentation level. Indentation level must be an integer!")
        return ''
    return ' ' * level * 2

def readLibertyFile(fileObject):
    ''' Read Liberty File
    I:  fileObject, the object to the file for parsing
    O:  content, a string of the entire file
    '''
    rString = fileObject.read()
    if rString[-1] != '\n':
        rString = rString + '\n'
    return rString

def moveToNextStatement(libFile, curChar, endOfFile, curLine):
    ''' Move to next statement
    I:  libFile, the liberty file in string
    I:  curChar, the index of the currently processed character
    I:  endOfFile, the end index of this entire liberty file
    I:  curLine, the line number where the current character is in
    O:  curChar, curLine
        After moving to the next statement, returned curChar is the
        character index of that in the liberty file, returned curLine
        is which line this character is at 
    '''
    while curChar < endOfFile:
        if not libFile[curChar].isspace():
            break
        else:
            if libFile[curChar] == '\n':
                curLine = curLine + 1
            curChar = curChar + 1
    return curChar, curLine
    
def findMatchedBracket(parseString, source = '{', target = '}'):
    '''
    Find the matched bracket
    I:  parseString, the string where the bracket is to be found
        the first character in the string must be the source parameter
    I:  source, the source bracket that need to be matched
    I:  target, the target bracket
    O:  offsetVal, the amount of offset in this string where the matched
        bracket is found. When it is a None, meaning no such matched
        bracket is in the string
    '''
    assert parseString[0] == source
    assert len(source) == 1
    assert len(target) == 1

    maxIndex = len(parseString)
    curIndex = 1 # Skip the first character, which is the source
    stackDepth = 1
    while curIndex < maxIndex:
        if parseString[curIndex] == target:
            stackDepth = stackDepth - 1
            if stackDepth == 0:
                return curIndex
        elif parseString[curIndex] == source:
            stackDepth = stackDepth + 1
        curIndex = curIndex + 1
    return None

def classify(libFile, curChar):
    '''
    Classify
    I:  libFile, The string that contains the whole liberty file
    I:  curChar, the current character being process, in this case, the statement classi-
        fication starts from this character
    O:  Statement instance, endChar: 
        Statement instance, an instance of the statement class that matches the pattern
        of the parseString; 
        endChar, the offset + 1 at the end of this statement. The extra 1 offset is added
        so that libFile[curChar, endChar] is the very statement for processing
    '''
    # Find the starting point of the parsing process
    parseString = libFile[curChar:]

    # Check if it is a comment
    indexCommentStart = parseString.find('/*')
    if indexCommentStart == 0:
        indexCommentEnd = parseString.find('*/')
        return Comment(), curChar + indexCommentEnd + 2

    # Check if it is a group statement, as group statements always have a '{' before ';'
    indexSemicolon = parseString.find(';')
    indexLeftBracket = parseString.find('{')
    if indexLeftBracket < indexSemicolon and indexSemicolon != -1 and indexLeftBracket != -1:
        # A group statement or a false one
        # endChar is 0 as anything can happen in a group statement, and simple, reliable detection doesn't exist
        # For instance, an earlier '}' may show up in a comment before the actual termination
        return GroupStatement(), 0
    
    # If there is a colon, that is a simple attribute
    indexColon = parseString.find(':')
    if indexColon != -1 and indexColon < indexSemicolon and indexSemicolon != -1:
        offsetNewLine = parseString[indexSemicolon:].find('\n')
        return SimpleAttribute(), curChar + indexSemicolon + offsetNewLine + 1
    
    # Check if it is a definition statement
    indexDefine = parseString.find('define')
    indexInclude = parseString.find('include_file')
    indexLeftParenthsis = parseString.find('(')
    if indexDefine < indexSemicolon and indexDefine != -1 and indexSemicolon != -1:
        # TODO Should be define statement
        return Statement(), 0

    if indexInclude < indexSemicolon and indexInclude != -1 and indexSemicolon != -1:
        # TODO Should be include statement
        return Statement(), 0
    
    if indexLeftParenthsis < indexSemicolon and indexLeftParenthsis != -1 and indexSemicolon != -1:
        offsetNewLine = parseString[indexSemicolon:].find('\n')
        return ComplexAttribute(), curChar + indexSemicolon + offsetNewLine + 1

    # If nothing matches, I don't know
    return Statement()
