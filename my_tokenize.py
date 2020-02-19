
"""
Tokenizer
"""

import re

def normalizeEndingPunctuation(str, newLineEndings=False, keepOriginalPunctuation=True):
    """Normalizes the punctuation at the end of sentences to vertical bar ('|'),
       setting it up to be split by that character
    """
    if (newLineEndings):
        sent_end_chars = ('?','?\s*', '!','!\s*','\n','\r', '.')
    else:
        # convert multiple new lines to a period (end of sentence)
        str = re.sub(r'\n\n+','.',str)
        # remove new lines, because most are not actually ends of sentences
        str = str.replace('\n',' ')
        sent_end_chars = ('?','?\s*', '!','!\s*','\r', '.')
    normalizingCharacter = '|'
    str2 = str
    for c in sent_end_chars:
        if (keepOriginalPunctuation):
            # add original sentence punctuation before the normalizing character
            normalizingCharacter = c + normalizingCharacter
        str2 = str2.replace(c,normalizingCharacter)
        # remove this sentence's punctuation, and reset the normalizing character
        normalizingCharacter = '|' 
    return str2

def sent_tokenize(strs, newLineEndings=False, keepOriginalPunctuation=True):
    strs2 = normalizeEndingPunctuation(strs, newLineEndings, keepOriginalPunctuation)
    strs2 = strs2.replace('.\s*','.')
    # split the sentences apart using the normalizing character
    return strs2.split('|')









# ===== region Word Tokenize ==================================================

"""Excludes some characters from starting word tokens"""
_re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"
"""Characters that cannot appear within words"""
_re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
"""Hyphen and ellipsis are multi-character punctuation"""
_re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"

myRe = r'''(
    %(MultiChar)s
    |
    (?=%(WordStart)s)\S+?  # Accept word characters until end is found
    (?= # Sequences marking a word's end
        \s|                                 # White-space
        $|                                  # End-of-string
        %(NonWord)s|%(MultiChar)s|          # Punctuation
        ,(?=$|\s|%(NonWord)s|%(MultiChar)s) # Comma if at end of word
    )
    |
    \S
)'''

_re_word_tokenizer = re.compile(
    myRe
    % {
        'NonWord': _re_non_word_chars,
        'MultiChar': _re_multi_char_punct,
        'WordStart': _re_word_start,
    },
    re.UNICODE | re.VERBOSE,
)


def word_tokenize(str):
    """Tokenize a string to split off punctuation other than periods"""
    return _re_word_tokenizer.findall(str)

# END ===== region Word Tokenize
