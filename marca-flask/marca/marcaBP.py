"""
Main page for Marca app (index)
"""

import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format=f'{__name__}%(asctime)s %(message)s')
log.info('Starting marcaBP.py')

from marca.text_tools.FullText import FullText, Highlight, TEST_TEXT

log.info('Starting imports in marcaBP.py')
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort
import flask_sijax
from marca.SijaxHandler import SijaxHandler
'''example:
abort(404)  # 404 Not Found
abort(Response('Hello World'))
'''

log.info('Starting importing auth.login_required and db.get_db in marcaBP.py')
try:
    from auth import login_required
    from db import get_db, escape
except:
    try:
        from marca.auth import login_required
        from marca.db import get_db
    except Exception as e:
        log.error("Error importing login_required or get_db:", e)


#: Initialize Blueprint
log.info('Initializing Blueprint in marcaBP.py')
bp = Blueprint('marcaBP', __name__)

log.info(f'''
Blueprint is : {bp.url_prefix}
{bp.root_path}
{bp.subdomain}
''')


'''=======================Variables======================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'
# HTTP codes
http_notFound = 404
http_forbidden = 403


@bp.route('/dev/db', methods=(GET, POST))
@login_required
def devDB():

    if g.user['userID'] != 29 or g.user['userID'] is None: #then the user isn't me and shouldn't see this page
        return redirect(url_for('index'))

    log.info('Starting def devDB()')
    db = get_db().connect()
    cur = db.cursor()

    if request.method==POST:
        query = request.form['query']
        #query = db.escape(query)
        DBexec = cur.execute(query)
        db.commit()
        DBresult = cur.fetchall()

        return render_template('dev/db.html',query=query, DBexec=DBexec, DBresult=DBresult)

    log.info('Finished def devDB()')
    return render_template('dev/db.html')


'''=============================INDEX VIEW============================='''

# Database table names
fullTextTable = 'FullText'
userTable = 'userAccounts'


@bp.route('/')
def index():
    log.info('Starting def index()')
    #db = get_db().connect()
    #cur = db.cursor()

    # TODO -

    log.info('Finished def index()')
    return render_template('summary/index.html')


'''=============================DASHBOARD VIEW============================='''


@bp.route('/dashboard', methods=(GET, POST))
@login_required
def dashboard():
    # TODO
    #: get userAccountsID from g.user
    try:
        userAccountsID = g.user['userID']
    except Exception as e:
        return f'''Nope: {e}'''
    error = None


    ''' (as a logged-in user)
        Submit a new text document that will be uploaded to DB and available
        to review and interact with.

    request form name = newFullText
    '''
    #if method is POST
    if request.method == POST:
        # Get the text form submitted
        fullText = request.form['newFullText']
        #: remove apostrophe
        fullText = request.form['newFullText'].replace("'","`")
        title = request.form['textTitle']
        if title == "":
            title = "Untitled"
        textobject = FullText(fullText, title=title)
        FullText.submitToDB(textobject, userAccountsID)

        #now submit all the highlighted sections too
        Highlight.submitAllHighlightsFromText_toDB(textobject)

        flash('Document Uploaded Successfully')
        if userAccountsID == 29: # (then it's me testing)
            # flash('Got Text:',textobject)
            pass
    # continues if POST, jumps here if GET
    #: select texts from DB that match user
    userTexts = getTextAssociatedWithUserID(userAccountsID)


    #: render the dashboard template, send the user Texts also
    return render_template('summary/dashboard.html', userTexts=userTexts)

'''===========Dashboard helpers==========='''




def getTextAssociatedWithUserID(userAccountsID):
    # test response
    response = [{'email': 'me', 'FullText_ID': 42, 'title': 'Untitled', 'text_tokenized': "['New', 'Document', 'duh']", 'full_text': 'New Document duh'},
                {'email': 'me', 'FullText_ID': 43, 'title': '5 CONCLUSION', 'text_tokenized': "['The', 'media', 'landscape', 'has', 'experienced', 'a', 'massive', 'change', 'with', 'the', 'arrival', 'of', 'internet', 'and', 'the', 'recent', 'advent', 'of', 'Web', '3.0', 'and', 'has', 'influenced', ',', 'in', 'fact', ',', 'completely', 'changed', 'the', 'ways', 'in', 'which', 'information', 'communication', 'takes', 'place.', 'The', 'information', 'explosion', 'on', 'social', 'media', 'platforms', 'has', 'made', 'them', 'a', 'lot', 'more', 'engaging', 'than', 'stand', 'alone', 'communication', 'platforms', '[', '89', ']', '.', 'Social', 'media', 'platforms', 'are', 'utilized', 'for', 'discussions', 'surrounding', 'various', 'domains', 'including', 'healthcare', '[', '90', ']', ',', 'internet', 'of', 'things', '[', '91', ']', ',', 'politics', '[', '92', ']', ',', 'amongst', 'others.', 'In', 'the', 'current', 'scenario', ',', 'the', 'majority', 'of', 'people', 'get', 'to', 'know', 'about', 'recent', 'happenings', 'around', 'the', 'globe', 'through', 'social', 'media', 'platforms.', 'However', ',', 'the', 'content', 'being', 'shared', 'may', 'not', 'always', 'be', 'from', 'the', 'right', 'source', 'or', 'may', 'not', 'share', 'the', 'correct', 'information.', 'This', 'makes', 'these', 'platforms', 'vulnerable', 'to', 'propagation', 'of', 'misinformation.', 'Thus', ',', 'these', 'platforms', 'often', 'make', 'the', 'source', 'of', 'several', 'rumors', 'and', 'false', 'content.']", 'full_text': '\r\nThe media landscape has experienced a massive change with the arrival of internet and the recent advent of Web 3.0 and has influenced, in fact, completely changed the ways in which information communication takes place. The information explosion on social media platforms has made them a lot more engaging than stand alone communication platforms [89]. Social media platforms are utilized for discussions surrounding various domains including healthcare [90], internet of things [91], politics [92], amongst others. In the current scenario, the majority of people get to know about recent happenings around the globe through social media platforms. However, the content being shared may not always be from the right source or may not share the correct information. This makes these platforms vulnerable to propagation of misinformation. Thus, these platforms often make the source of several rumors and false content.'}
                ]
    db = get_db().connect()
    cur = db.cursor()

    query = f'''SELECT u.email, ft.FullText_ID, ft.title, ft.text_tokenized,
    ft.full_text FROM userAccounts u, pthompsoDB.FullText ft
    INNER JOIN pthompsoDB.user_FullText_assoc fta
    ON ft.FullText_ID = fta.FullTextID
    WHERE fta.userID = {userAccountsID} AND fta.userID = u.userID;
    '''
    #query = db.escape(query)
    cur.execute(query)
    response = cur.fetchall()
    return response


'''============================== REVIEW VIEW============================='''

@bp.route('/<int:textID>/review', methods=(GET, ))
@login_required
def review(textID):
    if textID ==0: #then i'm testing
        return render_template('summary/review.html',textID=textID)

    ''' Displays selected text for review:
    - Retrieves a FullText object from the database
    - sends the text object to the review template to fill:
        + First paragraph
            - with highlights highlighted
        + all other highlights in Navigation panel
            - with paragraph separators
        + First Highlight selected:
            - active-highlight span filled
            - notes filled (from DB)
            - rating filled (from DB)
    '''

    #- Retrieve a FullText object from the database
    textobject = FullText.getFullText_fromDB(textID)
    #- send the text object to the review template to fill:
        #+ First paragraph
            #- with highlights highlighted
        #+ all other highlights in Navigation panel
    highlightedSections = getHighlightedSections(textobject) #dictionary of {index:Highlight}

    #flash('indexing:'+str(highlightedSections[428]))
        #flash(f'<a id="{highlight.id}" href="#{highlight.paragraphParent}" class="nav-links pseudolink"> {highlight.text} </a>')
    currentParagraph = prepareParagraphForDisplay(textobject, paragraphIndex=0)
            #- with paragraph separators
        #+ First Highlight selected:
            #- active-highlight span filled
            #- notes filled (from DB)
            #- rating filled (from DB)

        #TODO finish this

        # TODO: get more than just the text from DB, etc... (make a FullText object?)

    g.user['Highlights'] = highlightedSections
    g.user['activeHighlight'] = next(iter(highlightedSections.values()))

    return render_template('summary/review.html',textID=textID,
                           text=textobject.text, textobject=textobject,
                           highlights = highlightedSections,
                           currentParagraph=currentParagraph)
    # (or return a redirect?)


'''===========Review helpers==========='''

def prepareParagraphForDisplay(textobject, paragraphIndex=0, paragraphStartDelim=None):
    '''adds span around highlighted sections'''
    if paragraphStartDelim is None:
        paragraphDelims = textobject.paragraphDelims[paragraphIndex]
    else:
        paragraphDelims = textobject.getTextFromParagraphStart(paragraphStartDelim, returnSliceOnly=True)
    paragraphForDisplay = ''
    wordsDict = textobject.getWordsDict()
    start = paragraphDelims.start
    stop = paragraphDelims.stop

    for index, word in wordsDict.items():
        #if index < start or index > stop:
        #if index < stop and index > start:
        if index > stop:
            break
        if index >= start:
            newWord = f'<span id="{str(index)}" class="word">{word}</span>'
            wordsDict[index] = newWord

    hDelims = textobject.highlightDelims
    previousPointer = -1
    for delim in hDelims:
        #if delim.start < start or delim.start > stop:
        #    break
        if delim.start < start:
            continue
        if delim.start >= stop:
            break
        startWord = f'''&nbsp;<span id="H{delim.start}"class=highlighted onclick="refresh_active_highlight(this)">
        {wordsDict[delim.start]}'''
        wordsDict[delim.start] = startWord
        if previousPointer >= 0:
            wordsDict[previousPointer] =  '</span>' + wordsDict[previousPointer]
        #wordsDict[delim.stop] =  '</span>' + wordsDict[delim.stop]
        previousPointer = delim.stop
        #print(f'''
        #wordsDict[delim.stop] is {wordsDict[delim.stop]} where stop is {delim.stop}
        #''')
        #flash(wordsDict[delim.start])
        #flash(wordsDict[delim.stop])
    # finish up
    wordsDict[previousPointer] =  '</span>' + wordsDict[previousPointer]

    for index, word in wordsDict.items():
        if index < start:
            continue
        if index > stop:
            break
        paragraphForDisplay += word

    return paragraphForDisplay #+ '<br>'+str(textobject.highlightDelims)


