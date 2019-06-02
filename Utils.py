# Find the matched bracket
# I: parseString, the string where the bracket is to be found
#    the first character in the string must be the source parameter
# I: source, the source bracket that need to be matched
# I: target, the target bracket
# O: offsetVal, the amount of offset in this string where the matched
#    bracket is found. When it is a None, meaning no such matched
#    bracket is in the string
def findMatchedBracket(parseString, source = '{', target = '}'):
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