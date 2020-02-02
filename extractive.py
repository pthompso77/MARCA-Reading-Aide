#!/usr/bin/env python3





# ===== region debug/test ==================================================

# set verbose_success to True to see all successful "try" block messages
verbose_success = False

# SET verbose_ON to True to see other print statement messages
verbose_ON = False
# END ===== region debug/test




# ===== region imports ==================================================

import sys, os
try:
	from my_tokenize import sent_tokenize, word_tokenize
	if (verbose_success):
		print("\nYES2 got my sent_tokenize, word_tokenize")
except Exception as e:
	print("\nNO2 error from extractive.py:  from my_tokenize import word_tokenize \ne=", e)
	
# END ===== region imports




# ===== region environment and local variables ==================================================

# set environment to include nltk_data
try:
	os.environ["NLTK_DATA"] = "/home/pthompso/nltk_data"
	sys.path.append("/home/pthompso/nltk_data")
	if (verbose_success):
		print("\nYES0 set vars")
except Exception as e:
	print('\nno0 e:',e)

"""defines the list of stopwords (words that will be overlooked during evaluation)"""
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
	
# END ===== region environment and local variables





# ===== region load text ==================================================

# article is set to a default value at first
article = """
In LDA, each document may be viewed as a mixture of various topics where each document is considered to have a set of topics that are assigned to it via LDA. This is identical to probabilistic latent semantic analysis (pLSA), except that in LDA the topic distribution is assumed to have a sparse Dirichlet prior. The sparse Dirichlet priors encode the intuition that documents cover only a small set of topics and that topics use only a small set of words frequently. In practice, this results in a better disambiguation of words and a more precise assignment of documents to topics. LDA is a generalization of the pLSA model, which is equivalent to LDA under a uniform Dirichlet prior distribution.[5]

For example, an LDA model might have topics that can be classified as CAT_related and DOG_related. A topic has probabilities of generating various words, such as milk, meow, and kitten, which can be classified and interpreted by the viewer as "CAT_related". Naturally, the word cat itself will have high probability given this topic. The DOG_related topic likewise has probabilities of generating each word: puppy, bark, and bone might have high probability. Words without special relevance, such as "the" (see function word), will have roughly even probability between classes (or can be placed into a separate category). A topic is neither semantically nor epistemologically strongly defined. It is identified on the basis of automatic detection of the likelihood of term co-occurrence. A lexical word may occur in several topics with a different probability, however, with a different typical set of neighboring words in each topic.
"""

# END ===== region load text




# ===== region Creating Dictionary Table ==================================================

def create_frequency_table(article) -> dict:
	"""Creates a table that shows the frequency of each word's occurence.
	
	Counts the number of times each word occurs in the text.
	
	Args:
		article: full text to summarize
		
	Returns:
		A dict with each unique word as the key,
		the value is the number of times that word occurs in the text.
		For example:
		
		{'lonely': 1,
		 'and': 35,
		 'trouble': 2}	
	"""
	
	# 1. Tokenize the text into one-word tokens
	words = word_tokenize(article)


	# 2. Stemming: reduce words to their root form
		# Stemming is the process of producing morphological variants of a root/base word.
	# stemmer = PorterStemmer() # removed 1719...not sure why...
	# TODO come back to this. Let's get PorterStemmer working!
	

	# 3. Create dictionary for the word frequency table
	freq_tab = dict() #this is the return value
	
	# 4. Remove stop words
	stopWords = stopwords	
	for word in words:
		# word = stemmer.stem(word) # removed 1719
		word = word.lower() # (I think stemmer does this...)
		if word in stopWords:
			continue # this is a stopword, we don't need it
		if word in freq_tab: #if we already have it
			freq_tab[word] += 1
		else:
			freq_tab[word] = 1

	return freq_tab

# create a frequency table from the article we received
freq_table = create_frequency_table(article)

# END ===== region Creating Dictionary Table




# ===== region Tokenize the sentences ==================================================

# Tokenize the sentences using my copy of NLTK's `sent_tokenize`
try:
	sentences = sent_tokenize(article)
	if (verbose_success):
		print('\nYES tokenized the sentences!',sentences)
except Exception as e:
	print('\nNO error with sentences/sent_tokenize. error=',e)
# END ===== region Tokenize the sentences





# ===== region Find weighted frequencies ==================================================

# ## Find weighted frequencies of the sentences
# #### Used to prioritize sentences to identify which ones should be summarized