def getHighlightedSections(textobject):
    return Highlight.submitAllHighlightsFromText_toDB(textobject, submitToDB=False)
    '''returns a dictionary of Highlight objects'''
    #textList = []
    textDict = {}
    for delims in textobject.highlightDelims:
        hlight = Highlight(textobject, startChar=delims.start, endChar=delims.stop) #hlight = Highlight(textobject, delims)
        #textList.append(hlight)
        textDict[delims.start] = hlight
        #flash(f'got highlight:{delims.start}, {hlight}')
    return textDict


def getTextByTextID(textID):
    # a test response
    response = {'FullText_ID': 40, 'title': 'Untitled', 'text_tokenized': "['Your', 'Saved', 'Documents', 'Your', 'Saved', 'Documents', 'Your', 'Saved', 'Documents']", 'full_text': 'Your Saved Documents Your Saved Documents Your Saved Documents'}

    db = get_db().connect()
    cur = db.cursor()

    query = f'''SELECT * FROM pthompsoDB.FullText WHERE FullText_ID = {textID};'''
    #query = db.escape(query)
    cur.execute(query)
    response = cur.fetchone()
    return response


'''=======================Actions======================='''


# TODO
@bp.route('/submitText', methods=(POST,))
def submitText():
    log.info('Starting submitText() in marcaBP.py')
    '''takes submitted text
        returns a summary
        name = userInput
    '''
    originalText = 'hey'
    originalText = request.form['userInput']


    # OLD

    from marca.text_tools.extractive_summarizer import doArticleSummary
    summary = 'shorter...'
    summary, freq_table, sentences, sentence_scores, threshold \
        = doArticleSummary(originalText, threshold_factor = 0.75, test_mode=True, summary_as_list=True)


    percentOfOriginal = 100*(len(summary) / len(sentence_scores))
    percentOfOriginal = f'''{percentOfOriginal:.0f}'''

    return render_template('summary/homepage_summary.html', summary=summary,
                           percentOfOriginal=percentOfOriginal)
    #return render_template('dev/db.html', summary=summary, \
                           #sentences=fullText.getSentences(), \
                           #sentence_scores=sentence_scores, ft = freq_table)



# TODO
@bp.route('/<int:paragraphID>/<int:textID>/loadParagraph')
@login_required
def loadParagraph(paragraphID, textID):
    """ Retrieves FullText from DB that matches textID,
        retrieves the highlighted sections that appear in that paragraph,
        then returns the paragraph section matching paragraphID
        to display on the summary dashboard
    """

    #TODO

    return('TODO')







