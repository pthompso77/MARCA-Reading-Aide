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
    """A container class for all Sijax methods."""

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
        log.info(f'userNotes = {userNotes}')
        from marca.text_tools.FullText import escape
        userNotes = escape(userNotes)
        #obj_response.script(f'''$("#userNotes").val(unescape(escape("{userNotes}")))''')
        obj_response.script(f'''$("#userNotes").val('{userNotes}')''')



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
        try:
            textobject = FullText.getFullText_fromDB(textobjectID)
        except Exception as e:
            logg(f'''Exception trying to get FullText with ID={textobjectID} \
            in paragraphStart1: {e}''')
            textobject = None

        paragraphDelims = textobject.getTextFromParagraphStart(paragraphStart, returnSliceOnly=True)
        logg(f'ok so far 2...paragraphDelims = {paragraphDelims.start}')

        try:
            obj_response.script(f'''alert('trying nested Sijax with index: ' + newHighlightIndex);
            Sijax.request('refresh_active_highlight',
            [{textobjectID},newHighlightIndex],
            {{url: '/jax'}} \
            );
            console.log("{textobject.paragraphDelims}")''')
            logg('ok so far 3...')
        except Exception as e:
            logg(f'''Exception in paragraphStart2: {e}''')


    @staticmethod
    def getNextParagraph(obj_response, arg):
        obj_response.alert('Sijax got arg: '+arg)





