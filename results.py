#!/usr/bin/env python3

print('Content-type: text/html\r\n\r\n')
print('<!--')
import cgi, cgitb; cgitb.enable()
import os, traceback, sys

'''
set verbose_success to True to see all successful "try" block messages
'''
verbose_success = False

'''
set nameOfThisFile to the name of this file
'''
nameOfThisFile = "results.py"


form = cgi.FieldStorage()
try:
	userInput = form.getvalue('userInput')
	if (verbose_success):
		print('\nsuccess in results: got form\'s userInput')
except:
	print('\nerror in results1')
	userInput = '[error getting userInput]'

if userInput is None:
	print('\nOH NO! results: userInput is None')
	userInput = '''There are broadly two types of extractive summarization tasks depending on what the summarization program focuses on. The first is generic summarization, which focuses on obtaining a generic summary or abstract of the collection (whether documents, or sets of images, or videos, news stories etc.). The second is query relevant summarization, sometimes called query-based summarization, which summarizes objects specific to a query. Summarization systems are able to create both query relevant text summaries and generic machine-generated summaries depending on what the user needs.

An example of a summarization problem is document summarization, which attempts to automatically produce an abstract from a given document. Sometimes one might be interested in generating a summary from a single source document, while others can use multiple source documents (for example, a cluster of articles on the same topic). This problem is called multi-document summarization. A related application is summarizing news articles. Imagine a system, which automatically pulls together news articles on a given topic (from the web), and concisely represents the latest news as a summary.

Image collection summarization is another application example of automatic summarization. It consists in selecting a representative set of images from a larger set of images.[2] A summary in this context is useful to show the most representative images of results in an image collection exploration system. Video summarization is a related domain, where the system automatically creates a trailer of a long video. This also has applications in consumer or personal videos, where one might want to skip the boring or repetitive actions. Similarly, in surveillance videos, one would want to extract important and suspicious activity, while ignoring all the boring and redundant frames captured.

At a very high level, summarization algorithms try to find subsets of objects (like set of sentences, or a set of images), which cover information of the entire set. This is also called the core-set. These algorithms model notions like diversity, coverage, information and representativeness of the summary. Query based summarization techniques, additionally model for relevance of the summary with the query. Some techniques and algorithms which naturally model summarization problems are TextRank and PageRank, Submodular set function, Determinantal point process, maximal marginal relevance (MMR) etc.
'''
	userInput = """And at first, this sort of thing is unpleasant enough.
 It touches one's sense of honor, particularly if you come of an old established family in the land, the van Rensselaers, or Randolphs, or Hardicanutes.
 And more than all, if just previous to putting your hand into the tar-pot, you have been lording it as a country schoolmaster, making the tallest boys stand in awe of you.
 The transition is a keen one, I assure you, from the schoolmaster to a sailor, and requires a strong decoction of Seneca and the Stoics to enable you to grin and bear it.
 But even this wears off in time.
  What of it, if some old hunks of a sea-captain orders me to get a broom and sweep down the decks?
 What does that indignity amount to, weighed, I mean, in the scales of the New Testament?
 Do you think the archangel Gabriel thinks anything the less of me, because I promptly and respectfully obey that old hunks in that particular instance?
 Who aint a slave?
 Tell me that.
 Well, then, however the old sea-captains may order me about - however they may thump and punch me about, I have the satisfaction of knowing that it is all right; that everybody else is one way or other served in much the same way - either in a physical or metaphysical point of view, that is; and so the universal thump is passed round, and all hands should rub each other's shoulder-blades, and be content.
  Again, I always go to sea as a sailor, because they make a point of paying me for my trouble, whereas they never pay passengers a single penny that I ever heard of.
 On the contrary, passengers themselves must pay.
 And there is all the difference in the world between paying and being paid.
 The act of paying is perhaps the most uncomfortable infliction that the two orchard.
 thieves entailed upon us.
 But being paid, - what will compare with it?
 The urbane activity with which a man receives money is really marvellous, considering that we so earnestly believe money to be the root of all earthly ills, and that on no account can a monied man enter heaven.
 Ah!
 how cheerfully we consign ourselves to perdition!
 Finally, I always go to sea as a sailor, because of the wholesome exercise and pure air of the forecastle deck.
 For as in this world, head winds are far more prevalent than winds from astern (that is, if you never violate the Pythagorean maxim), so for the most part the Commodore on the quarter-deck gets his atmosphere at second hand from the sailors on the forecastle.
 He thinks he breathes it first; but not so.
 In much the same way do the commonalty lead their leaders in many other things, at the same time that the leaders little suspect it."""
# from camra import camIO
# import camra
try:
	
	import extractive
	if (verbose_success):
		print('\nimported extractive from results.py')
except Exception as e:
	print('\nfailed to import extractive. Exception is:',e)
	exc_type, exc_value, exc_traceback = sys.exc_info()
	print("*** print_tb:")
	traceback.print_tb(exc_traceback, file=sys.stdout)

try: #try to get the 'processed' text from the processing engine
	if (verbose_success):
		print('\ntrying in results, userinput:',userInput)
	# keyWordsPhrases, argmnts = camra.summarizeThisText(userInput) #form.getvalue('userInput')
	# keyWordsPhrases = camra.summarizeThisText(userInput)
	keyWordsPhrases = extractive.doArticleSummary(userInput)
	if (verbose_success):
		print('\nresults: got keyWordsPhrases:',keyWordsPhrases)
except Exception as e:
	print('\nerror in results2:',e)
	errMessage = '[error getting keyWordsPhrases]\n' + str(e)
	keyWordsPhrases, argmnts = errMessage, '[error getting argmnts]'
	# keyWordsPhrases = '[error getting keyWordsPhrases]'

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
			<form id="text-form" action='''
				+ nameOfThisFile +
				''' method="post">
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
