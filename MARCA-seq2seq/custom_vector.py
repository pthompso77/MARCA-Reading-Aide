"""
02-15 1214pm
Takes a text input (article, book, etc)
using GloVe weights, assigns weights to each unique word in the vocabulary of text input
- (for any unknown words, it finds the closest word using cosine distance)

Returns an array where each row is a unique word, followed by n weights
- (where n is the size of the embedding dimension)
"""

def setup(pickle_filename = 'GloVe weights and index_dict.pickle'):
    alreadyPickled = __getPickle(pickle_filename)
    if alreadyPickled is None:
        import load_GloVe_weights, pickle
        gloVeEmeddingWeights, glove_index_dict = load_GloVe_weights.getGloVe()
        with open(pickle_filename, 'wb') as pickleWrite:
            pickle.dump((gloVeEmeddingWeights, glove_index_dict),pickleWrite)
    else:
        gloVeEmeddingWeights, glove_index_dict = alreadyPickled[0], alreadyPickled[1]
    return gloVeEmeddingWeights, glove_index_dict

def __getPickle(pickle_filename):
    pickleGot = None
    import pickle
    try:
        with open(pickle_filename, 'rb') as pickleRead:
            pickleGot = pickle.load(pickleRead)
    except:
        pass
    return pickleGot


""" 0. load custom text """
def loadText(textPath, readMode = 'r'):
    outputText = ''
    with open(textPath, readMode) as inputFile:
        outputText = inputFile.read()
    return outputText


""" 1. tokenize by sentence """
def __setCurrentToPath():
    import os,sys
    currentdir = os.path.dirname(__file__)
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)     
    
def __tokenize_text(inputText):
    __setCurrentToPath()    
    import my_tokenize
    sentences = my_tokenize.sent_tokenize(inputText, newLineEndings=False, keepOriginalPunctuation=False)
    words = my_tokenize.word_tokenize_list(sentences)
    return sentences, words
    
    



""" 2a. Build vocab_map and vocabCounter """
def __getVocabMap_and_Counter(tokenWords_list):
    import summarizerTools
    #vocab_count = summarizerTools._getVocabularyCount(sentences_list)
    vocab_count = summarizerTools._getVocabularyCount(tokenWords_list)
    vocab_map = summarizerTools._getVocabMap(vocab_count)
    return vocab_map, vocab_count

""" 2b. Index the words """
def __getDictsOfWordsAndIndices(vocab_map):
    import summarizerTools as st
    word2idx, idx2word = st.getDictsOfWordsAndIndices(vocab_map)
    return word2idx, idx2word    


""" N. copy word embedding values from GloVe"""
def __getWord2Glove(word2idx):
    """Maps the word in our custom vocab to the lowercase word in the GloVe vocab
    (is this necessary??)"""
    word2glove = {}
    for w in word2idx: # word2idx looks like : { 'the': 2, 'and': 3, ... }
        if w.startswith('#'):
            w = w[1:] # remove hash symbol
        isMatch_reg = w in glove_index_dict
        isMatch_lower = w.lower() in glove_index_dict
        if w in glove_index_dict:
            g = w
        elif w.lower() in glove_index_dict:
            g = w.lower()
            print(w, ':', g)
        else:
            continue
        word2glove[w] = g
    return word2glove


def __getCustomEmbedding(words2glove, index2word, gloVeEmeddingWeights, glove_index_dict):
    import load_GloVe_weights as glove
    return glove.copyGloveWeightsToCustomInputList(words2glove, index2word, gloVeEmeddingWeights, glove_index_dict)
"""CURRENT"""
    #todo = True


'''
OK, TODO

2. Index the words and get vocab/vocabcount
N. Copy word embedding values from GloVe

'''


if __name__ == '__main__':
    # set it up
    gloVeEmeddingWeights, glove_index_dict = setup()
    
    
    
    # 0. get text
    textpath = "/Users/lex/GitHub/MARCA sync with unca_server/public_html/MARCA-Reading-Aide/text-objects/moby_small.txt"
    txt = loadText(textpath)
    """ txt :: string
        'Call me Ishmael. Some years ago - never mind how long precisely -
        having little or no money in my purse, and nothing particular to
        interest me on shore, 
        ...
        when for scores on scores of miles you wade knee-deep among
        Tiger- lilies - what is the one charm wanting?'
    """
    
    # 1. tokenize
    txt_sent_tokens, txt_word_tokens = __tokenize_text(txt)
    """ txt_sent_tokens :: list
        0 = 'Call me Ishmael.'
        1 = ' Some years ago - never mind how long precisely - having little or no money in my purse, and no...
        ...
        45 = ' Go visit the Prairies in June,.'
        46 = ' when for scores on scores of miles you wade knee-deep among Tiger- lilies - what is the one ch...
        47 = ''
    """
    
    # 2. Index the words and get vocab/vocabcount
    #    a. get map and count
    #vocab_map, vocab_count = __getVocabMap_and_Counter(txt_sent_tokens)
    vocab_map, vocab_count = __getVocabMap_and_Counter(txt_word_tokens)
    """ vocab_map :: map
        <map object>
    """
    """ vocab_count :: dict; len=449
        - = 11
        American = 1
        And = 1
        Are = 1
        But = 4
        ...
        yet = 1
        yonder = 2
        you = 10
        your = 2
    """
    word2index, index2word = __getDictsOfWordsAndIndices(vocab_map)
    """ word2index :: dict; len=450
        - = 9
        <empty> = 0
        <eos> = 1
        American = 365
        ...
        yonder = 77
        you = 10
        your = 66
    """
    """ index2word :: dict; len=450
        0 = '<empty>'
        1 = '<eos>'
        2 = 'the'
        ...
        447 = 'what'
        448 = 'charm'
        449 = 'wanting?'
    """
    
    # N. copy word embedding values from GloVe
    words2glove = __getWord2Glove(word2index)
    """ words2glove :: dict; len=330
        - = '-'
        American = 'american'
        And = 'and'
        Are = 'are'
        But = 'but'
        ...
        yonder = 'yonder'
        you = 'you'
        your = 'your'
    """
    
    deleteMe_imAFiller=True
    
    
    """CURRENT"""
    custom_embedding = __getCustomEmbedding(index2word, gloVeEmeddingWeights, glove_index_dict)

