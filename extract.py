"""
For naive feature extraction from message text strings
"""
import re

async def findFormatting(message):
    """
    In: str message
    Look for markdown features, returns int flag
    0: no formatting 1: italics 2: bold 3: bold italics 4: ...
    """
    pass

async def findBase(numberRaw, target, bases):
    """
    In: int numberRaw, int target, int[] bases
    numberRaw in unknown base, target in decimal, checks which base conversion
    yields result closest to target. Converts to bases in bases.
    Returns tuple with (conversion result, base used)
    """
    pass

async def stripOutside(message, gapSize):
    """
    Strips away from first cluster of numbers found (numbers considered not
    together if separated by more than gapSize non-numbers)
    """
    numbers = set(["0","1","2","3","4","5","6","7","8","9"])
    # get index of first and last numeral
    iF = 0
    iL = 0
    started = False # whether the numbers have started
    count = 0
    i = 0
    print("Message:", message)
    for char in message:
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
        i += 1
    # slice the string accordingly
    print(f"Slicing from {iF} to {iL+1}")
    message = message[iF:iL+1]
    return message

async def findNumber(message, separators=[",", " ", "."]):
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
    message = await stripOutside(message, 3)
    message = re.sub("\D", "", message)
    number = int(message) if len(message) > 0 else -1
    print("Result:", number)
    return number
