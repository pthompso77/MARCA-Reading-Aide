
"""
Tokenizer
"""

import re

def normalizeEndingPunctuation(str):
    sent_end_chars = ('?','?\s*', '!','!\s*','\n','\r')
    # sent_end_chars = ('?','?\s*', '!','!\s*','\s*?','\s*!',)
    normChar = '.'
    str2 = str
    for c in sent_end_chars:
        str2 = str2.replace(c,normChar)
    return str2

def sent_tokenize(strs):
    strs2 = normalizeEndingPunctuation(strs)
    strs2 = strs2.replace('.\s*','.')
    return strs2.split('.')





_re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"
"""Excludes some characters from starting word tokens"""
_re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
"""Characters that cannot appear within words"""
_re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"
"""Hyphen and ellipsis are multi-character punctuation"""

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

"""
Main Tokenize Function
"""
def word_tokenize(str):
    """Tokenize a string to split off punctuation other than periods"""
    return _re_word_tokenizer.findall(str)
