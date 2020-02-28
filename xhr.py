#!/usr/bin/env python3

'''
set the name of the results file to be used for processing the summary
(entered as the action in form with id="text-form")
'''


import webprint, cgitb; cgitb.enable()
import cgi
from os import environ

webprint.printContentType(includeDoctype=False)
form = cgi.FieldStorage()
def routeBasedOnGET():
    GOT = environ.get('QUERY_STRING')
    GOTsplit = GOT.split('=')
    from sys import exit
    if GOT is not None:
        #webprint.Homepage.printPage()
        #webprint.printTesters()
        print("GOT is not None...wtf GOT? = ",GOT)
        print("GOTsplit = ",GOTsplit)
        try:
            #print(environ.items)
            pass
        except Exception as e:
            print('exception...', e)
    else:
        print("<br>GOT",GOT)
        pass




routeBasedOnGET()

