#!/usr/bin/env python3

'''
this file holds the logic to enable users to log in, including
 - getting user input from html form
 - querying the database
 - hashing user passwords
 - comparing the hash digests
 - ...
'''

# ===== region debug/testing ==================================================

# set verbose_success to True to see all successful "try" block messages
verbose_success = False

# ===== END region debug/testing





# ===== region imports ==================================================

import cgi, cgitb; cgitb.enable()
import os, traceback, sys

# ===== END region imports





# ===== region local variables ==================================================

# references HTML field storage element (placeholder) for later retrieval
html_form = cgi.FieldStorage()

#set nameOfThisFile to the name of this file
nameOfThisFile = "user-login.py"

# END ===== region local variables



username_in = html_form.getvalue('username_in')
