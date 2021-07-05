"""
For naive feature extraction from message text strings
"""
import re

def findFormatting(message):
    """
    In: str message
    Look for markdown features, returns int flag
    0: no formatting 1: italics 2: bold 3: bold italics 4: ...
    """
    pass

def findBase(numberRaw, target, bases):
    """
    In: int numberRaw, int target, int[] bases
    numberRaw in unknown base, target in decimal, checks which base conversion
    yields result closest to target. Converts to bases in bases.
    Returns tuple with (conversion result, base used)
    """
    pass

def stripOutside(message, gapSize):
    """
    Strips away from first cluster of numbers found (numbers considered not
    together if separated by more than gapSize non-numbers)
    """
    numbers = {"0","1","2","3","4","5","6","7","8","9"}
    # get index of first and last numeral
    iF = None
    iL = None
    started = False # whether the numbers have started
    count = 0
    for i, char in enumerate(message):
        if char in numbers:
            if not started:
                iF = i
            else:
                iL = i
            started = True
            count = 0
        elif started:
            count += 1
        if count > gapSize:
            break
    # slice the string accordingly
    message = message[iF:iL+1]
    return message

def findNumber(message, separators=[",", " ", "."]):
    """
    In: str message, str[] separators
    Processing occurs as follows:
    - Isolate the first group of numbers
    - Strip non-number characters

    TO IMPLEMENT LATER:
    - For non-numerals between number chunks, take the substring and see if it's allowed
    -- if in allowed separators, strip the substring out and
        concatenate numerals, record substring
    -- else, strip the substring and the numeral group according to
        which one is first in the message
    Returns tuple with
        (int, number of characters removed, intervening substrings)
    """
    message = stripOutside(message, 3)
    number = int( re.sub("\D", "", message) )
    return number
