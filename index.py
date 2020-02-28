#!/usr/bin/env python3

'''
set the name of the results file to be used for processing the summary
(entered as the action in form with id="text-form")
'''


import webprint, cgitb; cgitb.enable()
import cgi
from os import environ

webprint.printContentType()
form = cgi.FieldStorage()
def routeBasedOnGET():
    GOT = environ.get('QUERY_STRING')
    from sys import exit
    if GOT is not None:
        webprint.Homepage.printPage()
        webprint.printTesters()
    else:
        print("<br>GOT",GOT)
        pass




routeBasedOnGET()