# Algorithm for scoring a sentence by its words
def find_weighted_frequencies(sentencesThatAre, inFrequencyTable) -> dict:
	"""Calculates the weight of a sentence. This is done by using the frequency table
	   that was filled in create_frequency_table() 
	   
	Arguments:
	   sentencesThatAre: a list of tokenized sentences
	   inFrequencyTable: a frequency table (dict) indicating the occurence count for unique words in the article
	   
	Returns:
	   dict with the sentence as the key and it's calculated weight as the value
	"""

	sentenceWeights = dict()  # return variable
	if (verbose_ON):
		print('\nSENTENCESTHATARE:',sentencesThatAre)
	# TODO optimize this
	for sentence in sentencesThatAre:
		sentenceLength_withoutStops = 0
		for wordFreq in inFrequencyTable:
			# TODO is it 'lower' in wordFreq?
			if wordFreq in sentence.lower(): #lowercase
				sentenceLength_withoutStops += 1 # counting the word only if it isn't a stopword
				if sentence in sentenceWeights: # if it already exists
					sentenceWeights[sentence] += inFrequencyTable[wordFreq] # count it up
				else:
					sentenceWeights[sentence] = inFrequencyTable[wordFreq]
		# normalize the sentenceWeights
		if (sentenceLength_withoutStops == 0):
			sentenceWeights[sentence] = 0
		else:
			sentenceWeights[sentence] = (sentenceWeights[sentence] / sentenceLength_withoutStops)
		
	return sentenceWeights


# 
sentence_scores = find_weighted_frequencies(sentences, freq_table)

# END ===== region Find weighted frequencies





# now that the sentences have scores (weighted values)...
# ## Get a threshold by finding average score for each sentence
#

# In[ ]:


# Getting the threshold
def getThresholdUsingSentenceWeights(sentence_weights) -> int:
	valueSum = 0
	for key in sentence_weights:
		valueSum += sentence_weights[key]
	return (valueSum / len(sentence_weights))

# threshold = _calculate_average_score(sentence_scores)
threshold = getThresholdUsingSentenceWeights(sentence_scores)


# now that we have a threshold weight
# ## Get the Summary!

# In[ ]:


# Producing the summary
def finalizeSummary(sentences, sentence_weight, threshold):
	sentence_counter = 0
	article_summary = ''

	for sentence in sentences:
		if (sentence in sentence_weight) and sentence_weight[sentence] >= (threshold):
#			 print('yes',sentence_weight[sentence],'thresh:',threshold)
			article_summary += sentence + "<br>"
			sentence_counter += 1

	return article_summary

# finalizeSummary(sentences, sentence_scores, 1.5 * threshold)

article_other = """NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike. NLTK is available for Windows, Mac OS X, and Linux. Best of all, NLTK is a free, open source, community-driven project.

NLTK has been called “a wonderful tool for teaching, and working in, computational linguistics using Python,” and “an amazing library to play with natural language.”

Natural Language Processing with Python provides a practical introduction to programming for language processing. Written by the creators of NLTK, it guides the reader through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more. The online version of the book has been been updated for Python 3 and NLTK 3. (The original Python 2 version is still available at http://nltk.org/book_1ed.)"""


# # and now all together

# In[259]:


def doArticleSummary(article):

	#creating a dictionary for the word frequency table
#	 frequency_table = #_create_dictionary_table(article)
	try:
		freq_table = create_frequency_table(article)
	except:
		print('''cannot set freq_table
			article is:''',article)
	# print(freq_table)

	#tokenizing the sentences
#	 sentences = #sent_tokenize(article)
	sentences = sent_tokenize(article, keepOriginalPunctuation=True)
#	 print("sentences",sentences)

	#algorithm for scoring a sentence by its words
#	 sentence_scores = #_calculate_sentence_scores(sentences, frequency_table)
	sentence_scores = find_weighted_frequencies(sentences, freq_table)
#	 print("sentence_scores",sentence_scores)


	#getting the threshold
#	 threshold = #_calculate_average_score(sentence_scores)
	threshold = getThresholdUsingSentenceWeights(sentence_scores)
#	 print("threshold",threshold)
	# print("sentence_scores","(1.2*threshold=",1.2*threshold,")",sentence_scores.values())


	#producing the summary
	article_summary = finalizeSummary(sentences, sentence_scores, 1.0 * threshold)
	if (verbose_ON):
		print('\nextractive article summary:',article_summary,'\n[end summary]')
	return article_summary

# print("article:",article,"summary:",doArticleSummary(article),sep='\n\n')

if __name__ == "__main__":
	if (verbose_ON):
		print("\n\n__name__ == __main__")
