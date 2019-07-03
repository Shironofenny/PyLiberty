class Statement(object):

    def __init__(self, i_name = ''):
        self.name = i_name
        self.startingPoint = 0
        self.comment = None
        self.value = None
        self.path = ''
        self._parentPath = ''

    def __lt__(self, other):
        return self.startingPoint < other.startingPoint

    def __str__(self):
        # This class is supposed to be a semi-abstract class
        return '[WARNING]: Not a properly initialized statement!'

    def setParentPath(self, path):
        self._parentPath = path

    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        # Should not call this function!
        return curChar, curLine

    def write(self, libFile, indentationLevel, verbose = False):
        # Indentation level is not returned since every single statement should
        # return on the same indentation level it started with
        return libFile