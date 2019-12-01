#!/usr/bin/env python3

"""
TRYING TO PUT IT ALL TOGETHER WITHOUT (my) IMPORTS
"""

print('Content-type: text/html\r\n\r\n')
print('<!--')
import cgi, cgitb; cgitb.enable()
import os

"""
START EXTRACTIVE
"""
try:
	import nltk
	print('\n TRYING to get stopwords')
	from nltk.corpus import stopwords
	print('\n success with: from nltk.corpus import stopwords')
	nltk.download('stopwords')
	print('\n success with nltk.download(\'stopwords\')')
	stopwordsEN = stopwords.words('english')
	print('\n success getting stopwordsEN:',stopwordsEN)
except:
	print("error from extractive.py:  from nltk.corpus import stopwords")
try:
	from nltk.stem import PorterStemmer
	print('\n successfully imported from nltk.stem import PorterStemmer')
except:
	print("error from extractive.py:  from nltk.stem import PorterStemmer")
try:
	from nltk.tokenize import word_tokenize, sent_tokenize
	print('\n successfully imported from nltk.tokenize import word_tokenize, sent_tokenize')
except:
	print("error from extractive.py:  from nltk.tokenize import word_tokenize, sent_tokenize")

# ### Creating Dictionary Table

def create_frequency_table(article):
	print('\n starting: create_frequency_table()')
	#remove stop words
	try:
		import nltk
		print('\n\t success nltk1')
		from nltk.corpus import stopwords
		print('\n\t success nltk2')
		# nltk.download('stopwords')
		print('\n\t success nltk3')
		stopwordsEN = stopwords.words("english")
		print("\nstopwords type:",type(stopwordsEN))
		# stopWords = set(stopwords.words("english"))
	except:
		print('\n Error loading stop words (loading manually)')
		stopwordsEN = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
		print("\nstopwords type:",type(stopwordsEN))

	print('\n trying to word_tokenize(article)')
	try:
		from nltk.tokenize import word_tokenize
		print('\n success importing word_tokenize',word_tokenize)
		words = word_tokenize(article)
		# try:
		# 	import pickle
		# 	print('success import PICKLE')
		# 	output = open('word_tokenize.pkl','wb')
		# 	pickle.dump(word_tokenize, output)
		# 	output.close()
		# 	print('\b success pickling')
		# except:
		# 	print('fail pickle')
		print('\n success with word_tokenize(article)\n\t',words)
	except:
		import pickle
		print('\n\t something wrong with word_tokenize???')
		print('\n try to unpickle')
		input = open('word_tokenize.pkl','rb')
		print('\nsuccess1')
		word_tokenize = pickle.load(input)
		print('\nsuccess2')
		print('\n unpickled it:',word_tokenize)
		words = word_tokenize(article)
		print('\n \t success with word_tokenize(article)\n\t',words)
	#reduce words to their root form

	#Stemming is the process of producing morphological variants of a root/base word.
	print('\n trying to stemmer = PorterStemmer()')
	stemmer = PorterStemmer()
	print('\n success with stemmer = PorterStemmer()')

	# Creating dictionary for the word frequency table
	freq_tab = dict()
	print('freq_tab init:',freq_tab)
	print('\n\nITERATING THROUGH ALL WORDS in words',words,'\n\n')
	for word in words:
		# print('\n word is:',word)
		word2 = stemmer.stem(word)
		# print('\n stemmed word is:',word2)
		if word2 in stopwordsEN:
			# print('\n word2 in stopwords')
			continue # then we don't need this
		elif word2 in freq_tab: #if we already have it
			# print('\n word2 in freq_tab')
			freq_tab[word2] += 1
		else:
			# print('\n else')
			freq_tab[word2] = 1

	print('\n freq_tab is:',freq_tab)
	return freq_tab

