"""
created 2020-02-02
fleshing out the Summary object details
"""

from moby import mobytext
# shorten for working with it
mobytext = mobytext[7000:10000]
print(mobytext,'\n\n==============\n\n\n')

"""
updated 2020-02-07 to follow the model I created

Create FullText object
Tokenize text submission
identify paragraph sections (new line or sentence max)
store as a list of integer tuples, where the integers correspond to the index of the words that start and end the section, with exclusive upper bound. 
e.g. the first paragraph is identified as [0, 100) and contains 100 words; the second paragraph as [100,200), which  begins with the 101st word in the text
identify sentence sections
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
UH OH — COOKIE? SESSIONID?

"""



# full text reference (tokenized)
class FullText():
    ''' inputText must be a list of tokenized words from the original text,
    with the original formatting and punctuation '''
    def __init__(self,inputText):
        self.text = inputText
        
def do_testing():
        ''' for testing this file '''
        ob = Summary(mobytext)
        t = ob.getText()
        print(*t,sep='\n')
        
if __name__ == '__main__':
    do_testing()
