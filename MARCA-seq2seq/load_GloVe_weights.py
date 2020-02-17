import summarizerTools


def getPickledTuple(just100 = True):
        """Get the pickled tuple of 1,000,000 (Headlines, Keywords [None right now], and Descriptions)"""
                # (takes 10-20 seconds)
        heads_keys_descs = summarizerTools.getPickledTuple(just100=True)
        return heads_keys_descs
        
def doOtherStuff(comebacktothis = True):
        """Build a vocabulary?"""
        vocabularyMap, wordCounts = summarizerTools.getVocabularyAndCountFromTuple(heads_keys_descs)
        print(wordCounts,'\n\nit works')
        
        
        """Index the words - get two dictionaries (word:index and index:word)"""
        word2index, index2word = summarizerTools.getDictsOfWordsAndIndices(vocabularyMap, wordCounts)
        
def getGloVe():
        """GloVe"""
        seed = 42
        embedding_dimension = 100
        vocabulary_size = 40000
        filename = '/Users/lex/.keras/datasets/glove.6B.{}d.txt'.format(embedding_dimension)
        print('using file: ',filename)
        summarizerTools.getOrVerifyGloVeExists(filename, embedding_dimension=embedding_dimension)
        # NDArray: gloVeEmeddingWeights 
            # e.g. [-0.0038194, -0.024487 , ... , -0.01459  ,  0.08278]
        # dictionary: glove_index_dict
            # e.g. {'the' : 0 , ... , 'for' : 10}
        gloVeEmeddingWeights, glove_index_dict = summarizerTools.getGloVeEmeddingWeights(filename)
        print('got gloVeEmeddingWeights, which has the type: ',type(gloVeEmeddingWeights))
        return gloVeEmeddingWeights, glove_index_dict



def __initializeRandomWordEmbedding(gloVeEmeddingWeights):
        import numpy as np
        seed = 42
        vocab_size = 40000
        embedding_dimension = 100
        np.random.seed(seed)
        shape = (vocab_size, embedding_dimension)
        scale = gloVeEmeddingWeights.std()*np.sqrt(12)/2 # uniform and non-normal
        embedding = np.random.uniform(low = -scale, high = scale, size = shape)
        """ embedding :: numpy.ndarray
        array([[-0.17738751,  0.63726418,  0.32801584, ..., -0.10244963,
        -0.67100908, -0.55440164],
       [-0.66251147,  0.19287045, -0.26248176, ...,  0.56147351,
         0.54730083,  0.39571555],
       [ 0.2008183 , -0.58798379, -0.47842258, ..., -0.40180016,
         0.17375463, -0.58627651],
       ...,
       [ 0.69823127, -0.26700707, -0.3871925 , ..., -0.0267477 ,
        -0.11873932, -0.5748738 ],
       [ 0.42866682, -0.48184197, -0.15299062, ...,  0.564503  ,
         0.36926458,  0.34503737],
       [ 0.12692557,  0.38353676, -0.49469062, ...,  0.15906193,
        -0.57420162,  0.34496176]])
        """
        return embedding
        

def __copyGloveWeights(randomEmbedding, index2word, gloVeEmeddingWeights, glove_index_dict):
        """copy from glove weights of words that appear in our short vocabulary (index2word)"""
        keepingCount = 0
        vocab_size = gloVeEmeddingWeights.shape[0] # 40,000 words
        vocab_size = len(index2word) # 430 words...
        embedding = randomEmbedding
        wordsNotFound = []
        for i in range(vocab_size):
                embeddingAt_i_ = embedding[i,:]
                word = index2word[i]
                gloveIndex = glove_index_dict.get(word, glove_index_dict.get(word.lower()))
                if gloveIndex is None and word.startswith('#'):
                        word = word[1:]
                        gloveIndex = glove_index_dict.get(word, glove_index_dict.get(word.lower()))
                        print('gloveIndex is None:',gloveIndex, '\tword is:',word)
                if gloveIndex is not None:
                        embedding[i,:] = gloVeEmeddingWeights[gloveIndex,:]
                        keepingCount+=1
                else:
                        wordsNotFound.append(word)
        return embedding, wordsNotFound


def copyGloveWeightsToCustomInputList(index2word, gloVeEmeddingWeights, glove_index_dict):
        import numpy as np
        compare_threshold = 0.5 # don't accept distances below this threshold
        randomEmbedding = __initializeRandomWordEmbedding(gloVeEmeddingWeights)
        gloveWeightedEmbedding, wordsNotFound = __copyGloveWeights(randomEmbedding, index2word, gloVeEmeddingWeights, glove_index_dict)
        """CURRENT"""
        #otherArray = np.array(
        #[np.sqrt(
                #np.dot
                #)
        #)
        #normalized_embedding = embedding / otherArray
        
        
        TODO = True

if __name__ == '__main__':
        getGlove()