# Algorithm for scoring a sentence by its words
def find_weighted_frequencies(sentencesThatAre, inFrequencyTable):

	sentenceWeight = dict()  # return variable

	for sentence in sentencesThatAre:
		sentenceLength = len(word_tokenize(sentence))
		sentenceLength_withoutStops = 0
		for wordFreq in inFrequencyTable:
			if wordFreq in sentence.lower(): #lowercase
				sentenceLength_withoutStops += 1 # counting the word only if it isn't a stopword
				if sentence in sentenceWeight: # if it already exists
					sentenceWeight[sentence] += inFrequencyTable[wordFreq] # count it up
				else:
					sentenceWeight[sentence] = inFrequencyTable[wordFreq]
		# normalize the sentenceWeight
		sentenceWeight[sentence] = (sentenceWeight[sentence] / sentenceLength_withoutStops)
	return sentenceWeight

# Getting the threshold
def getThresholdUsingSentenceWeights(sentence_weights):
	valueSum = 0
	for key in sentence_weights:
		valueSum += sentence_weights[key]
	return (valueSum / len(sentence_weights))

# Producing the summary
def finalizeSummary(sentences, sentence_weight, threshold):
	print('\n starting finalizeSummary')
	sentence_counter = 0
	article_summary = ''
	for sentence in sentences:
		if (sentence in sentence_weight) and sentence_weight[sentence] >= (threshold):
			article_summary += " " + sentence
			sentence_counter += 1

	print('\nfinalizeSummary returns:',article_summary,"[end]\n")
	return article_summary

def doArticleSummary(article):
	print("\ndoArticleSummary success")
	freq_table = create_frequency_table(article)
	print('\nfreq_table success')
	# try:
	#	 freq_table = create_frequency_table(article)
	# except:
	#	 print('''cannot set freq_table
	#		 article is:''',article)
	sentences = sent_tokenize(article)
	print('\n sentences success')
	sentence_scores = find_weighted_frequencies(sentences, freq_table)
	print('\n sentence_scores success')
	threshold = getThresholdUsingSentenceWeights(sentence_scores)
	print('\n threshold success')
	article_summary = finalizeSummary(sentences, sentence_scores, 1.0 * threshold)
	print('\nextractive article summary:',article_summary,'\n[end summary]')
	return article_summary

"""
END EXTRACTIVE
"""


form = cgi.FieldStorage()
try:
	userInput = form.getvalue('userInput')
	print('\nsuccess in results: got form\'s userInput')
except:
	print('\nerror in results1')
	userInput = '[error getting userInput]'

if userInput is None:
	print('\nwe\'re testing! results: userInput is None')
	userInput = '''Lorem Ipsum is simply dummy text of the printing and typesetting industry.
	Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
	Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
	'''


# from camra import camIO
"""
import camra
"""
"""
import campack
"""
# import extractive #(Added to this file)
class summarizer:
	def __init__(self, inputText):
		print('\nsummarizer is getting keywords with inputText:',inputText)
		self.__kywrds = getMyKeywords(inputText)
		print('\n[summarizer got keywords]',self.__kywrds,'\n')
	def getKeywords(self):
		print('\n success getting keywords(self)')
		return self.__kywrds


def getMyKeywords(txt):
	# TODO return to this and actually get keywords :)
	txt2 = 'bumble from campack.py'
	try:
		print('\ncampack: trying to send txt to extractive:',txt,'\n[end campack:trying to send txt]')
		txt2 = doArticleSummary(txt)
	except:
		txt2 = 'nope'
	return txt2
	# return txt

"""
END CAMPACK
"""
def summarizeThisText(userInput):
	print("\ntrying to create new summarizer")
	summy = summarizer(userInput)
	print("\nsuccess: created new summarizer")
	# # # some kind of error here?
	keyWordsPhrases = summy.getKeywords()
	# argmnts = ''
	print('\nsummarizeThisText (orig from campack) has kwrds:',keyWordsPhrases)
	return keyWordsPhrases #, argmnts

"""
END CAMRA
"""
try: #try to get the 'processed' text from the processing engine
	print('\ntrying in results, userinput:',userInput,'\n[end trying in results]')
	# keyWordsPhrases, argmnts = camra.summarizeThisText(userInput) #form.getvalue('userInput')
	# # # we are having a problem here...
	keyWordsPhrases = summarizeThisText(userInput)
	print('\nresults: got keyWordsPhrases:',keyWordsPhrases)
