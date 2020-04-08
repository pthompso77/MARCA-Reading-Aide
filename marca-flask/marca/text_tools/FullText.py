"""
created 2020-04-07
fleshing out the FullText object details
"""


"""
updated 2020-02-07 to follow the model I created
then again 2020-04-07 :-D

Create FullText object
    identify paragraph sections (new line or sentence max)
      store as a list of integer tuples, where the integers correspond to the index of the words that start and end the section, with exclusive upper bound.
        e.g. the first paragraph is identified as [0, 100) and contains 100 words; the second paragraph as [100,200), which  begins with the 101st word in the text
    Tokenize sentence sections
    Tokenize words by sentence
      store as list of integers (as above)

Summarize/Highlight
    (words are compared as stemmed and lowercase, original text is not modified)
    for each section selected for highlighting, store the range as integer tuple with exclusive upper bound: [0:12)
    Store in tables
        FullText
        Paragraph_Delims
        Sentence_Delims
        Highlight_Delims
after insert into database, get textID and store in FullText object

"""



# full text reference (tokenized)
class FullText():
    ''' inputText must be a list of tokenized words from the original text,
    with the original formatting and punctuation

    '''
    def __init__(self, inputText, FulLText_ID=None):
        self.text = inputText
        self.paragraphList = getParagraphList(inputText)
        #store as a list of integer tuples, where the integers correspond to the index of the words that start and end the section, with exclusive upper bound.
            #e.g. the first paragraph is identified as [0, 100) and contains 100 words; the second paragraph as [100,200), which  begins with the 101st word in the text
        self.paragraphDelims = getDelims_Paragraph(self.paragraphList)
        # (currently, paragraph tokens start at the beginning of new lines, and sentences append whitepace to the end of tokens)
        #Tokenize sentence sections
        self.sentenceDelims = getDelims_Sentence(inputText)
        #Tokenize words by sentence
          #store as list of integers (as above)
        self.wordDelims = getDelims_Words(inputText)
        self.highlightDelims = self._getHightlightDelims()

    def _getHightlightDelims(self):
        from marca.text_tools import extractive_summarizer as summr
        from marca.text_tools import my_tokenize as tokenizer
        wordList = tokenizer.word_tokenize_withDelims(self.text, self.wordDelims)
        #: creating a dictionary for the word frequency table
        freq_table = summr.create_frequency_table(self.text, wordList=wordList)
        #: tokenizing the sentences
        sentences = tokenizer.sent_tokenize_withDelims(self.text, self.sentenceDelims)
        #: find weighted frequencies of sentences
        sentence_scores = summr.find_weighted_frequencies(sentences, freq_table)
        #: getting the threshold
        threshold = summr.getThresholdUsingSentenceWeights(sentence_scores)
        #: summarize and return the highlighted section delimeters
        highlightDelims = summr.assembleSummary_withDelims(sentences, self.sentenceDelims, sentence_scores, 1.0 * threshold)

        return highlightDelims



def getDelims_Words(inputText):
    '''
        Returns:
        a list of integer tuples, where the integers correspond to the index of
        the characters that start and end each word, with exclusive upper bound.
        [start, end)
    '''
    from nltk.tokenize import TreebankWordTokenizer
    word_tokenizer = TreebankWordTokenizer()
    wordDelims = []
    #previous_start = 0
    for this_start, this_end in word_tokenizer.span_tokenize(inputText):
        #delims = slice(previous_start, this_start)
        delims = slice(this_start, this_end)
        wordDelims.append(delims)
        #previous_start = this_start

    #: add the last slice (ending at the end of the inputText)
    #wordDelims.append(slice(previous_start, len(inputText)))
    #: remove the first slice [0:0]
    #wordDelims.pop(0)

    return wordDelims



def getDelims_Sentence(inputText):
    '''
        Returns:
        a list of integer tuples, where the integers correspond to the index of
        the words that start and end each sentence, with exclusive upper bound.
        [start, end)
    '''
    from nltk.tokenize import PunktSentenceTokenizer
    sent_tokenizer = PunktSentenceTokenizer()
    sentenceDelims = []
    previous_start = 0
    for this_start, this_end in sent_tokenizer.span_tokenize(inputText):
        delims = slice(previous_start, this_start)
        sentenceDelims.append(delims)
        previous_start = this_start

    #: add the last slice (ending at the end of the inputText)
    sentenceDelims.append(slice(previous_start, len(inputText)))
    #: remove the first slice [0:0]
    sentenceDelims.pop(0)
    return sentenceDelims



def getDelims_Paragraph(paragraphList):
    '''
        Returns:
        a list of integer tuples, where the integers correspond to the index of
        the words that start and end each paragraph, with exclusive upper bound.
        [start, end)
    '''
    paragraphDelims = []
    startDelim = 0
    for paragraph in paragraphList:
        paragraphLength = startDelim + len(paragraph)
        delims = slice(startDelim, paragraphLength)
        paragraphDelims.append(delims)

        startDelim = paragraphLength
    return paragraphDelims


def getParagraphList(inputText):
    from nltk.tokenize.texttiling import TextTilingTokenizer
    tiling_tokenizer = TextTilingTokenizer(demo_mode=False)
    paragraphList = tiling_tokenizer.tokenize(inputText)
    return paragraphList


def testLen(textStr, textList):
    ''' just testing - compares length of original text and paragraph tokens
    '''
    a = len(textStr)
    b = 0
    for t in textList:
        b += len(t)
    return a, b




def do_testing():
        ''' for testing this file '''
        with open('demo_text.txt', mode='r') as f:
            demotext1 = f.readlines()
        demotext = ''.join(demotext1)
        print(testLen(demotext, demotext1))

        ft = FullText(demotext)

        True


if __name__ == '__main__':
    do_testing()
