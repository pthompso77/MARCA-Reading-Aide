import pickle
from collections import Counter
from itertools import chain

"""
preceding steps:
...
...
...

"""

def getPickledTuple(just100 = False):
    """
    02-12 448am
    Get the pickled tuple of 1,000,000 (Headlines, Keywords [None right now], and Descriptions)
    (takes about 10 seconds)
    """
    filenameOfPickledTuple = 'jlist_100_tuple.pickle' if just100 else 'jlist_full_tuple.pkl'
    readBinaryMode = 'rb'
    with open(filenameOfPickledTuple, readBinaryMode) as pickledFile:
        heads_keys_descs = pickle.load(pickledFile)
    print('success, now you have heads_keys_descs')
    return heads_keys_descs
        
        
def _getVocabularyCount(inputListOfWords):
    """
    02-12 513am
    Get the count of the vocabulary in this text
    inputListOfWords is a list of strings (tokenized by word)
    """
    # TODO RETURN HERE AND TOKENIZE WORDS INSTEAD OF SPLIT!!!
    
    vocabCount = Counter(words for textStrings in inputListOfWords for words in textStrings.split()) 
    return vocabCount


def _getVocabMap(vocabularyCounter):
    """
    02-12 642am
    Generate and return a map of words sorted by most frequent
    """
    # 1. sort the inputList based on vocabularyCounter (descending)
    sortDecendingFun = lambda x : -x[1]
    sortedList = sorted(vocabularyCounter.items(), key=sortDecendingFun)
    
    # 2. map it by first value (word as key)
    firstValueMapFun = lambda x : x[0]
    return map(firstValueMapFun,  sortedList)
    


def getVocabularyAndCountFromTuple(heads_keys_descs):
    """
    02-12 649am
    Returns a tuple of (vocabulary map sorted by most frequent, count of words)
    """
    # make a list of headings and descriptions (minus the keywords)
    '''
    !! RETURN HERE BECAUSE THIS WON'T WORK, IT NEEDS TOKENIZED WORDS, NOT SENTENCES
    '''
    headsAndDescs = heads_keys_descs[0]+heads_keys_descs[2]
    wordCounts = _getVocabularyCount(headsAndDescs)
    vocabMap = _getVocabMap(wordCounts)
    return vocabMap, wordCounts


def getDictsOfWordsAndIndices(vocabMap, wordCounts=None):
    empty = 0 # RNN mask of no data
    eos = 1  # end of sentence
    start_idx = eos+1 # first real word   
    
    # Word:Index
    word2idx = dict((word, idx+start_idx) for idx,word in enumerate(vocabMap))
    word2idx['<empty>'] = empty
    word2idx['<eos>'] = eos
    
    # Index:Word
    idx2word = dict((idx,word) for word,idx in word2idx.items())

    return word2idx, idx2word    


"""
NOW TIME FOR WORD EMBEDDING WITH GLOVE
"""



"""
embedding_dimension = 100
vocabulary_size = 40000
filename = 'glove.6B.{}d.txt'.format(embedding_dimension)
"""

def getOrVerifyGloVeExists(filename, embedding_dimension = 100):
    """
    I think we only want to do this if the dataset doesn't 
    already exist in /Users/lex/.keras/datasets
    """
    import keras
    fname = 'glove.6B.%dd.txt'%embedding_dimension
    import os
    datadir_base = os.path.expanduser(os.path.join('~', '.keras'))
    if not os.access(datadir_base, os.W_OK):
        datadir_base = os.path.join('/tmp', '.keras')
    datadir = os.path.join(datadir_base, 'datasets')
    glove_filename_txt = os.path.join(datadir, fname)
    alreadyTere = os.path.exists(glove_filename_txt)
    if not alreadyTere:
        path = 'glove.6B.zip'
        newpath = get_file(path, origin="http://nlp.stanford.edu/data/glove.6B.zip")
        #!unzip {datadir}/{path}    


def _makeLowercase_gloveIndexDict(glove_index_dict):
    """ 02-15 1115am
    Ensures that all the entries in the index dictionary
    have lowercase versions with weight values that match
    """
    tempDictToAddLowercaseVersions = {}
    for word,i in glove_index_dict.items():    
        word_low = word.lower()
        match = word_low == word
        if not match:
            print('comparing {} | {}'.format(word_low, word))
        if word_low not in glove_index_dict:
            print('adding word_low: {}'.format(word_low))
            tempDictToAddLowercaseVersions[word_low] = i  
    glove_index_dict.update(tempDictToAddLowercaseVersions)
    return glove_index_dict
    

def getGloVeEmeddingWeights(glove_filename_txt, embedding_dimension = 100, global_scale = 1):
    """
    workin on this one
    Returns a tuple:
        [0] glove_embedding_weights :: NDArray
        [1] and glove_index_dict :: dictionary
    """
    import numpy as np
    #import os
    glove_index_dict = {}
    
    glove_n_symbols = len(open(glove_filename_txt).readlines())
    glove_embedding_weights = np.empty((glove_n_symbols, embedding_dimension))
    with open(glove_filename_txt) as fp:
        i = 0
        for line in fp:
            line = line.strip().split()
            word = line[0]
            glove_index_dict[word] = i
            restOfLine = line[1:]
            mapp = map(float,restOfLine)
            glove_embedding_weights[i,] = list(mapp)
            i += 1
    glove_embedding_weights *= global_scale
    glove_index_dict_normalized = _makeLowercase_gloveIndexDict(glove_index_dict)
    return glove_embedding_weights, glove_index_dict_normalized



seed = 42


def currentTesting():
    four = 2+2 #just a placeholder
    #glove_filename_txt = '/Users/lex/.keras/datasets/glove.6B.100d.txt'
    #getOrVerifyGloVeExists(filename)
    
    #embedding_dimension = 100
    #glove_filename_txt = '/Users/lex/.keras/datasets/glove.6B.100d.txt'
    # read the number of lines in glove_filename_txt file
    


if __name__ == '__main__':
    currentTesting()
 