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
            # Initializing for better autocompletion
            tReturnObject = None
            # Case 1: it is a multi-level access
            if '.' in key:
                keyChain = key.split('.')
                tSearchObjects = [self]
                # Find a list of objects recursively
                for iKey in keyChain:
                    # Process to see if a specific name is in the group statement
                    # For better auto-completion, things are initialized (although unnecessary)
                    tGroup = None
                    tToken = None
                    if ('(' in iKey) and (')' in iKey):
                        tLeftP = iKey.find('(')
                        tRightP = iKey.find(')')
                        tGroup = iKey[:tLeftP].strip()
                        tToken = iKey[tLeftP + 1 : tRightP].strip()
                    else:
                        tGroup = iKey
                    tNextLevelObjects = []
                    for tSearchObject in tSearchObjects:

                        # Case 1: "valid_name" or "valid_group(valid_name)""
                        if tGroup in tSearchObject.index:
                            # Get the indexes of where the objects are found
                            tIndexes = tSearchObject.index[tGroup]
                            # Find if they match the token
                            for tIndex in tIndexes:
                                tExamineObject = tSearchObject.content[tIndex]
                                if tToken == None:
                                    tNextLevelObjects.append(tExamineObject)
                                else:
                                    if isinstance(tExamineObject, GroupStatement):
                                        if (tToken == '*') or (tExamineObject.value == tToken):
                                            tNextLevelObjects.append(tExamineObject)
                        
                        # Case 2: "*" or "*(valid_name)"
                        elif tGroup == '*':
                            if tToken == None:
                                tNextLevelObjects.append(tSearchObject.content)
                            else:
                                for tExamineObject in tSearchObject.content:
                                    if isinstance(tExamineObject, GroupStatement) and tExamineObject.value == tToken:
                                        tNextLevelObjects.append(tExaminObject)
                        
                        # Case 3: I don't know
                        else:
                            # Once nothing hits, return a new empty list
                            continue
                    # At the end of the loop, next level objects become current level objects
                    tSearchObjects = tNextLevelObjects

                # By the end, return the objects that are supposed to go through next level searching               
                tReturnObject = tSearchObjects

            # Case 2: it is a single level access
            else:
                tGroup = None
                tToken = None
                # It is a group statement
                if ('(' in key) and (')' in key):
                    tLeftP = key.find('(')
                    tRightP = key.find(')')
                    tGroup = key[:tLeftP]
                    tToken = key[tLeftP+1 : tRightP]
                else:
                    tGroup = key
                
                # Now, it is a properly parsed group statement with tGroup(tToken)
                # Case 1: "property_name" or "*""
                if tToken == None:
                    if tGroup == '*':
                        tReturnObject = self.content
                    else:
                        tReturnObject = [self.content[i] for i in self.index[tGroup]]
                # Case 2: "valid_group(valid_name)" or "valid_group(*)" or "*(valid_name)" or *(*)" 
                else:
                    tReturnObject = []
                    # "*(valid_name)" or "*(*)"
                    if tGroup == '*':
                        for iEntry in self.content:
                            if isinstance(iEntry, GroupStatement) and (tToken == '*' or iEntry.value == tToken):
                                tReturnObject.append(iEntry)
                    # "valid_group(valid_name)" or "valid_group(*)"
                    else:
                        tReturnIndex = self.index[tGroup]
                        if tToken == '*':
                            for iEntryIndex in tReturnIndex:
                                if isinstance(self.content[iEntryIndex], GroupStatement):
                                    tReturnObject.append(self.content[iEntryIndex])
                        else:
                            for iEntryIndex in tReturnIndex:
                                if isinstance(self.content[iEntryIndex], GroupStatement) and self.content[iEntryIndex].value == tToken:
                                    tReturnObject.append(self.content[iEntryIndex])
            return tReturnObject
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

        # Check if it is a top level group statement:
        if self._parentPath == '':
            self.path = '@'
        elif self._parentPath == '@':
            self.path = self.name + '(' + self.value + ')'
        else:
            self.path = self._parentPath + '.' + self.name + '(' + self.value + ')'
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
            tStatement.setParentPath(self.path)
            tStatement.parent = self
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