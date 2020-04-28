import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
i=0
from marca.text_tools.FullText import FullText
from marca.text_tools.FullText import Highlight
from marca.text_tools.FullText import escape
from marca.text_tools.FullText import Highlight
from flask import g, session, current_app, flash, request

def logg(message):
    log.info(f'''from SijaxHandler: {message}''')


class SijaxHandler(object):
    """A container class for all Sijax handlers.

    Grouping all Sijax handler functions in a class
    (or a Python module) allows them all to be registered with
    a single line of code.
    """

    @staticmethod
    def save_message(obj_response, message):

        message = message.strip()
        if message == '':
            return obj_response.alert("Empty messages are not allowed!")

        # Save message to database or whatever..

        import time, hashlib
        time_txt = time.strftime("%H:%M:%S", time.gmtime(time.time()))
        message_id = 'message_%s' % hashlib.sha256(time_txt.encode("utf-8")).hexdigest()

        message = """
        <div id="%s" style="opacity: 0;">
            [<strong>%s</strong>] %s
        </div>
        """ % (message_id, time_txt, message)

        # Add message to the end of the container
        obj_response.html_append('#messages', message)

        # Clear the textbox and give it focus in case it has lost it
        obj_response.attr('#message', 'value', '')
        obj_response.script("$('#message').focus();")

        # Scroll down the messages area
        obj_response.script("$('#messages').attr('scrollTop', $('#messages').attr('scrollHeight'));")

        # Make the new message appear in 400ms
        obj_response.script("$('#%s').animate({opacity: 1}, 400);" % message_id)


    @staticmethod
    def clear_messages(obj_response):

        # Delete all messages from the database

        # Clear the messages container
        obj_response.html('#messages', '')

        # Clear the textbox
        obj_response.attr('#message', 'value', '')

        # Ensure the texbox has focus
        obj_response.script("$('#message').focus();")


    @staticmethod
    def getText(obj_response, ID):
        ft = FullText.getFullText_fromDB(ID)
        obj_response.alert(ft.text)


    @staticmethod
    def jaxy(obj_response, arg1, arg2):
        obj_response.html("#div1","gotcha")
        #obj_response.alert(arg1)
        obj_response.alert(arg2)
        #obj_response.alert(arg[0] + " and " + arg[1])
        #obj_response.html('#paragraph-summary', 'hey there')


    # called by getHighlight(H_id)
    # in main.js
    @staticmethod
    def getHighlight(obj_response, H_id):
        user = g.user['userID']
        highlights = g.user['Highlights']
        activeHighlight = g.user['activeHighlight']
        '''TODO
        - build the Highlight object by ID
          - getting it's parent text
          - get the paragraph text from the full text
        - get ratings and notes from DB (after making this table!)
        -
        '''
        obj_response.alert(f'got user: {user} and H_id: {H_id}')


    @staticmethod
    def shell(obj_response, cmd):
        '''no...'''
        def my_exec(code):
            exec('global i; i = %s' % code)
            global i
            return i
        obj_response.html('#shell',my_exec(cmd))

    @staticmethod
    def refresh_active_highlight(obj_response, db_ID, newHighlightIndex):
        logg(f'''message from refresh_active_highlight
        db_ID = {db_ID}
        newHighlightIndex = {newHighlightIndex}''')
        textobject = FullText.getFullText_fromDB(db_ID)
        newHighlight = Highlight.getHighlightFromDB(textobject, newHighlightIndex)
        obj_response.script("$('.active').each(makeInactive)")

        # return all the portions of the page that need updating:
        #: active highlights (nav, paragraph, middle)

        # Nav
        obj_response.script(f'''$("#Nav{newHighlightIndex}").addClass("active")''')

        # paragraph text
        paragraphTextStart = newHighlight.paragraphParent
        from marca.marcaBP import prepareParagraphForDisplay
        paragraphText = prepareParagraphForDisplay(textobject, paragraphStartDelim=paragraphTextStart)
        obj_response.html("#paragraph-summary",f"{paragraphText}")
        obj_response.script(f'''$("#H{newHighlightIndex}").addClass("active")''')

        # middle section
        obj_response.html("#active-highlight",f"{newHighlight.text}")

        # clear all ratings
        obj_response.script('''$('input[type=radio]').each(function() {
            $(this).prop('checked',false);
        });''')

        # rating
        rating = newHighlight.userRating
        ratingBetween1and4 = rating > 0 and rating < 5
        if ratingBetween1and4:
            obj_response.script(f'''$('#rate{rating}').prop('checked',true)''')

        # notes
        userNotes = newHighlight.userNotes
        #userNotes = escape(userNotes)
        obj_response.script(f'''$("#userNotes").val(escape('{userNotes}'))''')



    @staticmethod
    def saveUserNotes(obj_response, textobjectID, highlightIndex, newNotes):
        #saveNotes
        textobject = FullText.getFullText_fromDB(textobjectID)
        highlight = Highlight.getHighlightFromDB(textobject, highlightIndex)
        highlight.saveNotes(newNotes)
        obj_response.script(f'''console.log('updated the user notes');''')


    @staticmethod
    def saveUserRating(obj_response, textobjectID, highlightIndex, ratingValue):
        #saveNotes
        textobject = FullText.getFullText_fromDB(textobjectID)
        highlight = Highlight.getHighlightFromDB(textobject, highlightIndex)
        highlight.saveRating(ratingValue)
        obj_response.script(f'''console.log('updated the user rating');''')


    @staticmethod
    def getPreviousParagraph(obj_response, textobjectID, paragraphStart):
        textobject = FullText.getFullText_fromDB(textobjectID)
        paragraphDelims = textobject.getTextFromParagraphStart(paragraphStart, returnSliceOnly=True)
        obj_response.script(f'''Sijax.request('refresh_active_highlight',
        [{textobjectID},newHighlightIndex],
        {{url: '/jax'}} \
        );''')


    @staticmethod
    def getNextParagraph(obj_response, arg):
        obj_response.alert('Sijax got arg: '+arg)





