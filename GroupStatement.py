from Statement import Statement
import Utils

class GroupStatement(Statement):
    ''' A group statement is a named collection of statements
    '''

    def __init__(self, i_name = ''):
        ''' Initialize everything that belongs to this class
        '''

        # The name in the parenthsis
        Statement.__init__(self, i_name)
        # A quick index as a helper class.
        # The index is organized as: "statement_name" : List(locations in content array)
        # "statement_name" is the actual name of the statement
        # List(location in content array) is a list that points you to where the statements with the
        # corresponding name can be found
        self.index = {}
        # The actual statements in this group statement
        self.content = []

    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        ''' I libFile is a string array of each line of the liberty file
            I curLine is the current line for parsing this group statement
            I endLine is the end of the line, just for safety reason
            R nextLine is the next line that the potential parent parser should start to work on
        '''
        # Sanity check
        if curChar >= endChar:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endChar, -1
        
        self.startingPoint = curChar
        
        # The current part of the information should be the starting point of a group statement
        # Put a redundant check to be safe
        tString = libFile[curChar:]
        indexFirstLeftBracket = tString.find('{')
        indexFirstSemicolon = tString.find(';')
        if indexFirstLeftBracket < indexFirstLeftBracket or indexFirstLeftBracket == -1 or indexFirstSemicolon == -1:
            if verbose:
                print("[ERROR]: Not a valid group statement on line " + str(curLine + 1) + ".")
            return endChar, -1
        
        sGroupStatementHeader = tString[:indexFirstLeftBracket]
        indexLeftParenthesis = sGroupStatementHeader.find('(')
        indexRightParenthesis = sGroupStatementHeader.find(')')
        self.name = sGroupStatementHeader[:indexLeftParenthesis].strip()
        self.value = sGroupStatementHeader[indexLeftParenthesis + 1 : indexRightParenthesis].strip()
        curChar = curChar + indexFirstLeftBracket + 1
        curChar, curLine = Utils.moveToNextStatement(libFile, curChar, endChar, curLine)

        # Parsing everything within this group statement
        sStatementCounter = 0
        while True:
            tString = libFile[curChar:]
            # Check if it is the end of the group statement
            if tString[0] == '}':
                curChar = curChar + 1
                break

            # Actual parsing starts here
            # All leading white spaces should have been removed before the classification started
            tStatement = Utils.classify(tString)
            curChar, curLine = tStatement.parse(libFile, curChar, endChar, curLine, verbose)
            self.content.append(tStatement)
            tName = tStatement.name
            tLocation = len(self.content)-1
            if tName in self.index:
                self.index[tName].append(tLocation)
            else:
                self.index[tName] = [tLocation]
            curChar, curLine = Utils.moveToNextStatement(libFile, curChar, endChar, curLine)

        return curChar, curLine