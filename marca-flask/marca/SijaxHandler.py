import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
i=0
i+=1; log.info(f'''got to SijaxHandler at state {i}''') #1
from marca.text_tools.FullText import FullText
i+=1; log.info(f'''got to SijaxHandler at state {i}
importing Highlight''') #2
from marca.text_tools.FullText import Highlight
i+=1; log.info(f'''got to SijaxHandler at state {i}''')
from marca.text_tools.FullText import escape
i+=1; log.info(f'''got to SijaxHandler at state {i}''')
from marca.text_tools.FullText import Highlight
i+=1; log.info(f'''got to SijaxHandler at state {i}''')
from flask import g, session, current_app, flash, request
i+=1; log.info(f'''got to SijaxHandler at state {i}''')
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
    def refresh_active_highlight0(obj_response, newHighlightIndex):
        # set g's active highlight
        #g.user['activeHighlight'] =
        flash(f"request method form keys {request.form.keys()}")
        flash(f'Sijax has g is {g} with keys: {g.user.keys()}')
        obj_response.alert(f'g items: {g.user.items()}')
        return
        previousActiveHighlight = g.user['activeHighlight']
        newActiveHighlight = g.user['Highlights'][newHighlightIndex]
        g.user['activeHighlight'] = newActiveHighlight
        # return all the portions of the page that need updating:
        #: active highlights (nav, paragraph, middle)
        #: paragraph text
        #: middle section
        #: rating
        #: notes
        #obj_response.alert('refreshing!')


    @staticmethod
    def refresh_active_highlight(obj_response, db_ID, newHighlightIndex):
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

        # rating
        rating = newHighlight.userRating
        obj_response.script(f'''$('#rate{rating}').prop('checked',true)''')

        # notes
        userNotes = newHighlight.userNotes
        userNotes = escape(userNotes)
        obj_response.script(f'''$("#userNotes").val('{userNotes}')''')



    @staticmethod
    def saveUserNotes(obj_response, textobjectID, highlightIndex, newNotes):
        #saveNotes
        textobject = FullText.getFullText_fromDB(textobjectID)
        highlight = Highlight.getHighlightFromDB(textobject, highlightIndex)
        highlight.saveNotes(newNotes)


