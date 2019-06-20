class Statement(object):

    def __init__(self, i_name = ''):
        self.name = i_name
        self.startingLine= 0
        self.endingLine = 0

    def __lt__(self, other):
        return self.startingLine < other.startingLine

    def __str__(self):
        # This class is supposed to be a semi-abstract class
        return '[WARNING]: Not a properly initialized statement!'

    def parse(self, libFile, curLine, endLine, verbose = False):
        # Should not call this function!
        pass

    def write(self, libFile):
        pass