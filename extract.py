"""
For naive feature extraction from message text strings
"""

def findFormatting(message):
    """
    In: str message
    Look for markdown features, returns int flag
    0: no formatting 1: italics 2: bold 3: bold italics 4: ...
    """
    pass

def isolateNumber(message, separators):
    """
    In: str message,
    Processing occurs as follows:
    - Leading and trailing non-numerals are stripped
    - For non-numerals between number chunks, take the substring and see if it's allowed
    -- if in allowed separators or small gap, strip the substring out and
        concatenate numerals, record substring
    -- else, strip the substring and the numeral group according to
        which one is first in the message
    Returns tuple with
        (processed string, number of characters removed, intervening substrings)
    """
    pass

def convertNumber(numberRaw, target, bases):
    """
    In: int numberRaw, int target, int[] bases
    numberRaw in unknown base, target in decimal, checks which base conversion
    yields result closest to target. Converts to bases in bases.
    Returns tuple with (conversion result, base used)
    """
    pass
