from .Statement import Statement
from . import Utils

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

    def __str__(self):
        return "Group Statement: " + self.name + "(" + self.value + "), containing " + str(len(self.content)) + " statements."

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise TypeError("Group statement doesn't take slices as keys.")
        elif isinstance(key, str):
            if key in self.index:
                if len(self.index[key]) == 1:
                    return self.content[self.index[key][0]]
                else:
                    return [self.content[i] for i in self.index[key]]
            else:
                raise IndexError("Cannot find entry " + str(key) + ".")
        elif isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Group statements only accept (name, value) as a tuple for group statement indexing")
            name, value = key
            if name in self.index:
                for iEntry in self.index[name]:
                    if self.content[iEntry].value == value:
                        return self.content[iEntry]
                raise IndexError("Group statement " + name + " with value " + value + " not found!")
            else:
                raise IndexError("Group statement " + name + " not found!")
        else:
            raise TypeError("Invalid argument Type!")

    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        ''' I libFile is a string array of each line of the liberty file
            I curLine is the current line for parsing this group statement
            I endLine is the end of the line, just for safety reason
            R nextLine is the next line that the potential parent parser should start to work on
        '''

        # endChar cannot be properly determined before the group statement is parsed
        sEndOfFile = len(libFile)
        # Sanity check
        if curChar >= sEndOfFile:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return len(libFile), -1
        
        self.startingPoint = curChar
        
        # The current part of the information should be the starting point of a group statement
        # Put a redundant check to be safe
        tString = libFile[curChar:] 
        indexFirstLeftBracket = tString.find('{')
        indexFirstSemicolon = tString.find(';')
        if indexFirstLeftBracket < indexFirstLeftBracket or indexFirstLeftBracket == -1 or indexFirstSemicolon == -1:
            if verbose:
                print("[ERROR]: Not a valid group statement on line " + str(curLine + 1) + ".")
            return sEndOfFile, -1
        
        sGroupStatementHeader = tString[:indexFirstLeftBracket]
        indexLeftParenthesis = sGroupStatementHeader.find('(')
        indexRightParenthesis = sGroupStatementHeader.find(')')
        self.name = sGroupStatementHeader[:indexLeftParenthesis].strip()
        self.value = sGroupStatementHeader[indexLeftParenthesis + 1 : indexRightParenthesis].strip()
        curChar = curChar + indexFirstLeftBracket + 1
        curChar, curLine = Utils.moveToNextStatement(libFile, curChar, sEndOfFile, curLine)

        # Parsing everything within this group statement
        while True:
            tString = libFile[curChar:]
            # Check if it is the end of the group statement
            if tString[0] == '}':
                curChar = curChar + 1
                break

            # Actual parsing starts here
            # All leading white spaces should have been removed before the classification started
            tStatement, endChar = Utils.classify(libFile, curChar)
            curChar, curLine = tStatement.parse(libFile, curChar, endChar, curLine, verbose)
            self.content.append(tStatement)
            tName = tStatement.name
            tLocation = len(self.content)-1
            if tName in self.index:
                self.index[tName].append(tLocation)
            else:
                self.index[tName] = [tLocation]
            curChar, curLine = Utils.moveToNextStatement(libFile, curChar, sEndOfFile, curLine)

        return curChar, curLine
    
    def write(self, libFile, indentationLevel, verbose = False):
        libFile = libFile + '\n' + Utils.indent(indentationLevel)
        libFile = libFile + self.name + ' (' + self.value + ') {'
        for tIterator in range(len(self.content)):
            libFile = self.content[tIterator].write(libFile, indentationLevel + 1, verbose)
        libFile = libFile + '\n' + Utils.indent(indentationLevel) + '}'
        return libFile