except:
	print('\nerror in results2')
	# keyWordsPhrases, argmnts = '[error getting keyWordsPhrases]', '[error getting argmnts]'
	keyWordsPhrases = '[error getting keyWordsPhrases]'

	# print('got keyWordsPhrases',keyWordsPhrases)


print(' -->')

""" ---------------------------------------------------
HTML
"""

print('''
<!doctype html>
<head>
	<title>Summarize!</title>
	<script src="js/xhr.js"></script>
	<meta charset="utf-8">
  <meta name="description" content="Summarize any length of text">
  <meta name="keywords" content="Summary, Abstract, NLP, Computer science, artificial intelligence">
  <meta name="author" content="Peter T">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<style>
		a {
			text-decoration: none;
		}
		* {
			box-sizing: border-box;
  background-color: #f1f1f1;
		}
/*
justify-content		align the flex items horizontal (side to side in container)
						(default: flex-start)
align-items			Vertically aligns the flex items when the items do not use all available
					space on the cross-axis
						(default: stretch) stretches the space
align-content		Modifies the behavior of the flex-wrap property. It is similar to align-
					items, but instead of aligning flex items, it aligns flex lines
						(default: stretch) stretches items
*/

.flex-container {
	min-height: 500px;
  display: flex;
/*	flex-direction: row;*/
/*	flex-wrap: wrap;*/
	flex-flow: row wrap;
/*	justify-content: space-between;*/
/*	align-items: center;*/
	align-content: center;
}

/*
The flex item properties are:
order
flex-grow
flex-shrink
flex-basis
flex
align-self
*/
#input-section {
/*	order: 2;*/
	flex-grow: 2;/* default is 0
/*	flex-shrink: 0; default is 1*/
	flex-basis: 320px;
/*	align-self: center; (overrides anything defined in the flex container) */
}

/*		this is a flex item*/
.flex-container > section {
  background-color: #f1f1f1;
  margin: 10px;
  padding: 20px;
  font-size: 30px;
/*  min-width: 300px;*/
	flex: 1 0 300px;
}
		#test-text {
			margin: 15px;
		}
		#test-text section { /*row*/
			display: flex;
			flex-direction: row;
			flex-wrap: wrap;
			width: 100%;
		}
		#test-text article { /*column*/
			padding: 10px;
			display: flex;
			flex-direction: column;
			flex-basis: 100%;
			flex: 1 0 400px;
		}
		#test-text p{
			font-size: 12px;
		}

		h1{
			font-family: "PT Sans";
    font-size: 32px;
    font-weight: 400;
    font-style: normal;
    text-decoration: none;
    text-transform: none;
    color: #000;
/*    background-color: initial;*/
    line-height: 42px;
    letter-spacing: normal;
    text-shadow: none;
		}
		h2 {
			    font-family: "PT Sans";
    font-size: 32px;
    font-weight: 400;
    font-style: italic;
    color: #808080;
    line-height: 62px;
		}
		h3 {
			    font-family: "PT Sans";
    font-size: 26px;
    font-weight: 400;
    font-style: normal;
    text-decoration: none;
    text-transform: none;
    color: #000;
    background-color: initial;
    line-height: 33px;
    letter-spacing: normal;
    text-shadow: none;
			    padding-top: 0;
    text-indent: 0;
    padding-bottom: 0;
    padding-right: 0;
    text-align: left;
		}
		p, p *{
			font-family: Lato;
				font-size: 20px;

		}

/*		FOR LEFT SIDE: TEXT CONTAINER*/

		#text-container, .container {
			min-width: 200px;
			min-height: 100px;
			display: flex;
/*			flex-direction: row;*/
			flex-flow: row wrap;
/*			justify-content: flex-end;*/
			align-content: space-between;
		}
		#text-input {
/*
			flex-basis: 400px;
			flex-basis: 100%;
*/
			flex: 1 0 100%;
			min-height: 200px;
		}
		#submit-text {
			flex: 0 0 100px;
			align-self: flex-end;
			font-family: "Helvetica Neue", sans-serif;
    font-size: 20px;

    text-align: center;
			margin-top: 20px;
    padding: 15px;
    border: 1px solid #52646f;
    border-radius: 24px;
    background-color: #82939e;
		}


		.arg {
/*			todo*/
/*			align-self: flex-start;*/
		}


</style>
</head>

<!--A Flexible Layout must have a parent element with the display property set to flex. Direct child elements(s) of the flexible container automatically becomes flexible items.-->

<body>
	<div class="flex-container">
		<section id="input-section">
			<a href="index.py">
			<h1>Insert Text to Summarize Below</h1>
				</a>
			<div id="text-container">
				<textarea id="text-input" name="userInput" form="text-form" required>'''
	  + userInput +
				'''</textarea>
			</div>
			<form id="text-form" action="results_1201.py" method="post">
<!--			<form id="text-form" onsubmit="tryXHR()" action="ajax.py" method="post"> -->
			<input type="submit" id="submit-text" value="Summarize"/>
				</form>
		</section>
<!--		end of input-section-->

		<section id="summary-section">
			<h2>Summary</h2>
			<div id="summary-container" class="generated">
				<article id="keywords">
<!--				<h3>Key words and phrases</h3>-->
				<p  class="container">
					'''+ keyWordsPhrases +'''
				</p>
					</article>
<!--
				<article id="arguments" >
				<h3>Arguments</h3>
				<p  class="container">
				<span class="arg">Text must be full for processing.</span>
					<span class="arg">Emptiness means nothing.</span>
						<span class="arg"></span>
				</p>
					</article>
-->
			</div>
<!--			end summary container-->
		</section>
<!--		end of summary-section-->

	</div>

<div id="test-text">
		<h1>Sample Text</h1>
	<section>
		<article>
		<h5>From <a href="https://lipsum.com/" target="_blank">lipsum.com</a></h5>
<p>
	Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
</p>
<p>
Why do we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
</p>
<p>
Where does it come from?
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
</p></article>
	<article>
	<h5>From <a href="https://en.wikipedia.org/wiki/Automatic_summarization" target="_blank">Wikipedia</a></h5>
		<p>
		There are broadly two types of extractive summarization tasks depending on what the summarization program focuses on. The first is generic summarization, which focuses on obtaining a generic summary or abstract of the collection (whether documents, or sets of images, or videos, news stories etc.). The second is query relevant summarization, sometimes called query-based summarization, which summarizes objects specific to a query. Summarization systems are able to create both query relevant text summaries and generic machine-generated summaries depending on what the user needs.
		</p>
		<p>

An example of a summarization problem is document summarization, which attempts to automatically produce an abstract from a given document. Sometimes one might be interested in generating a summary from a single source document, while others can use multiple source documents (for example, a cluster of articles on the same topic). This problem is called multi-document summarization. A related application is summarizing news articles. Imagine a system, which automatically pulls together news articles on a given topic (from the web), and concisely represents the latest news as a summary.
		</p>
		<p>

Image collection summarization is another application example of automatic summarization. It consists in selecting a representative set of images from a larger set of images.[2] A summary in this context is useful to show the most representative images of results in an image collection exploration system. Video summarization is a related domain, where the system automatically creates a trailer of a long video. This also has applications in consumer or personal videos, where one might want to skip the boring or repetitive actions. Similarly, in surveillance videos, one would want to extract important and suspicious activity, while ignoring all the boring and redundant frames captured.
		</p>
		<p>

At a very high level, summarization algorithms try to find subsets of objects (like set of sentences, or a set of images), which cover information of the entire set. This is also called the core-set. These algorithms model notions like diversity, coverage, information and representativeness of the summary. Query based summarization techniques, additionally model for relevance of the summary with the query. Some techniques and algorithms which naturally model summarization problems are TextRank and PageRank, Submodular set function, Determinantal point process, maximal marginal relevance (MMR) etc.
	</article>
		</section>
</div>
</body>
''')
