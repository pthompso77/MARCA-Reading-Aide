#!/usr/bin/env python3

import cgi
from os import environ
results_file = "results.py"


def printContentType(setCookie=False, includeDoctype=True):
    if setCookie:
        pass
    contentTypeMessage = '''Content-type: text/html\r\n\r\n''' + "<!doctype html>" if includeDoctype else ""
    print(contentTypeMessage)

def parseArgs(tagType, attribute, args):
    opentag = "<{tagType} {attr}=".format(tagType=tagType, attr=attribute)
    closetag = "></{tagType}\r\n".format(tagType=tagType)
    output = ""
    for arg in args:
        output = output + opentag + arg + closetag
    return output


def printHead(titleIn="Summarize", scripts=["scripts/JS/main.js"], stylesheet="scripts/CSS/main.css"):
    scriptImport = parseArgs(tagType="script",attribute="src",args=scripts)
    style = '<link rel="stylesheet" type="text/css" href="{}">'.format(stylesheet)
    otherstuff = '''
	<title>{title}</title>
    {scriptImports}
	<meta charset="utf-8">
	<meta name="description" content="Summarize any length of text">
	<meta name="keywords" content="Summary, Abstract, NLP, Computer science, artificial intelligence">
	<meta name="author" content="Peter T">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">'''
    otherstuff = otherstuff.format(title=titleIn, scriptImports=scriptImport)
    headElement = '''<head>
	{one}
    {two}
	</head>'''
    headElement = headElement.format(one=style,two=otherstuff)
    print(headElement)


def printNavigationBar():
    navbar = '''
	<!--Navigation Bar-->
	<div id="nav-bar">
	    <section id="login-link" class="">
		<a href="">Log In or Register</a>
	    </section>

	    <section id="login-link2" class="">
		<br>
		<a href="">Log In or Register(2)</a>
		<a class="btn" href="javascript:{alert('hiii')}"> say hi</a>
		<a class="btn" href="javascript:{tryXHR('?bingo=bongo")}"> XHR</a>

	    </section>
	</div>
	<!--end Navigation Bar-->'''
    print(navbar)

def printTesters():
    test1 = '''
	<section id="GET-id" class="login_register">
		<a href="?get-id=boop">test-Get</a>
	    </section>

	    <a href="javascript:{alert('hey!');}">Test-Hey
	    </a>
	    <a href="javascript:{setcookie('SESSIONID','bigLONGvalueeeee83982364^yeah');}">Test-Cookie
	    </a>

	    '''
    test2='''
	<form id='testformid' class='testformclass' action='' method='post'>
	    <input name='testinput' type="text">
		<input name="setCookie" type="hidden">
	    <input type="submit" value="Go!"/>
	    </form>
	    '''
    print(test1,test2)
    '''start POST'''
    print('<div>')
    form = cgi.FieldStorage()
    for i in form:
        print('i=',i,'<br>')
        print('FROM cgi.FieldStorage:', i,form[i],'<br>')
    #val = form[i]
    #print('you entered: {}'.format(val))
    print('<hr></div>')
    '''end POST'''


    '''start COOKIE'''
    print('<div>')

    print('<hr></div>')
    '''end COOKIE'''


    '''start ENVIRON VARIABLES'''
    print('<div>environ:')
    print('<br><br>trying to get environ GET value<br>')
    env = environ.items()
    GET = environ.get('QUERY_STRING')
    #for g in GET.split('='):
        #print(g)
    print(GET)
    print('<br><br>')
    for item in environ.items():
        print('<br>',item)
    print('</div>')
    '''end ENVIRON VARIABLES'''

class Homepage():
    @staticmethod
    def _printBody():
        print ('''<!--A Flexible Layout must have a parent element with the display property set to flex. Direct child element(s) of the flexible container automatically become flexible items.-->''')

        print("<body>")
        printNavigationBar()




        print('''
			<div class="flex-container">

				<section id="input-section">
					<a href="index.py">
					<h1>Insert Text to Summarize Below</h1>
						</a>
					<div id="text-container">
						<textarea id="text-input" name="userInput" form="text-form" required></textarea>
					</div>'''+
                                                 '''<form id="text-form" action="''')

        print(results_file)

        print('''" method="post">
					<input type="submit" id="submit-text" value="Summarize"/>
						</form>'''+
                                                          '''</section>
		<!--		end of input-section-->

				<section id="summary-section">
					<h2>Summary</h2>
					<div id="summary-container" class="generated">
						<article id="keywords">
		<!--				<h3>Key words and phrases</h3>-->
						<p  class="container">

						</p>
							</article>
		<!--
						<article id="arguments" >
						<h3>Arguments</h3>
						<p  class="container">
						<span class="arg">Text must be full for processing.</span>
							<span class="arg">Emptiness means nothing.</span>
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
    @staticmethod
    def printPage():
        printContentType()
        printHead(stylesheet="scripts/CSS/main.css")
        Homepage._printBody()




class LoginPage():
    def printPage():
        printContentType()
        printHead(titleIn="Login")
        LoginPage._printBody()
    @staticmethod
    def _printBody():
        print('''
		<body>
		<h1>Let's Log In!</h1>
        <form id="user-login-form" action="{action}"
		'''.format("user-login.py"))
        #method="post">
        print('''method="get">
	    <label for="username_in">Username</label>
	    <input type="text" id="uname" name="username_in"><br><br>

	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>

	    <input type="submit" value="Submit">
		</form>
		</body>''')



if __name__ == "__main__":
    printHead()
    printTesters()
    Homepage.printPage()
