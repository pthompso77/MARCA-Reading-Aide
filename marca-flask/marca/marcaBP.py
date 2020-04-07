"""
Main page for Marca app (index)
"""

import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.info('Starting marcaBP.py')


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


'''=======================Variables======================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'
# HTTP codes
http_notFound = 404
http_forbidden = 403


@bp.route('/dev/db', methods=(GET, POST))
def devDB():

    if g.user['userID'] != 29: #then the user isn't me and shouldn't see this page
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
    userAccountsID = g.user['userID']
    error = None


    ''' (as a logged-in user)
        Submit a new text document that will be uploaded to DB and available
        to review and interact with.

    request form name = newFullText
    '''
    #TODO
    #if method is POST
    if request.method == POST:
        # Get the text form submitted
        fullText = request.form['newFullText']
        fullText = request.form['newFullText'].replace("'","`")
        title = request.form['textTitle']
        if title == "":
            title = "Untitled"

        #: tokenize the text
        from marca.text_tools.my_tokenize import word_tokenize

        tokenizedText = word_tokenize(fullText)
        tokenizedText = str(tokenizedText).replace('"','""')

        db = get_db().connect()
        cur = db.cursor()
        result = ""

        #: submit text to DB
        print("fullText before: ",fullText,end="\n\n")
        fullText = fullText.replace('"','\\"')
        print("fullText after: ",fullText,end="\n\n")
        query = f'''INSERT INTO `FullText` (title, text_tokenized, full_text)
        VALUES ("%s","%s","%s");''' % (title, tokenizedText, fullText)
        print('\n',query)
        #query = db.escape(query)
        result = cur.execute(query)
        db.commit()

        #: get return value of new text insert (tokenizedTextID)
        q1 = '''SELECT FullText_ID from pthompsoDB.FullText ORDER BY FullText_ID DESC LIMIT 1;'''
        #q1 = db.escape(q1)
        cur.execute(q1)
        tokenizedTextRow =  cur.fetchone()
        tokenizedTextID = tokenizedTextRow['FullText_ID']


        # insert statement for text/user association
        fullText_UserAccount_assoc_Query = f'''INSERT INTO `pthompsoDB`.`user_FullText_assoc`
                (`userID`,
                `FullTextID`)
            VALUES
                ({userAccountsID},
                {tokenizedTextID});
            '''
        #fullText_UserAccount_assoc_Query = db.escape(fullText_UserAccount_assoc_Query)
        cur.execute(fullText_UserAccount_assoc_Query)
        db.commit()
        log.info('Finished submitText() in marcaBP.py')


# Submit text and userAccountsID to DB (make sure they are associated)

        flash('Document Uploaded Successfully')
        if userAccountsID == 29: # (then it's me testing)
            flash(f'got (first 20): {fullText[:20]}')
            flash(f'''and tokenized (first 1)= {tokenizedText[:1]}''')
            flash(f'''and userAccountsID= {userAccountsID}''')
            flash(f'''and result= {result}''')
            flash(f'''and tokenizedTextID= {tokenizedTextID}''')


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

@bp.route('/<int:textID>/review', methods=(GET, POST))
@login_required
def review(textID):

    # it should only be POST (probably)
    if request.method == POST:
        fullTextID = request.form['fullTextID']

        #TODO finish this

    text = getTextByTextID(textID)
    return render_template('summary/review.html',textID=textID, text=text)
    # (or return a redirect?)


'''===========Review helpers==========='''

def getTextByTextID(textID):
    # test response
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

    #from marca.text_tools.extractive_summarizer import doArticleSummary
    summary = 'shorter...'
    #summary = doArticleSummary(originalText)


    '''Now for my_tokenize paragraph summary'''
    from marca.text_tools.my_tokenize import paragraph_tokenize
    summary = 'paragraphs...'
    summary = paragraph_tokenize(originalText)


    ts = len(summary)
    #: return redirect(?) to dashboard
    return render_template('dev/db.html', summary=summary)



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







