class Statement(object):

    def __init__(self, i_name = ''):
        self.name = i_name
        self.startingPoint = 0
        self.comment = None
        self.value = None

    def __lt__(self, other):
        return self.startingPoint < other.startingPoint

    def __str__(self):
        # This class is supposed to be a semi-abstract class
        return '[WARNING]: Not a properly initialized statement!'

    def parse(self, libFile, curChar, endChar, curLine, verbose = False):
        # Should not call this function!
        pass

    def write(self, libFile):
        pass