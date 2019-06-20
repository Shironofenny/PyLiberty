from Statement import Statement

class GroupStatement(Statement):
    ''' A group statement is a named collection of statements
    '''

    def __init__(self, i_name = ''):
        ''' Initialize everything that belongs to this class
        '''

        # The name in the parenthsis
        Statement.__init__(self, i_name)
        # A quick index as a helper class.
        # The index is organized as: "statement_name" : "statement_type"
        # "statement_name" is the actual name of the statement
        # "statement_type" is one of: "group", "attribute_simple", "attribute_complex", and "definition"
        self.index = {}
        # The actual statements in this group statement
        self.content = []
        # The comments found within the lines of the group statement
        # Each element in this list is a tuple of (lineNumber, commentString)
        comments = []

    def parse(self, libFile, curLine, endLine):
        ''' I libFile is a string array of each line of the liberty file
            I curLine is the current line for parsing this group statement
            I endLine is the end of the line, just for safety reason
            R nextLine is the next line that the potential parent parser should start to work on
        '''
        # Sanity check
        if curLine >= endLine:
            print("[ERROR]: Starting beyond the end of the file. Something must has gone wrong!")
            return endLine
        
        self.lineStart = curLine
        sContinueParsing = True
        while sContinueParsing:
            tCurrentLine = libFile[curLine]
            # Check if it is the end of the group statement
            if '}' in tCurrentLine:
                sContinueParsing = False
                tEscapeChar = tCurrentLine.strip()
                if tEscapeChar == '}':
                    break
                else:
                    tCurrentLine = tCurrentLine.rstrip('}')
        
            # Actual parsing starts here
            # If it is a new group statement
            if '{' in tCurrentLine:
                tGroupName = tCurrentLine[:tCurrentLine.find('(')].strip()
