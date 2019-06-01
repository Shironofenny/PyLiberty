import string

class GroupStatement:
    ''' A group statement is a named collectio of statements
    '''

    def __init__(self):
        index = {}
        content = {}
        pass

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

        sContinueParsing = True
        while sContinueParsing:
            tCurrentLine = libFile[curLine]
            # Check if it is the end of the group statement
            if "}" in tCurrentLine:
                sContinueParsing = False
                tEscapeChar = tCurrentLine.strip()
                if tEscapeChar == "}":
                    break
                else:
                    tCurrentLine = tCurrentLine.rstrip("}")
        
            # Actual parsing starts here