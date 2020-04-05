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
    from db import get_db
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
    log.info('Starting def devDB()')
    db = get_db().connect()
    cur = db.cursor()

    if request.method==POST:
        query = request.form['query']
        DBexec = cur.execute(query)
        db.commit()
        DBresult = cur.fetchall()

        return render_template('dev/db.html',query=query, DBexec=DBexec, DBresult=DBresult)

    log.info('Finished def devDB()')
    #return redirect(url_for('index'))
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
    #: get user id
    userID = g.user['userID']
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

        #: tokenize the text
        from marca.text_tools.my_tokenize import word_tokenize
        #tokenizedText = str(word_tokenize(fullText))
        tokenizedText = word_tokenize(fullText)

        # query to call the MySQL proc call
        # like: CALL `pthompsoDB`.`insert_FullText`(<{IN tokenizedText TEXT}>, <{OUT output INT}>);
        #insertTextQuery = f'''CALL `pthompsoDB`.`insert_FullText` ("{tokenizedText}", );'''

        db = get_db().connect()
        cur = db.cursor()
        result = ""

        tokenizedTexta = "this is a test"
        #insertTextQuery = f'''CALL `pthompsoDB`.`insert_FullText` ("{tokenizedText}", );'''
        #>>> args = (5, 6, 0) # 0 is to hold value of the OUT parameter pProd
        #args = (tokenizedTexta, 0)
        #>>> cursor.callproc('multiply', args)
        #result, tokenizedTextID = cur.callproc('insert_FullText', args)


        #: submit to DB, get return value (tokenizedTextID)
        query = f'''INSERT INTO `FullText` (full_text) VALUES ("{tokenizedText}");'''
        result = cur.execute(query)
        db.commit()
        q1 = '''SELECT FullText_ID from pthompsoDB.FullText ORDER BY FullText_ID DESC LIMIT 1;'''
        cur.execute(q1)
        tokenizedTextRow =  cur.fetchone()
        tokenizedTextID = tokenizedTextRow['FullText_ID']

        #: get userAccountsID from g.user
        userAccountsID = userID

        # insert statement for text/user association
        fullText_UserAccount_assoc_Query = f'''INSERT INTO `pthompsoDB`.`user_FullText_assoc`
                (`userID`,
                `FullTextID`)
            VALUES
                ({userAccountsID},
                {tokenizedTextID});
            '''
        cur.execute(fullText_UserAccount_assoc_Query)
        db.commit()
        log.info('Finished submitText() in marcaBP.py')


# Submit text and userID to DB (make sure they are associated)

        flash('Document Uploaded Successfully')
        if userID == 29: # (then it's me testing)
            flash(f'got (first 20): {fullText[:20]}')
            flash(f'''and tokenized (first 1)= {tokenizedText[:1]}''')
            flash(f'''and userAccountsID= {userAccountsID}''')
            flash(f'''and result= {result}''')
            flash(f'''and tokenizedTextID= {tokenizedTextID}''')


    # continues if POST, jumps here if GET
    #: select texts from DB that match user
    userTexts = ['TODO', 'get','fromDB']


    #: render the dashboard template, send the user Texts also
    return render_template('summary/dashboard.html', userTexts=userTexts)


'''============================== REVIEW VIEW============================='''

@bp.route('/review', methods=(GET, POST))
# TODO change this to only POST method?
@login_required
def review():

    # it should only be POST (probably)
    if request.method == POST:
        fullTextID = request.form['fullTextID']

        #TODO finish this

    return render_template('summary/review.html')


'''=======================Actions======================='''


# TODO
@bp.route('/submitText', methods=(POST,))
def submitText():
    log.info('Starting submitText() in marcaBP.py')
    '''takes submitted text
        returns a summary
        form id="text-form"
    '''

    # TODO - FINISH AND TEST THIS

    #: get text from request (POST)
    rawText = "TODO"

    #: tokenize the text
    tokenizedText = "TODO"

    # query to call the MySQL proc call
    # like: CALL `pthompsoDB`.`insert_FullText`(<{IN tokenizedText TEXT}>, <{OUT output INT}>);
    insertTextQuery = f'''CALL `pthompsoDB`.`insert_FullText` ({tokenizedText}, );'''

    #: submit to DB, get return value (tokenizedTextID)
    tokenizedTextID = "TODO"

    #: get userAccountsID from g.user
    userAccountsID = "TODO"

    # insert statement for text/user association
    fullText_UserAccount_assoc_Query = f'''INSERT INTO `pthompsoDB`.`user_FullText_assoc`
            (`userID`,
            `FullTextID`)
        VALUES
            ({userAccountsID},
            {tokenizedTextID});
        '''
    log.info('Finished submitText() in marcaBP.py')

    #: return redirect(?) to dashboard
    return('TODO')



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







