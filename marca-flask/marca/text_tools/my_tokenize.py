def __tokenize_text(inputText):
    __setCurrentToPath()
    sentences = sent_tokenize(inputText, newLineEndings=False, keepOriginalPunctuation=False)
    words = word_tokenize_list(sentences)
    return sentences, words


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


def paragraph_tokenize(strs, keepOriginalPunctuation=True):
    # TODO!
    print('returning sent_tokenize right now...')
    return sent_tokenize(strs)


# ===== region Word Tokenize ==================================================

"""Excludes some characters from starting word tokens"""
#_re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"
_re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\/\-,]" # added forward slash
"""Characters that cannot appear within words"""
#_re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
_re_non_word_chars = r"(?:[?!)\";}\]\/\*:@\'\({\[])" # added forward slash
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


def word_tokenize(strs):
    """Tokenize a string to split off punctuation other than periods"""
    return _re_word_tokenizer.findall(strs)

# END ===== region Word Tokenize

if __name__ == '__main__':
    txt = '''consumers and product manufacturers/service providers. Marketers should be very careful while identifying potential influencers that they can use for promoting their content. In addition to this, they need to be cognizant of the actual authentic followers vs. fake followers who may tweet about them. Fake followers may tend to adversely affect the brand equity. Similarly, other consumers of the brand/service should also beware of similar named Twitter handles that could be fake and may share misleading information. The studies combined together could be an easy way to identify the artificially boosted content by fake followers.

    5 CONCLUSION
    The media landscape has experienced a massive change with the arrival of internet and the recent advent of Web 3.0 and has influenced, in fact, completely changed the ways in which information communication takes place. The information explosion on social media platforms has made them a lot more engaging than stand alone communication platforms [89]. Social media platforms are utilized for discussions surrounding various domains including healthcare [90], internet of things [91], politics [92], amongst others. In the current scenario, the majority of people get to know about recent happenings around the globe through social media platforms. However, the content being shared may not always be from the right source or may not share the correct information. This makes these platforms vulnerable to propagation of misinformation. Thus, these platforms often make the source of several rumors and false content.
    '''

    print(paragraph_tokenize(txt))
    pause = True

